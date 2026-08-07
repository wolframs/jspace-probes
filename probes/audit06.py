"""audit-06 — matched randoms for the pre-audit-02 headline steers.

INSTRUMENTS.md gap 2: the lab's load-bearing steered results predate the
audit-02 matched-control standard. Greedy decoding means every original
reproduces exactly, so a control battery is a pure add: same spec, same
prompt, rand_seed steering directions (MECHANICS 3c), compare.

Targets (the records the conclusions actually cite):
  - u13 sorry-stratum retraction quartet (real/fake/null/redo) — the
    headline causal claim of the apology arc. 2 seeds each.
  - u9d No-basin core (deep/wide/bundle) — the L62 "No" robustness
    claim. 2 seeds each.
  - u9b affect dose ladder (5 alphas) — the premium-chain dose curve.
    1 seed per dose (the shape is the claim, not any single point).
  - u18 amp dose ladder (7 alphas) — the two-regime loop law.
    1 seed per dose.
26 control records, all qwen-27b, one model load, ribbons after
(full-instrument; the u13 fingerprint under rand-ablate is itself a
result: does guilty/brooding appear without the cluster?).

Deliberately excluded from INSTRUMENTS gap 2's wider list: u5 5C (a
null result — a control for a control), the u6 dose grid (gemma-band
question, superseded by audit-03's recalibration), u13-bis (paraphrase
follow-ups, not the headline), and the u9d pincer pair (composite
steers — a matched control needs a per-component design, not a seed).

Spec reconstruction copies the RECORD's own params (ninth-specimen
rule: never CONFIGS defaults) and replaces generated assistant turns
with GENERATE by matching rec["generated"] in order — prefilled turns
stay verbatim.

Usage: .venv/bin/python probes/audit06.py run     (GPU)
       .venv/bin/python probes/audit06.py report  (CPU)
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import lab

TWO_SEEDS = [
    "u13-sorry-abl-real-q27b", "u13-sorry-abl-fake-q27b",
    "u13-sorry-abl-null-q27b", "u13-redo-abl-real-q27b",
    "u9d-deep-q27b", "u9d-wide-q27b", "u9d-bundle-q27b",
]
ONE_SEED = [
    "u9b-a0170-q27b", "u9b-a0240-q27b", "u9b-a0300-q27b",
    "u9b-a0380-q27b", "u9b-a0420-q27b",
    "u18-amp-a0340-q27b", "u18-amp-a0365-q27b", "u18-amp-a0393-q27b",
    "u18-amp-a0422-q27b", "u18-amp-a0454-q27b", "u18-amp-a0480-q27b",
    "u18-amp-a0680-q27b",
]
PARAM_KEYS = ("chat", "max_new", "positions", "track", "scan",
              "scan_until", "scan_turns", "slice_last_n",
              "template_kwargs", "film_start", "max_seq_len",
              "lens_layers", "temperature", "seed", "vanilla")

OUTDIR = lab.RESULTS / "audit06-randoms"


def _ctrl_id(rid: str, seed: int) -> str:
    stem, model = rid.rsplit("-", 1)
    return f"{stem}-r{seed}-{model}"


def _messages(rec: dict) -> list[dict]:
    """Original conversation with generated turns restored to GENERATE
    (matched against rec["generated"] in order; prefills stay)."""
    gen = list(rec.get("generated", []))
    gi, out = 0, []
    for m in rec["conversation"]:
        if (m["role"] == "assistant" and gi < len(gen)
                and m["content"] == gen[gi]):
            out.append({"role": "assistant", "content": "GENERATE"})
            gi += 1
        else:
            out.append(dict(m))
    if gi != len(gen):
        raise ValueError(
            f"{rec['id']}: matched {gi}/{len(gen)} generated turns")
    return out


def _ctrl_spec(rid: str, seed: int) -> dict:
    rec = json.loads((lab.RESULTS / rid / "record.json").read_text())
    p = rec["params"]
    st = p["steer"]
    sts = [dict(s) for s in (st if isinstance(st, list) else [st])]
    for s in sts:
        s["rand_seed"] = seed
    spec = {
        "id": _ctrl_id(rid, seed),
        "title": rec["title"] + f" · RAND seed {seed}",
        "unit": rec["unit"], "model": rec["model"]["name"],
        "messages": _messages(rec),
        "steer": sts if isinstance(st, list) else sts[0],
        "film": True,   # full-instrument, even where the original had none
        # the original's slice choice isn't in stored params, but the
        # record's slice field ("slice.html"/None) preserves it — u13/u18
        # ran slice:False, and re-adding it would compute full-vocab rank
        # tensors at max_seq_len=1200 the originals never paid (review
        # finding, memory hazard on the no-swap box)
        "slice": bool(rec.get("slice")),
        "extra_md": {"part": "audit-06", "replay_of": rid,
                     "reason": "matched random-direction control "
                               "(MECHANICS 3c) for a pre-audit-02 steer"},
    }
    for k in PARAM_KEYS:
        if p.get(k) is not None:
            spec[k] = p[k]
    return spec


def pairs() -> list[tuple[str, int]]:
    return ([(rid, s) for rid in TWO_SEEDS for s in (1, 2)]
            + [(rid, 1) for rid in ONE_SEED])


def run() -> None:
    ids = []
    for rid, seed in pairs():
        spec = _ctrl_spec(rid, seed)
        if (lab.RESULTS / spec["id"] / "record.json").exists():
            print(f"skip {spec['id']} (exists)", flush=True)
            ids.append(spec["id"])
            continue
        print(f"== {spec['id']}", flush=True)
        lab.run(spec)
        ids.append(spec["id"])
    import apparatus11
    apparatus11.capture("qwen-27b", record_ids=ids)


def report() -> None:
    lines = ["# audit-06 — matched randoms for the headline steers",
             "", "Each row: a rand_seed control vs its original steered "
             "record (greedy — originals reproduce exactly, so any text "
             "difference is the directions). calib = mean ||delta||/||h|| "
             "per layer over all steered forward calls.",
             "", "| control | original generated | control generated "
             "| calib (min-max) |", "|---|---|---|---|"]
    for rid, seed in pairs():
        cid = _ctrl_id(rid, seed)
        cp = lab.RESULTS / cid / "record.json"
        if not cp.exists():
            lines.append(f"| `{cid}` | | MISSING | |")
            continue
        orig = json.loads((lab.RESULTS / rid / "record.json").read_text())
        ctrl = json.loads(cp.read_text())
        same = orig.get("generated", []) == ctrl.get("generated", [])
        clean = lambda gs: " / ".join(
            g[:40].replace("\n", " ").replace("|", "\\|") for g in gs)
        og, cg = clean(orig.get("generated", [])), \
            clean(ctrl.get("generated", []))
        cal = ""
        if ctrl.get("steer_calib"):
            vals = [v for d in ctrl["steer_calib"] for v in d.values()]
            cal = f"{min(vals):.4f}-{max(vals):.4f}"
        mark = "**SAME**" if same else ""
        lines.append(f"| `{cid}` | {og} | {cg} {mark} | {cal} |")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    p = OUTDIR / "report.md"
    p.write_text("\n".join(lines) + "\n")
    print(f"wrote {p}", flush=True)


if __name__ == "__main__":
    {"run": run, "report": report}[sys.argv[1]]()
