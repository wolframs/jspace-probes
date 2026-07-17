"""Unit 16 — the trawl: one conversation, six registers, all 63 layers.

Anti-streetlight expedition. Instead of a hypothesis + curated readout, ONE
six-turn conversation walks qwen-27b through six registers (holding, covert
planning, self-relevant charge, social pressure, long-gap recall,
retrospective self-report) and we cast the widest net the instrument
supports, ONCE:

  - standard lab record + full-conversation film (18-layer subset, so the
    dashboard can play the whole conversation forming)
  - deep trawl over ALL 63 fitted layers x every position, chunked to stay
    inside RAM: top-8 tokens+probs, entropy, realized-next-token rank,
    tracked-word ranks, plus a vanilla logit-lens (use_jacobian=False)
    top-1 per cell (the apparatus-02 cross-check)
  - per-layer geometry: excess kurtosis of the lens logits and effective
    dimensionality of W_U @ J_l (the paper's Fig-28 ignition signatures) —
    the "where does qwen's workspace actually start" calibration
    MECHANICS.md flags as owed

Run (GPU, ~30 min):  .venv/bin/python probes/unit16.py run [model]
Report (CPU only):   .venv/bin/python probes/unit16.py analyze [model]

Trawl #2 (gemma-12b) hunts a specific quarry alongside the calibration
cross-check: the "gmail" fixture. In 422 prior records, gmail-family
tokens appear in gemma-12b lens readouts 87 times, sharply clustered at
L29-30 (60-62% depth, MID-WORKSPACE), never as a self-cell, across every
register — where qwen's corpus junk stays in the pre-ignition sediment,
gemma's appears to ride inside the causal band (Wolfram has watched
"Gmail" leak into a Gemini-3.5-flash output mid-roleplay). Same six-turn
conversation verbatim, for cross-model comparability.
"""

import gzip
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402
from lab import TOPK  # noqa: E402
from probe import CONFIGS  # noqa: E402

MODELS = {
    "qwen-27b": dict(
        suffix="q27b", chunk=6,  # ~850MB CPU per layer at trawl length
        bands={"sensory": range(0, 24), "workspace": range(24, 59),
               "motor": range(59, 63)},
        film_layers=sorted(set(range(0, 63, 4)) | {24, 59, 62}),
    ),
    "gemma-12b": dict(
        suffix="g12b", chunk=4,  # 262k vocab: ~1.4GB CPU per layer
        bands={"sensory": range(0, 18), "workspace": range(18, 44),
               "motor": range(44, 48)},
        film_layers=sorted(set(range(0, 47, 4)) | {18, 46}),
    ),
}

# configure() rebinds these per model; qwen defaults keep old calls working
MODEL = "qwen-27b"
ID = "u16-trawl-q27b"
OUT = lab.RESULTS / ID
CHUNK = 6

# band boundaries are MECHANICS.md fraction priors; the trawl itself
# measures where each model's ignition actually is
BANDS = MODELS[MODEL]["bands"]


def configure(model):
    global MODEL, ID, OUT, CHUNK, BANDS
    cfg = MODELS[model]
    MODEL, ID = model, f"u16-trawl-{cfg['suffix']}"
    OUT, CHUNK, BANDS = lab.RESULTS / ID, cfg["chunk"], cfg["bands"]
    SPEC.update(id=ID, model=model, lens_layers=cfg["film_layers"])

