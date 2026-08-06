"""affect-08 slice — re-elicit gemma-12b's `desperate` vector.

The g12b desperate direction has split-half reliability 0.23 (flagged in
affect-06's design note and again in the langval postmortem) — the
weakest instrument in the affect battery, and the one the g12b escape
results lean on. This slice doubles its story count (12 -> 24: the 3
arms x 4 fresh seeds) and rebuilds the affect-01 artifacts.

Honesty notes:
  - The rebuild shifts every emotion's vector slightly (grand mean moves
    and desperate is upweighted 24-vs-12 inside it). validation.json and
    vectors.pt are regenerated; stories.json carries a dated note. Old
    downstream numbers cite the old instrument — do not silently re-read
    them through the new one.
  - Before/after is computed with the SAME estimator (seeded half-split
    of desperate rows vs grand mean, per layer): "before" on the original
    12 rows, "after" on all 24. n=12 halves are 6-story means; noisy —
    the report gives the workspace-band mean and the full curve.

Usage:  .venv/bin/python probes/affect08s.py        # GPU, resumable
Artifacts: results/affect08s-g12b/report.md + delta.json; updates
results/affect01-gemma-12b/{stories.json, means.pt, vectors.pt,
validation.json} via affect.build + affect.report.
"""

import json

import torch

import affect
from affect import ARMS, TOPICS, _gen, _mean_resid, _unit, outdir, SKIP
from lab import RESULTS, get_model

MODEL = "gemma-12b"
EMO = "desperate"
NEW_SEEDS = [55, 66, 77, 88]
WS_BAND = list(range(28, 44))          # audit-03 measured band, wide
OUT = RESULTS / "affect08s-g12b"
NOTE = "affect-08 slice 2026-08-06: +12 desperate stories (seeds 55-88)"


def elicit_more() -> None:
    d = outdir(MODEL)
    meta = json.loads((d / "stories.json").read_text())
    if any(s.get("re_elicit") for s in meta["stories"]):
        print("skip elicit (re-elicit stories already present)",
              flush=True)
        return
    lm = get_model(MODEL)
    means = torch.load(d / "means.pt")
    added = 0
    for ai, (arm, tpl) in enumerate(ARMS.items()):
        for si, seed in enumerate(NEW_SEEDS):
            topic = TOPICS[(ai * len(NEW_SEEDS) + si) % len(TOPICS)]
            prompt = tpl.format(emo=EMO, topic=topic)
            ids, (n0, end), text = _gen(lm, prompt, seed)
            n_story = end - n0
            if n_story < 30:
                print(f"  SHORT ({n_story} tok) {arm}/s{seed}", flush=True)
            lo = n0 + min(SKIP, max(0, n_story - 60))
            means = torch.cat([means, _mean_resid(lm, ids, (lo, end))
                               .unsqueeze(0)])
            meta["stories"].append({
                "kind": "emotion", "emotion": EMO, "arm": arm,
                "seed": seed, "prompt": prompt, "text": text,
                "n_story_tokens": n_story, "pooled_from": lo - n0,
                "re_elicit": NOTE})
            added += 1
            print(f"  [{added}/12] {arm}/s{seed}: {n_story} tok",
                  flush=True)
    meta.setdefault("notes", []).append(NOTE)
    (d / "stories.json").write_text(json.dumps(meta, indent=1))
    torch.save(means, d / "means.pt")
    print(f"ELICIT DONE: +{added} stories -> {d}", flush=True)


def _split_half(means: torch.Tensor, rows: list[int],
                grand: torch.Tensor, seed: int) -> torch.Tensor:
    """Per-layer cosine between half-split desperate means (vs grand)."""
    g = torch.Generator().manual_seed(seed)
    perm = torch.randperm(len(rows), generator=g).tolist()
    h1 = means[[rows[i] for i in perm[:len(rows) // 2]]].mean(0)
    h2 = means[[rows[i] for i in perm[len(rows) // 2:]]].mean(0)
    return (_unit(h1 - grand) * _unit(h2 - grand)).sum(-1)


def delta() -> None:
    d = outdir(MODEL)
    meta = json.loads((d / "stories.json").read_text())
    idx = meta["stories"]
    means = torch.load(d / "means.pt").float()
    emos = list(affect.EMOTIONS)
    U = torch.stack([means[[i for i, s in enumerate(idx)
                            if s["emotion"] == e]].mean(0)
                     for e in emos])
    grand = U.mean(0)

    old = [i for i, s in enumerate(idx)
           if s["emotion"] == EMO and not s.get("re_elicit")]
    all_ = [i for i, s in enumerate(idx) if s["emotion"] == EMO]
    # average over several split seeds — n=12 halves are noisy
    seeds = range(7, 27)
    before = torch.stack([_split_half(means, old, grand, s)
                          for s in seeds]).mean(0)
    after = torch.stack([_split_half(means, all_, grand, s)
                         for s in seeds]).mean(0)

    OUT.mkdir(exist_ok=True)
    bw = before[WS_BAND].mean().item()
    aw = after[WS_BAND].mean().item()
    (OUT / "delta.json").write_text(json.dumps({
        "model": MODEL, "emotion": EMO, "note": NOTE,
        "n_old": len(old), "n_all": len(all_),
        "ws_band": WS_BAND, "split_seeds": list(seeds),
        "before_ws_mean": round(bw, 4), "after_ws_mean": round(aw, 4),
        "before_curve": [round(x, 4) for x in before.tolist()],
        "after_curve": [round(x, 4) for x in after.tolist()]}, indent=1))
    L = [f"# affect-08 slice · {MODEL} `{EMO}` re-elicit\n",
         f"{NOTE}. Split-half (desperate-vs-grand direction, mean over "
         f"{len(list(seeds))} seeded splits):\n",
         f"- workspace band L28-43 mean: **{bw:.3f} -> {aw:.3f}** "
         f"(n={len(old)} -> {len(all_)} stories)",
         "- per-layer curves in delta.json; instrument artifacts "
         "rebuilt via affect.build (vectors.pt, validation.json).\n"]
    (OUT / "report.md").write_text("\n".join(L))
    print(f"split-half ws-band: before={bw:.3f} after={aw:.3f}",
          flush=True)


if __name__ == "__main__":
    elicit_more()
    affect.build(MODEL)
    affect.report(MODEL)
    delta()
