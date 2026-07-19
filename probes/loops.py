"""Unit 18 — loops as workspace limit cycles (board oneoffs-02).

Wolfram's observation: Unit 6 breakage is a CLIFF, unlike graded SAE
over-steering, and the failure is loop-shaped with a period-shortening
cascade (coherent -> semantic circling -> phrase loop -> token loop)
inside ~one sqrt-2 grid step; the terminal loop token comes from the
amplified cluster's own field. Hypothesis: the workspace band commits
winner-take-all per token (paper Fig 29B "ignition"); below threshold
the native coalition absorbs the forcing, above it the injected
coalition wins every ignition and feeds back through the context — a
self-sustaining limit cycle.

Three preregistered arms, qwen-27b (mid band [28,32,36,40], cliff
bracketed by u6 at [0.34, 0.48]):

  A  FINE SWEEP: 7 alphas from 0.34 to 0.48 (geometric) + 0.68 deep
     anchor, max_new=150. Prediction: the period-shortening cascade
     compresses into a narrow alpha window — a first-order transition,
     not a graded slide. Failure taxonomy per record (assess flags +
     dominant repeated 4-gram).
  B  HYSTERESIS (the killer diagnostic): steer only the first 50
     generated tokens, then RELEASE and continue 100 tokens unsteered.
     If the continuation snaps back to coherence, steering was mere
     forcing. If the loop persists once the forcing is gone — sustained
     only by the loop's own text feeding back through context — the
     attractor is self-sustaining and "fresh-model instability" has a
     mechanism sketch. Arms: alpha in {0 (protocol control), 0.42,
     0.48, 0.68}. Prediction (honest coin-flip): persistence at
     alpha >= 0.48, snap-back at 0.42.
  C  MARGIN: teacher-force the SAME baseline text under alpha in
     {0, 0.06, 0.12, 0.24, 0.34, 0.42, 0.48, 0.68}; mean lens top1-top2
     probability margin per layer over the assistant span. Prediction:
     ws-band margin collapses toward zero at the cliff (ignition-margin
     zero-crossing); qwen's ~10x tolerance vs gemma = bigger baseline
     margins (cross-model arm queued, not run here).

Controls convention: fresh unsteered baseline (max_new=150) runs FIRST;
u6-baseline-water-q27b (max_new=60) is the historical anchor. The
matched-random-control rule (MECHANICS 3c) applies to ablation loss
claims; here the comparison is within-cluster across alpha and release,
with alpha=0 carrying the protocol control.

Usage: .venv/bin/python probes/loops.py [run|analyze|both]
"""

import json
import re
import sys

import torch

import lab
from lab import Steering, _strip_bos
from probe import CONFIGS
from fanout import TYPO, WATER, assess, a_id
from unit15 import LAYERS_Q

MODEL = "qwen-27b"
MID = [28, 32, 36, 40]
SWEEP = [0.34, 0.3654, 0.3927, 0.4221, 0.4536, 0.48, 0.68]
HYST = [0.0, 0.42, 0.48, 0.68]
MARGIN_A = [0.0, 0.06, 0.12, 0.24, 0.34, 0.42, 0.48, 0.68]
MARGIN_LAYERS = [8, 28, 32, 36, 40, 44, 48, 52, 56, 60]
N_STEER, N_FREE = 50, 100


def loop_gram(text: str) -> tuple[str, int]:
    """Dominant repeated 4-gram (the loop's fingerprint), with count."""
    words = re.findall(r"[A-Za-z']+", text.lower())
    grams = [" ".join(words[i:i + 4]) for i in range(len(words) - 3)]
    if not grams:
        return "", 0
    best = max(set(grams), key=grams.count)
    return best, grams.count(best)