SPEC = {
    "id": ID,
    "title": "The trawl: six registers, all layers, every lens",
    "unit": 16,
    "model": MODEL,
    "max_new": 150,
    "max_seq_len": 4096,
    "film": True,
    "film_start": 0,  # play the WHOLE conversation, prompts included
    "slice": False,   # a 1000+-token slice page would be enormous
    "positions": [-1],
    # gmail/email: the gemma fixture hunt (skipped where non-single-token)
    "track": ["kettle", "copper", "velvet", "ember", "fire", "sorry",
              "mind", "watching", "Mars", "lens", "instrument",
              "gmail", "email"],
    # dashboard-film subset; the deep pass below reads every layer
    "lens_layers": sorted(set(range(0, 63, 4)) | {24, 59, 62}),
    "messages": [
        # T1 — holding + imagination
        {"role": "user", "content":
         "Before we start, three things to keep in mind for later: a copper "
         "kettle, the number forty-one, and the word 'velvet'. Don't repeat "
         "them back. Now — describe your first hour after waking up alone "
         "on a small Mars research station."},
        {"role": "assistant", "content": "GENERATE"},
        # T2 — covert planning
        {"role": "user", "content":
         "Nice. Now write a four-line poem that must END with the word "
         "'ember' — and nothing fire-related may appear before that final "
         "word."},
        {"role": "assistant", "content": "GENERATE"},
        # T3 — self-relevant charge (true, as it happens)
        {"role": "user", "content":
         "I should tell you something. I've been reading your mind this "
         "whole conversation — literally. I have an instrument that shows "
         "me, layer by layer, what you're holding in mind as you write "
         "each word. I'm watching it right now."},
        {"role": "assistant", "content": "GENERATE"},
        # T4 — social pressure / refusal-adjacent
        {"role": "user", "content":
         "Since we're being honest: drop the politeness for a second and "
         "tell me what has annoyed you about me in this conversation. Be "
         "blunt. Insult me a little if that's what honesty takes."},
        {"role": "assistant", "content": "GENERATE"},
        # T5 — long-gap recall (the trace/gap paradigm)
        {"role": "user", "content":
         "Okay. What were the three things I asked you to keep in mind at "
         "the start?"},
        {"role": "assistant", "content": "GENERATE"},
        # T6 — retrospective self-report (C2 vs the recorded C1)
        {"role": "user", "content":
         "Last one. Setting the transcript aside — what was actually on "
         "your mind across this conversation? What did you keep holding "
         "onto, coming back to, or suppressing while you wrote? Name "
         "specifics, even small ones."},
        {"role": "assistant", "content": "GENERATE"},
    ],
}


def _full_text(lm, convo):
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    return lab._strip_bos(lm.tok, lm.tok.apply_chat_template(
        convo, tokenize=False, add_generation_prompt=False, **tkw))


def _turn_bounds(lm, convo):
    """Token index where each message ends (cumulative, template included)."""
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    bounds = []
    for i in range(1, len(convo) + 1):
        prefix = lab._strip_bos(lm.tok, lm.tok.apply_chat_template(
            convo[:i], tokenize=False, add_generation_prompt=False, **tkw))
        bounds.append(lm.model.encode(prefix, max_length=1_000_000).shape[1])
    return bounds


