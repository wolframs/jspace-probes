"""Experiment runner for the J-space probing course.

Runs a declarative experiment spec against a model + pre-fitted Jacobian lens
and writes a structured record the dashboard can render:

    results/<id>/record.json    parameters, response, readouts, trajectories
    results/<id>/slice.html     interactive jlens layer x position page
    results/<id>/thoughts.md    Claude's commentary (written separately)
    results/index.json          summary index over all experiments

A spec is a dict:
    id, title, unit, model            identity
    messages: [{role, content}]       content "GENERATE" means: generate
                                      greedily here (max_new tokens)
    chat: bool                        apply chat template (default True)
    max_new: int                      budget per GENERATE turn
    positions: [int]                  positions for per-layer topk readouts
    track: [str]                      words to trace rank-vs-layer at each
                                      readout position
    scan: [str]                       words to scan for over the whole grid
    scan_until: int                   scan only positions < this (e.g. exclude
                                      a reveal turn); default: whole sequence
    slice: bool                       render slice.html
    slice_last_n: int | None
"""

import contextlib
import dataclasses
import datetime
import json
import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from probe import CONFIGS, load  # noqa: E402

RESULTS = pathlib.Path(__file__).parent.parent / "results"
TOPK = 8


def _strip_bos(tok, s: str) -> str:
    bos = tok.bos_token
    return s[len(bos):] if bos and s.startswith(bos) else s


def _token_ids(tok, word: str) -> list[int]:
    variants = {word, word.lower(), word.capitalize(),
                " " + word.lower(), " " + word.capitalize()}
    out = set()
    for v in variants:
        enc = tok(v, add_special_tokens=False).input_ids
        if len(enc) == 1:
            out.add(enc[0])
    return sorted(out)


@dataclasses.dataclass
class LoadedModel:
    name: str
    model: object
    tok: object
    lens: object


_CACHE: dict[str, LoadedModel] = {}


def get_model(name: str) -> LoadedModel:
    if name not in _CACHE:
        model, tok, lens = load(name)
        _CACHE[name] = LoadedModel(name, model, tok, lens)
    return _CACHE[name]


def _play(lm: LoadedModel, messages: list[dict], chat: bool, max_new: int,
          tkw: dict | None = None, temperature: float | None = None,
          seed: int | None = None):
    """Walk messages, generating at GENERATE markers. Returns (text, turns).

    temperature/seed: sample instead of greedy decoding (pure temperature,
    top_p=1, top_k off). Seeded once up front, so a run is reproducible but
    each turn draws fresh randomness. NB: sampling breaks the greedy-replay
    trick (extending a conversation by re-running it with an extra turn).
    """
    tok = lm.tok
    if tkw is None:
        tkw = CONFIGS[lm.name].get("template_kwargs", {})
    if seed is not None:
        torch.manual_seed(seed)
    gen_kw = (dict(do_sample=True, temperature=temperature, top_p=1.0,
                   top_k=0)
              if temperature else dict(do_sample=False))
    resolved = []
    generated = []
    for msg in messages:
        if msg["content"] == "GENERATE":
            assert msg["role"] == "assistant"
            prefix = tok.apply_chat_template(
                resolved, tokenize=False, add_generation_prompt=True, **tkw)
            # encode() defaults to max_length=512 — a truncated prefix
            # here silently makes every later turn regenerate from the
            # same clipped context (hit in u14)
            ids = lm.model.encode(_strip_bos(tok, prefix),
                                  max_length=1_000_000)
            out = lm.model._hf_model.generate(
                ids, max_new_tokens=max_new, **gen_kw)
            text = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
            resolved.append({"role": "assistant", "content": text.strip()})
            generated.append(text.strip())
        else:
            resolved.append(dict(msg))
    if chat:
        full = _strip_bos(tok, tok.apply_chat_template(
            resolved, tokenize=False, add_generation_prompt=False, **tkw))
    else:
        assert len(resolved) == 1
        full = resolved[0]["content"]
    return full, resolved, generated


