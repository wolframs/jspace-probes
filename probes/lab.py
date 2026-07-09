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


def _play(lm: LoadedModel, messages: list[dict], chat: bool, max_new: int):
    """Walk messages, generating at GENERATE markers. Returns (text, turns)."""
    tok = lm.tok
    tkw = CONFIGS[lm.name].get("template_kwargs", {})
    resolved = []
    generated = []
    for msg in messages:
        if msg["content"] == "GENERATE":
            assert msg["role"] == "assistant"
            prefix = tok.apply_chat_template(
                resolved, tokenize=False, add_generation_prompt=True, **tkw)
            ids = lm.model.encode(_strip_bos(tok, prefix))
            out = lm.model._hf_model.generate(
                ids, max_new_tokens=max_new, do_sample=False)
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
    """

    def __init__(self, lm, words, layers, mode="ablate", alpha=0.12):
        tids = []
        for w in words:
            tids += _token_ids(lm.tok, w)
        if not tids:
            raise ValueError(f"no single-token encodings among {words}")
        W = lm.model._lm_head.weight.detach()
        rows = torch.stack([W[t] for t in sorted(set(tids))]).float()
        self._per_layer = {}
        for l in layers:
            if l not in lm.lens.jacobians:
                continue
            J = lm.lens.jacobians[l].to(rows.device)
            D = rows @ J  # [k, d_model]: readout directions at this layer
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

    def _make_hook(self, layer):
        kind, mat = self._per_layer[layer]
        alpha = self._alpha

        def hook(module, inputs, output):
            t = output if torch.is_tensor(output) else output[0]
            h = t.float()
            m = mat.to(h.device)
            if kind == "ablate":
                h = h - (h @ m) @ m.T
            else:
                h = h + alpha * h.norm(dim=-1, keepdim=True) * m
            h = h.to(t.dtype)
            return h if torch.is_tensor(output) else (h, *output[1:])

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


def run(spec: dict) -> dict:
    lm = get_model(spec["model"])
    tok, model, lens = lm.tok, lm.model, lm.lens
    chat = spec.get("chat", True)

    messages = spec.get("messages") or [
        {"role": "user", "content": spec["prompt"]}]

    steer_ctx = contextlib.nullcontext()
    if spec.get("steer"):
        s = spec["steer"]
        steer_ctx = Steering(lm, s["words"], s["layers"],
                             s.get("mode", "ablate"), s.get("alpha", 0.12))

    with steer_ctx:
        if chat:
            text, resolved, generated = _play(
                lm, messages, chat, spec.get("max_new", 40))
        else:
            text, resolved, generated = messages[0]["content"], messages, []

        lens_logits, model_logits, input_ids = lens.apply(
            model, text, positions=None)
    toks = [tok.decode([t]) for t in input_ids[0]]
    n = len(toks)
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

    # scan: best cells per candidate over the grid. scan_turns limits the
    # scan to the token span of the first N conversation messages (so a
    # later reveal turn can't contaminate a "was it held earlier?" scan).
    scan_results = []
    limit = spec.get("scan_until", n)
    if spec.get("scan_turns") is not None and chat:
        prefix = _strip_bos(tok, tok.apply_chat_template(
            resolved[:spec["scan_turns"]], tokenize=False,
            add_generation_prompt=False))
        limit = min(limit, model.encode(prefix).shape[1])
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

    slice_file = None
    if spec.get("slice", True):
        from jlens import vis
        with steer_ctx:  # steered runs get steered slices
            slice_data = vis.compute_slice(
                model, lens, text, last_n_tokens=spec.get("slice_last_n"))
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
                    "scan_until", "scan_turns", "slice_last_n", "steer")},
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
        "slice": slice_file,
    }
    (outdir / "record.json").write_text(json.dumps(record, indent=1))
    reindex()
    return record


def reindex() -> None:
    entries = []
    for rec_path in sorted(RESULTS.glob("*/record.json")):
        rec = json.loads(rec_path.read_text())
        entries.append({
            "id": rec["id"], "title": rec["title"], "unit": rec["unit"],
            "model": rec["model"]["name"], "quant": rec["model"]["quant"],
            "created": rec["created"],
            "has_thoughts": (rec_path.parent / "thoughts.md").exists(),
            "emergence": rec["emergence"]["ranks"],
            "top1": rec["emergence"]["top1"],
        })
    entries.sort(key=lambda e: (e["unit"], e["created"]))
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "index.json").write_text(json.dumps(entries, indent=1))


if __name__ == "__main__":
    reindex()
    print(f"reindexed {RESULTS / 'index.json'}")