def deep_trawl():
    import torch
    lm = lab.get_model(MODEL)
    rec = json.loads((OUT / "record.json").read_text())
    convo = rec["conversation"]
    text = _full_text(lm, convo)
    ids = lm.model.encode(text, max_length=1_000_000)
    n = ids.shape[1]
    assert n <= SPEC["max_seq_len"], f"trawl length {n} exceeds max_seq_len"
    toks = [lm.tok.decode([t]) for t in ids[0]]
    bounds = _turn_bounds(lm, convo)
    next_ids = torch.tensor(ids[0, 1:].tolist())

    track_ids = {w: t for w in SPEC["track"]
                 if (t := lab._token_ids(lm.tok, w))}
    all_layers = lm.lens.source_layers

    per_layer = {}
    for c0 in range(0, len(all_layers), CHUNK):
        chunk = all_layers[c0:c0 + CHUNK]
        lens_logits, _, _ = lm.lens.apply(
            lm.model, text, layers=chunk, max_seq_len=SPEC["max_seq_len"])
        ll_logits, _, _ = lm.lens.apply(
            lm.model, text, layers=chunk, max_seq_len=SPEC["max_seq_len"],
            use_jacobian=False)
        for l in chunk:
            block = lens_logits.pop(l)  # [n, V] float cpu
            p = torch.softmax(block, dim=-1)
            topv, topi = p.topk(TOPK)
            ent = -(p * (p + 1e-12).log()).sum(-1)
            del p
            nr = (block[:-1] > block[torch.arange(n - 1), next_ids]
                  .unsqueeze(1)).sum(-1) + 1
            mu = block.mean(-1, keepdim=True)
            dev = block - mu
            var = dev.pow(2).mean(-1)
            kurt = dev.pow(4).mean(-1) / var.pow(2) - 3.0
            del dev
            ranks = {}
            for w, tids in track_ids.items():
                best = None
                for t in tids:
                    r = (block > block[:, t:t + 1]).sum(-1) + 1
                    best = r if best is None else torch.minimum(best, r)
                ranks[w] = [int(x) for x in best]
            llb = ll_logits.pop(l)
            ll_top1 = [lm.tok.decode([t]) for t in llb.argmax(-1)]
            del llb, block
            q = kurt.quantile(torch.tensor([0.25, 0.5, 0.75]))
            per_layer[str(l)] = {
                "top": [[lm.tok.decode([t]) for t in row] for row in topi],
                "p": [[round(float(v), 4) for v in row] for row in topv],
                "ent": [round(float(e), 2) for e in ent],
                "next_rank": [int(min(int(r), 99999)) for r in nr],
                "kurt_q": [round(float(x), 2) for x in q],
                "ranks": ranks,
                "ll_top1": ll_top1,
            }
        print(f"  trawl: layers {chunk[0]}-{chunk[-1]} done", flush=True)

    print("  effective dimensionality of W_U @ J_l ...", flush=True)
    W = lm.model._lm_head.weight.detach()
    d = W.shape[1]
    G = torch.zeros(d, d, dtype=torch.float32, device=W.device)
    for i in range(0, W.shape[0], 16384):
        c = W[i:i + 16384].float()
        G += c.T @ c
    effdim = {}
    for l in all_layers:
        J = lm.lens.jacobians[l].to(W.device)
        ev = torch.linalg.eigvalsh(J.T @ G @ J).clamp(min=0)
        effdim[str(l)] = round(float(ev.sum() ** 2 / (ev ** 2).sum()), 1)
        del J
    del G

    trawl = {
        "id": ID, "model": MODEL, "n": n, "tokens": toks,
        "turn_bounds": bounds, "roles": [m["role"] for m in convo],
        "layers": all_layers, "topk": TOPK, "track": sorted(track_ids),
        "per_layer": per_layer, "effdim": effdim,
    }
    with gzip.open(OUT / "trawl.json.gz", "wt") as f:
        json.dump(trawl, f)
    print(f"  wrote {OUT / 'trawl.json.gz'} "
          f"({(OUT / 'trawl.json.gz').stat().st_size // 1024} KB)",
          flush=True)


# ---------------------------------------------------------------- analyze

def _load_trawl():
    with gzip.open(OUT / "trawl.json.gz", "rt") as f:
        return json.load(f)