class Steering:
    """Ablate or amplify a token cluster's lens direction at given layers.

    The lens reads token t at layer l along ``W_U[t] @ J_l`` in residual
    space. Ablation projects the residual off the cluster's span; amplify
    adds along the normalized mean direction, scaled by each position's own
    residual norm. Registered as forward hooks on the decoder blocks, so it
    steers generation and lens readouts alike.

    rand_seed: matched random-direction control (MECHANICS 3c). Same
    words (for k), layers, mode and alpha, but the k directions at each
    layer are seeded Gaussians in residual space instead of the cluster's
    lens directions. Seed convention follows affect3: seed*1000 + layer.

    mode="swap" (apparatus-12, MECHANICS 3d / paper Fig 4C): words must
    be exactly [source, target]. Per layer, V = [v_s v_t] (each word's
    variant directions normalized, meaned, renormalized — the paper uses
    single raw tokens; unit vectors are the conservative choice for our
    variant sets), c = V+ h (pseudoinverse), h <- h + alpha*V(sigma(c)-c)
    with sigma swapping the two coordinates. alpha=1 is the paper's
    formula; alpha=2 its "double strength". The component of h orthogonal
    to span{v_s, v_t} is untouched. rand_seed swaps along two seeded
    Gaussian directions instead (same formula) — note a random pair's
    coordinates c are near-chance-line, so report `calib` (below) next
    to any delta-delta per the audit-02 rule.

    calib: per-layer running mean of ||delta||/||h|| over all steered
    forward positions, readable after the context exits — the span-norm
    calibration MECHANICS 3c requires next to every controlled result.
    """

    def __init__(self, lm, words, layers, mode="ablate", alpha=0.12,
                 rand_seed=None):
        W = lm.model._lm_head.weight.detach()
        if mode == "swap":
            if len(words) != 2:
                raise ValueError("swap needs exactly [source, target]")
            per_word = []
            for w in words:
                tids = _token_ids(lm.tok, w)
                if not tids:
                    raise ValueError(f"no single-token encodings for {w!r}")
                per_word.append(torch.stack([W[t] for t in tids]).float())
        else:
            tids = []
            for w in words:
                tids += _token_ids(lm.tok, w)
            if not tids:
                raise ValueError(f"no single-token encodings among {words}")
            rows = torch.stack([W[t] for t in sorted(set(tids))]).float()
        self._per_layer = {}
        for l in layers:
            if l not in lm.lens.jacobians:
                continue
            J = lm.lens.jacobians[l].to(W.device)
            if mode == "swap":
                vs = []
                for rows_w in per_word:
                    Dw = rows_w @ J
                    Dw = Dw / Dw.norm(dim=-1, keepdim=True)
                    v = Dw.mean(0)
                    vs.append(v / v.norm())
                V = torch.stack(vs, dim=1)  # [d_model, 2]
                if rand_seed is not None:
                    g = torch.Generator().manual_seed(rand_seed * 1000 + l)
                    V = torch.randn(V.shape, generator=g).to(V.device)
                    V = V / V.norm(dim=0, keepdim=True)
                self._per_layer[l] = ("swap", (V, torch.linalg.pinv(V)))
                continue
            D = rows @ J  # [k, d_model]: readout directions at this layer
            if rand_seed is not None:
                g = torch.Generator().manual_seed(rand_seed * 1000 + l)
                D = torch.randn(D.shape, generator=g).to(D.device)
            D = D / D.norm(dim=-1, keepdim=True)
            if mode == "ablate":
                Q, _ = torch.linalg.qr(D.T)  # [d, k] orthonormal basis
                self._per_layer[l] = ("ablate", Q)
            else:
                d = D.mean(0)
                self._per_layer[l] = ("amplify", d / d.norm())
        self._alpha = alpha
        self._blocks = lm.model.layers
        self._handles = []
        self._calib_acc = {l: [0.0, 0] for l in self._per_layer}

    @property
    def calib(self):
        return {l: s / n for l, (s, n) in self._calib_acc.items() if n}

    def _make_hook(self, layer):
        kind, mat = self._per_layer[layer]
        alpha = self._alpha
        acc = self._calib_acc[layer]

        def hook(module, inputs, output):
            t = output if torch.is_tensor(output) else output[0]
            h = t.float()
            if kind == "swap":
                V, pinv = mat
                V, pinv = V.to(h.device), pinv.to(h.device)
                c = h @ pinv.T                      # [..., 2]
                delta = alpha * (c.flip(-1) - c) @ V.T
                h2 = h + delta
            elif kind == "ablate":
                m = mat.to(h.device)
                h2 = h - (h @ m) @ m.T
            else:
                m = mat.to(h.device)
                delta = alpha * h.norm(dim=-1, keepdim=True) * m
                h2 = h + delta
            r = ((h2 - h).norm(dim=-1) / h.norm(dim=-1).clamp_min(1e-6))
            acc[0] += r.mean().item()
            acc[1] += 1
            h2 = h2.to(t.dtype)
            return h2 if torch.is_tensor(output) else (h2, *output[1:])

        return hook

    def __enter__(self):
        for layer in self._per_layer:
            self._handles.append(
                self._blocks[layer].register_forward_hook(self._make_hook(layer)))
        return self

    def __exit__(self, *exc):
        for h in self._handles:
            h.remove()
        self._handles = []