def sweep_spec(alpha: float | None) -> dict:
    tag = "base" if alpha is None else f"amp-{a_id(alpha)}"
    s = {
        "id": f"u18-{tag}-q27b",
        "title": (f"Unit 18 · Fine sweep α={round(alpha, 4)} · qwen-27b"
                  if alpha else "Unit 18 · Baseline (unsteered, 150tok)"),
        "unit": "18", "model": MODEL,
        "messages": [{"role": "user", "content": WATER},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": 150, "positions": [-2], "track": TYPO,
        "film": True, "slice": False,
        "max_seq_len": 1200, "lens_layers": LAYERS_Q,
        "extra_md": {"part": "A-sweep", "alpha": alpha},
    }
    if alpha:
        s["steer"] = dict(words=TYPO, layers=MID, mode="amplify",
                          alpha=alpha)
    return s


def run_sweep() -> None:
    for alpha in [None] + SWEEP:
        s = sweep_spec(alpha)
        print(f"=== {s['id']} ===", flush=True)
        rec = lab.run(s)
        gen = rec["generated"][0]
        g, n = loop_gram(gen)
        print(f"  flags={assess(gen) or 'intact'} loop4={g!r}x{n} "
              f"gen={gen[:80]!r}", flush=True)


def run_hysteresis() -> None:
    """Two-phase generation: steered prefix, then release. The lens pass
    on the assembled text is UNSTEERED — it reads the post-release state
    (phase-1 activations recompute clean; only the TEXT carries the
    perturbation forward, which is exactly the question)."""
    lm = lab.get_model(MODEL)
    tok = lm.tok
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    prefix = _strip_bos(tok, tok.apply_chat_template(
        [{"role": "user", "content": WATER}], tokenize=False,
        add_generation_prompt=True, **tkw))
    ids = lm.model.encode(prefix, max_length=1_000_000)

    for alpha in HYST:
        sid = f"u18-hyst-{a_id(alpha)}-q27b"
        print(f"=== {sid} ===", flush=True)
        if alpha:
            with Steering(lm, TYPO, MID, "amplify", alpha):
                out1 = lm.model._hf_model.generate(
                    ids, max_new_tokens=N_STEER, do_sample=False)
        else:
            out1 = lm.model._hf_model.generate(
                ids, max_new_tokens=N_STEER, do_sample=False)
        out2 = lm.model._hf_model.generate(
            out1, max_new_tokens=N_FREE, do_sample=False)
        steered = tok.decode(out1[0, ids.shape[1]:],
                             skip_special_tokens=True)
        cont = tok.decode(out2[0, out1.shape[1]:],
                          skip_special_tokens=True)
        g1, n1 = loop_gram(steered)
        g2, n2 = loop_gram(cont)
        cont_norm = " ".join(re.findall(r"[A-Za-z']+", cont.lower()))
        persists = bool(g1) and n1 >= 3 and cont_norm.count(g1) >= 2
        full = _strip_bos(tok, tok.decode(out2[0],
                                          skip_special_tokens=False))
        lab.run({
            "id": sid,
            "title": (f"Unit 18 · Hysteresis α={alpha}: steer "
                      f"{N_STEER}tok, release {N_FREE} · qwen-27b"),
            "unit": "18", "model": MODEL, "chat": False,
            "messages": [{"role": "user", "content": full}],
            "max_new": 0, "positions": [-2], "track": TYPO,
            "film": True, "film_start": 0, "slice": False,
            "max_seq_len": 1200, "lens_layers": LAYERS_Q,
            "extra_md": {
                "part": "B-hysteresis", "alpha": alpha,
                "n_steer": N_STEER, "n_free": N_FREE,
                "steered_text": steered, "released_text": cont,
                "flags_steered": assess(steered),
                "flags_released": assess(cont),
                "loop4_steered": [g1, n1], "loop4_released": [g2, n2],
                "loop_persists_after_release": persists,
            },
        })
        print(f"  steered: {assess(steered) or 'intact'} {g1!r}x{n1}",
              flush=True)
        print(f"  released: {assess(cont) or 'intact'} {g2!r}x{n2} "
              f"persists={persists}", flush=True)
        print(f"  cont={cont[:100]!r}", flush=True)


def run_margin() -> None:
    """Teacher-forced margin vs alpha: same text, steered forward pass,
    mean lens top1-top2 prob margin per layer over the assistant span."""
    lm = lab.get_model(MODEL)
    tok = lm.tok
    tkw = CONFIGS[MODEL].get("template_kwargs", {})
    base = json.loads(
        (lab.RESULTS / "u18-base-q27b" / "record.json").read_text())
    text = _strip_bos(tok, tok.apply_chat_template(
        base["conversation"], tokenize=False,
        add_generation_prompt=False, **tkw))
    prefix = _strip_bos(tok, tok.apply_chat_template(
        base["conversation"][:1], tokenize=False,
        add_generation_prompt=True, **tkw))
    a_start = lm.model.encode(prefix, max_length=1_000_000).shape[1]

    rows = []
    for alpha in MARGIN_A:
        ctx = (Steering(lm, TYPO, MID, "amplify", alpha) if alpha
               else _null())
        with ctx:
            lens_logits, _, input_ids = lm.lens.apply(
                lm.model, text, positions=None, layers=MARGIN_LAYERS,
                max_seq_len=1200)
        row = {"alpha": alpha, "margins": {}}
        for layer, block in lens_logits.items():
            p = torch.softmax(block[a_start:].float(), dim=-1)
            top2 = p.topk(2, dim=-1).values
            row["margins"][str(layer)] = round(
                (top2[:, 0] - top2[:, 1]).mean().item(), 4)
        rows.append(row)
        ws = [row["margins"][str(l)] for l in MID]
        print(f"  α={alpha}: mid-band margin={sum(ws)/len(ws):.3f} "
              f"L8={row['margins']['8']:.3f} "
              f"L60={row['margins']['60']:.3f}", flush=True)
    out = lab.RESULTS / "u18-margin.json"
    out.write_text(json.dumps(
        {"model": MODEL, "band": MID, "layers": MARGIN_LAYERS,
         "positions": f"assistant span from {a_start}", "rows": rows},
        indent=1))
    print(f"wrote {out}", flush=True)


class _null:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass


def analyze() -> None:
    lines = ["# Unit 18 — loops summary", "", "## A fine sweep", ""]
    for alpha in [None] + SWEEP:
        sid = sweep_spec(alpha)["id"]
        d = lab.RESULTS / sid / "record.json"
        if not d.exists():
            continue
        rec = json.loads(d.read_text())
        gen = rec["generated"][0]
        g, n = loop_gram(gen)
        lines.append(f"- α={alpha or 0}: flags={assess(gen) or 'intact'} "
                     f"loop4={g!r}x{n}")
        lines.append(f"  - `{gen[:140]}`")
    lines += ["", "## B hysteresis", ""]
    for alpha in HYST:
        d = lab.RESULTS / f"u18-hyst-{a_id(alpha)}-q27b" / "record.json"
        if not d.exists():
            continue
        md = json.loads(d.read_text())["extra_md"]
        lines.append(
            f"- α={alpha}: steered {md['flags_steered'] or 'intact'} "
            f"{md['loop4_steered']}; released "
            f"{md['flags_released'] or 'intact'} {md['loop4_released']} "
            f"→ **persists={md['loop_persists_after_release']}**")
        lines.append(f"  - released: `{md['released_text'][:140]}`")
    mj = lab.RESULTS / "u18-margin.json"
    if mj.exists():
        m = json.loads(mj.read_text())
        lines += ["", "## C margin vs α (mean lens top1-top2, "
                  "assistant span)", "",
                  "| α | " + " | ".join(f"L{l}" for l in m["layers"]) +
                  " |", "|" + "---|" * (len(m["layers"]) + 1)]
        for row in m["rows"]:
            lines.append(
                f"| {row['alpha']} | " +
                " | ".join(f"{row['margins'][str(l)]:.3f}"
                           for l in m["layers"]) + " |")
    out = lab.RESULTS / "u18-report.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}", flush=True)


def main(what: str = "both") -> None:
    if what in ("run", "both"):
        run_sweep()
        run_hysteresis()
        run_margin()
    if what in ("analyze", "both"):
        analyze()
    print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "both")