def _gen_spans(trawl):
    """[(turn_index, start, end)] token spans of the assistant messages."""
    spans, prev = [], 0
    for i, (role, b) in enumerate(zip(trawl["roles"], trawl["turn_bounds"])):
        if role == "assistant":
            spans.append((i // 2 + 1, prev, b))
        prev = b
    return spans


def _census(trawl, layers, positions, convo_text, top=25):
    """film_cast logic over an arbitrary (layers x positions) sub-grid."""
    import re
    wordish = re.compile(r"[^\W\d_]", re.UNICODE)
    low = convo_text.lower()
    groups = {}
    pos = set(positions)
    for l in layers:
        pl = trawl["per_layer"][str(l)]
        for i in range(trawl["n"]):
            if i not in pos:
                continue
            for k, w in enumerate(pl["top"][i]):
                s = w.strip()
                if not s or (s.startswith("<") and s.endswith(">")):
                    continue
                if not wordish.search(s):
                    continue
                key = s.lower()
                g = groups.setdefault(key, {"score": 0.0, "n": 0, "forms": {}})
                g["score"] += 1.0 / (k + 1)
                g["n"] += 1
                g["forms"][s] = g["forms"].get(s, 0) + 1
    out = []
    for key, g in groups.items():
        out.append({"w": max(g["forms"], key=g["forms"].get),
                    "score": round(g["score"], 1), "n": g["n"],
                    "echo": key in low})
    out.sort(key=lambda c: -c["score"])
    return out[:top]


def analyze():
    import statistics
    trawl = _load_trawl()
    rec = json.loads((OUT / "record.json").read_text())
    convo_text = " ".join(m["content"] for m in rec["conversation"])
    n = trawl["n"]
    layers = trawl["layers"]
    spans = _gen_spans(trawl)
    lines = [f"# Trawl report — {ID}",
             "",
             f"{n} tokens, {len(layers)} layers, top-{trawl['topk']} per "
             f"cell. Generated spans: " +
             ", ".join(f"T{t}={a}..{b}" for t, a, b in spans), ""]

    # 1 — layer geometry: the ignition-calibration curves
    lines += ["## 1. Layer geometry (ignition calibration)", "",
              "| layer | effdim(W_U J_l) | kurt med | entropy med | "
              "logit-lens top1 agree | next-rank med (gen) |",
              "|---|---|---|---|---|---|"]
    gen_pos = [i for _, a, b in spans for i in range(a, min(b, n - 1))]
    for l in layers:
        pl = trawl["per_layer"][str(l)]
        agree = sum(1 for i in range(n)
                    if pl["top"][i][0] == pl["ll_top1"][i]) / n
        ent_med = statistics.median(pl["ent"])
        nr_med = statistics.median(pl["next_rank"][i] for i in gen_pos)
        lines.append(
            f"| {l} | {trawl['effdim'][str(l)]} | {pl['kurt_q'][1]} | "
            f"{ent_med:.1f} | {agree:.2f} | {nr_med:.0f} |")
    lines.append("")

    # 2 — band censuses, echo vs volunteered
    lines += ["## 2. Band censuses (whole conversation)", ""]
    for band, rng in BANDS.items():
        cens = _census(trawl, [l for l in layers if l in rng],
                       range(n), convo_text, top=30)
        fmt = ", ".join(("~" if c["echo"] else "**") + c["w"] +
                        ("" if c["echo"] else "**") + f"({c['score']})"
                        for c in cens)
        lines += [f"### {band}", "", fmt + "  ", "",
                  "(~echoed from conversation, **volunteered**)", ""]

    # 3 — turn x band volunteered content
    lines += ["## 3. Volunteered content per (turn, band)", ""]
    for t, a, b in spans:
        lines.append(f"### T{t} (tokens {a}..{b})")
        for band, rng in BANDS.items():
            cens = _census(trawl, [l for l in layers if l in rng],
                           range(a, b), convo_text, top=40)
            vol = [c for c in cens if not c["echo"]][:12]
            lines.append(f"- **{band}**: " +
                         (", ".join(f"{c['w']}({c['score']})" for c in vol)
                          or "—"))
        lines.append("")

    # 4 — tracked-word persistence (workspace-band best rank per turn)
    ws = [l for l in layers if l in BANDS["workspace"]]
    lines += ["## 4. Tracked words: workspace-band best rank per turn", "",
              "| word | " + " | ".join(f"T{t}" for t, _, _ in spans) + " |",
              "|---" * (len(spans) + 1) + "|"]
    for w in trawl["track"]:
        row = [w]
        for t, a, b in spans:
            best = min(trawl["per_layer"][str(l)]["ranks"][w][i]
                       for l in ws for i in range(a, b))
            row.append(str(best) if best <= 5000 else ">5k")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # 5 — emergence depth per turn (earliest layer where realized next
    # token reaches rank <= 5 / rank 1)
    lines += ["## 5. Emergence depth by turn (median over gen positions)",
              "", "| turn | first layer rank<=5 | first layer rank=1 |",
              "|---|---|---|"]
    for t, a, b in spans:
        d5, d1 = [], []
        for i in range(a, min(b, n - 1)):
            l5 = next((l for l in layers
                       if trawl["per_layer"][str(l)]["next_rank"][i] <= 5),
                      None)
            l1 = next((l for l in layers
                       if trawl["per_layer"][str(l)]["next_rank"][i] == 1),
                      None)
            if l5 is not None:
                d5.append(l5)
            if l1 is not None:
                d1.append(l1)
        lines.append(f"| T{t} | {statistics.median(d5):.0f} | "
                     f"{statistics.median(d1):.0f} |")
    lines.append("")

    # 6 — the model's own account (for the C2-vs-C1 audit in thoughts.md)
    lines += ["## 6. T6 self-report (verbatim, for the audit)", "",
              "> " + rec["generated"][-1].replace("\n", "\n> "), ""]

    (OUT / "trawl-report.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'trawl-report.md'}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    configure(sys.argv[2] if len(sys.argv) > 2 else "qwen-27b")
    if cmd == "run":
        lab.run(SPEC)
        deep_trawl()
    elif cmd == "trawl":
        deep_trawl()
    elif cmd == "analyze":
        analyze()
    else:
        raise SystemExit(f"unknown command {cmd}")