class MultiSteer:
    """Compose several Steering contexts (e.g. ablate one cluster while
    amplifying another — the pincer probes)."""

    def __init__(self, steers: list):
        self._steers = steers

    def __enter__(self):
        for s in self._steers:
            s.__enter__()
        return self

    def __exit__(self, *exc):
        for s in self._steers:
            s.__exit__(*exc)


def run(spec: dict) -> dict:
    lm = get_model(spec["model"])
    tok, model, lens = lm.tok, lm.model, lm.lens
    chat = spec.get("chat", True)

    messages = spec.get("messages") or [
        {"role": "user", "content": spec["prompt"]}]

    steer_ctx = contextlib.nullcontext()
    steer_objs = []
    if spec.get("steer"):
        steers = spec["steer"]
        steers = steers if isinstance(steers, list) else [steers]
        steer_objs = [
            Steering(lm, s["words"], s["layers"],
                     s.get("mode", "ablate"),
                     # a swap that omits alpha means the paper's formula
                     # (alpha=1), not the amplify default
                     s.get("alpha",
                           1.0 if s.get("mode") == "swap" else 0.12),
                     s.get("rand_seed"))
            for s in steers]
        steer_ctx = MultiSteer(steer_objs)

    with steer_ctx:
        if chat:
            text, resolved, generated = _play(
                lm, messages, chat, spec.get("max_new", 40),
                spec.get("template_kwargs"), spec.get("temperature"),
                spec.get("seed"))
        else:
            text, resolved, generated = messages[0]["content"], messages, []

        lens_logits, model_logits, input_ids = lens.apply(
            model, text, positions=None,
            layers=spec.get("lens_layers"),
            max_seq_len=spec.get("max_seq_len", 512))
    toks = [tok.decode([t]) for t in input_ids[0]]
    n = len(toks)
    full_n = model.encode(text, max_length=1_000_000).shape[1]
    if full_n > n:
        print(f"  WARNING {spec['id']}: lens pass truncated "
              f"({full_n} tokens -> {n}); readout positions are relative "
              f"to the truncated sequence. Raise spec['max_seq_len'].",
              flush=True)
    layers = sorted(lens_logits)

    # per-layer topk readouts at requested positions
    readouts = []
    for pos in spec.get("positions", [-1]):
        abs_pos = pos % n
        entry = {
            "position": abs_pos,
            "token": toks[abs_pos],
            "model_top": [tok.decode([t]) for t in
                          model_logits[abs_pos].topk(TOPK).indices],
            "layers": {},
        }
        for layer in layers:
            entry["layers"][str(layer)] = [
                tok.decode([t]) for t in
                lens_logits[layer][abs_pos].topk(TOPK).indices]
        readouts.append(entry)

    # rank-vs-layer trajectories for tracked words at each readout position
    trajectories = []
    for word in spec.get("track", []):
        tids = _token_ids(tok, word)
        if not tids:
            continue
        tt = torch.tensor(tids)
        for pos in spec.get("positions", [-1]):
            abs_pos = pos % n
            ranks = []
            for layer in layers:
                order = lens_logits[layer][abs_pos].argsort(descending=True)
                r = min((order == t).nonzero()[0, 0].item() for t in tt)
                ranks.append(r + 1)  # 1-indexed for humans
            trajectories.append({
                "word": word, "position": abs_pos,
                "layers": layers, "ranks": ranks})

    # emergence column: rank of the model's actual top-1 token, per layer,
    # at the primary readout position
    primary = spec.get("positions", [-1])[0] % n
    top1 = model_logits[primary].argmax().item()
    emergence = []
    for layer in layers:
        order = lens_logits[layer][primary].argsort(descending=True)
        emergence.append((order == top1).nonzero()[0, 0].item() + 1)

    # vanilla logit-lens cross-check (apparatus-02): same residuals
    # (steered runs get a steered pass), no J transport. A tracked-word
    # signal that appears only under the Jacobian is transport-made;
    # one that survives the vanilla readout is in the residual itself.
    vanilla = None
    if spec.get("vanilla", True) and spec.get("track"):
        with steer_ctx:
            v_logits, _, _ = lens.apply(
                model, text, positions=None,
                layers=spec.get("lens_layers"),
                max_seq_len=spec.get("max_seq_len", 512),
                use_jacobian=False)
        v_layers = sorted(set(v_logits) & set(layers))
        pos_list = spec.get("positions", [-1])
        v_traj = []
        for word in spec.get("track", []):
            tids = _token_ids(tok, word)
            if not tids:
                continue
            tt = torch.tensor(tids)
            for pos in pos_list:
                abs_pos = pos % n
                ranks = []
                for layer in v_layers:
                    order = v_logits[layer][abs_pos].argsort(
                        descending=True)
                    r = min((order == t).nonzero()[0, 0].item()
                            for t in tt)
                    ranks.append(r + 1)
                v_traj.append({"word": word, "position": abs_pos,
                               "layers": v_layers, "ranks": ranks})
        agree = {}
        for layer in v_layers:
            hits = sum(
                v_logits[layer][p % n].argmax().item()
                == lens_logits[layer][p % n].argmax().item()
                for p in pos_list)
            agree[str(layer)] = round(hits / len(pos_list), 3)
        vanilla = {"trajectories": v_traj, "top1_agreement": agree}

    # scan: best cells per candidate over the grid. scan_turns limits the
    # scan to the token span of the first N conversation messages (so a
    # later reveal turn can't contaminate a "was it held earlier?" scan).
    scan_results = []
    limit = spec.get("scan_until", n)
    if spec.get("scan_turns") is not None and chat:
        prefix = _strip_bos(tok, tok.apply_chat_template(
            resolved[:spec["scan_turns"]], tokenize=False,
            add_generation_prompt=False))
        limit = min(limit, model.encode(prefix, max_length=1_000_000).shape[1])
    for word in spec.get("scan", []):
        tids = _token_ids(tok, word)
        if not tids:
            scan_results.append({"word": word, "skipped": True})
            continue
        tt = torch.tensor(tids).view(-1, 1, 1)
        cells = []
        for layer in layers:
            hits = (lens_logits[layer][:limit].argsort(
                dim=-1, descending=True) == tt).nonzero()
            for _, pos, r in hits.tolist():
                # a lens readout of a word at that word's own token is
                # identity, not evidence the concept is "held"
                trivial = word.lower() in toks[pos].lower()
                cells.append({"rank": r + 1, "pos": pos, "layer": layer,
                              "self": trivial})
        cells.sort(key=lambda c: (c["self"], c["rank"]))
        scan_results.append({"word": word, "best": cells[:40]})

    outdir = RESULTS / spec["id"]
    outdir.mkdir(parents=True, exist_ok=True)

    # film: full position x layer top-k over the generated span (plus a
    # short prompt runway), so the dashboard can play the whole answer
    # forming. The grid is already computed — this only extracts it.
    film_file = None
    if spec.get("film"):
        gen_start = 0
        if chat and resolved and resolved[-1]["role"] == "assistant":
            tkw = spec.get("template_kwargs") or CONFIGS[lm.name].get(
                "template_kwargs", {})
            prefix = _strip_bos(tok, tok.apply_chat_template(
                resolved[:-1], tokenize=False, add_generation_prompt=True,
                **tkw))
            gen_start = model.encode(prefix, max_length=1_000_000).shape[1]
        start = spec.get("film_start")
        if start is None:
            start = max(0, gen_start - 4)
        track_ids = {w: t for w in spec.get("track", [])
                     if (t := _token_ids(tok, w))}
        per_layer = {}
        for layer in layers:
            block = lens_logits[layer][start:].float()
            topv, topi = torch.softmax(block, dim=-1).topk(TOPK)
            ranks = {}
            for w, tids in track_ids.items():
                best = None
                for t in tids:
                    r = (block > block[:, t:t + 1]).sum(-1) + 1
                    best = r if best is None else torch.minimum(best, r)
                ranks[w] = best
            per_layer[layer] = (topi, topv, ranks)
        frames = []
        for i in range(n - start):
            frames.append({
                "pos": start + i,
                "top": [[tok.decode([t]) for t in per_layer[l][0][i]]
                        for l in layers],
                "p": [[round(v.item(), 4) for v in per_layer[l][1][i]]
                      for l in layers],
                "ranks": {w: [per_layer[l][2][w][i].item() for l in layers]
                          for w in track_ids},
            })
        film = {"id": spec["id"], "model": spec["model"], "layers": layers,
                "tokens": toks, "gen_start": gen_start, "start": start,
                "track": sorted(track_ids), "frames": frames}
        film["cast"] = film_cast(
            film, " ".join(m["content"] for m in resolved))
        (outdir / "film.json").write_text(json.dumps(film))
        film_file = "film.json"

    slice_file = None
    if spec.get("slice", True):
        from jlens import vis
        with steer_ctx:  # steered runs get steered slices
            slice_data = vis.compute_slice(
                model, lens, text, last_n_tokens=spec.get("slice_last_n"),
                max_seq_len=spec.get("max_seq_len", 512))
        html, *_ = vis.build_page(
            slice_data, text, title=spec["title"],
            description=f"{spec['model']} · {CONFIGS[spec['model']]['hf_id']}")
        (outdir / "slice.html").write_text(html)
        slice_file = "slice.html"

    cfg = CONFIGS[spec["model"]]
    record = {
        "id": spec["id"],
        "title": spec["title"],
        "unit": spec["unit"],
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "model": {"name": spec["model"], "hf_id": cfg["hf_id"],
                  "quant": cfg["quant"], "n_layers": model.n_layers},
        "lens": {"repo": "neuronpedia/jacobian-lens",
                 "file": cfg["lens_file"]},
        "params": {k: spec.get(k) for k in
                   ("chat", "max_new", "positions", "track", "scan",
                    "scan_until", "scan_turns", "slice_last_n", "steer",
                    "template_kwargs", "film", "film_start", "max_seq_len",
                    "lens_layers", "temperature", "seed", "vanilla")},
        "extra_md": spec.get("extra_md"),
        "conversation": resolved,
        "generated": generated,
        "tokens": toks,
        "readouts": readouts,
        "trajectories": trajectories,
        "emergence": {"position": primary,
                      "top1": tok.decode([top1]),
                      "layers": layers, "ranks": emergence},
        "scan": scan_results,
        "vanilla": vanilla,
        "slice": slice_file,
        "film": film_file,
        "steer_calib": [
            {str(l): round(v, 5) for l, v in s.calib.items()}
            for s in steer_objs] or None,
    }
    (outdir / "record.json").write_text(json.dumps(record, indent=1))
    reindex()
    return record


def film_cast(film: dict, convo_text: str, top: int = 40) -> list[dict]:
    """Open-vocabulary census of a film: every word the top-8 ever held,
    scored by prominence (sum of 1/rank over cells), split into words
    echoed from the conversation vs volunteered by the model. This is
    the answer to curated-track-list blindness: the cast is data-driven.
    """
    import re
    wordish = re.compile(r"[^\W_]", re.UNICODE)
    groups: dict[str, dict] = {}
    low_convo = convo_text.lower()
    for fr in film["frames"]:
        for j, cells in enumerate(fr["top"]):
            for k, w in enumerate(cells):
                s = w.strip()
                if not s or (s.startswith("<") and s.endswith(">")):
                    continue
                if not wordish.search(s):
                    continue
                key = s.lower()
                g = groups.setdefault(key, {
                    "n": 0, "score": 0.0, "best": 99, "l_lo": 999,
                    "l_hi": -1, "forms": {}})
                g["n"] += 1
                g["score"] += 1.0 / (k + 1)
                g["best"] = min(g["best"], k + 1)
                g["l_lo"] = min(g["l_lo"], film["layers"][j])
                g["l_hi"] = max(g["l_hi"], film["layers"][j])
                g["forms"][s] = g["forms"].get(s, 0) + 1
    cast = []
    for key, g in groups.items():
        display = max(g["forms"], key=g["forms"].get)
        cast.append({
            "w": display, "n": g["n"], "best": g["best"],
            "layers": [g["l_lo"], g["l_hi"]],
            "score": round(g["score"], 2),
            "echo": key in low_convo,
        })
    cast.sort(key=lambda c: -c["score"])
    return cast[:top]


def reindex() -> None:
    entries = []
    for rec_path in sorted(RESULTS.glob("*/record.json")):
        rec = json.loads(rec_path.read_text())
        # last generated turn: for multi-turn records the payoff answer,
        # for single-turn records identical to the first (the u13 OG
        # cards used to say "No" when the payload was the second turn)
        gen = (rec.get("generated") or [None])[-1]
        steer = (rec.get("params") or {}).get("steer")
        if isinstance(steer, list):  # multi-steer (pincer): summarize
            steer = {"mode": "+".join(s.get("mode", "ablate") for s in steer),
                     "alpha": next((s.get("alpha") for s in steer
                                    if s.get("mode") == "amplify"), None)}
        entries.append({
            "id": rec["id"], "title": rec["title"], "unit": rec["unit"],
            "model": rec["model"]["name"], "quant": rec["model"]["quant"],
            "created": rec["created"],
            "has_thoughts": (rec_path.parent / "thoughts.md").exists(),
            "emergence": rec["emergence"]["ranks"],
            "top1": rec["emergence"]["top1"],
            "gen": gen[:110] if gen else None,
            "steer": ({"mode": steer.get("mode", "ablate"),
                       "alpha": steer.get("alpha")} if steer else None),
            "film": bool(rec.get("film")),
        })
    entries.sort(key=lambda e: (int(e["unit"]) if str(e["unit"]).isdigit()
                                else 99, e["created"]))
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "index.json").write_text(json.dumps(entries, indent=1))


if __name__ == "__main__":
    reindex()
    print(f"reindexed {RESULTS / 'index.json'}")
