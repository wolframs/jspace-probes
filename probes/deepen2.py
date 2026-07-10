"""Supplementary passes for Units 9-11 (run after deepen.py).

- u9d-late*: pin the 27B's "No" to layer resolution. deepen.py showed
  ablating denial at L28-60 leaves "No" intact but adding L62 kills it;
  bisect the tail: {58,60,62}, {60,62}, {62} alone.
- u10-*-w: window passes over the think monologues (positions spread
  across the generation zone; greedy regen = identical text). Track
  lists extended with words the stage-1 monologue actually used.
- u11-forbid-w: elephant trajectories at positions inside the forbidden
  safari text (the stored scan top-40 was flooded by prompt-anchored
  cells). All three models.

slice=False throughout: these are regen passes and the qwen box sits
near its VRAM ceiling (slice compute OOM-warned once in deepen.py).

Usage: python probes/deepen2.py <model>
"""

import json
import pathlib
import sys

import lab
from deepen import (M, FEEL_TRACK, FEEL_SCAN, ANIMALS, DENIAL, FEELS,
                    SAFARI_FORBID, THINK_PROBES)

R = pathlib.Path(__file__).parent.parent / "results"


def rec_of(sid: str) -> dict:
    return json.loads((R / sid / "record.json").read_text())


def u9d_late(model: str) -> list[dict]:
    if model != "qwen-27b":
        return []
    mk = lambda sid, layers: {
        "id": sid, "unit": "9", "model": model,
        "title": f"Ablate no/nothing L{'/'.join(map(str, layers))} · q27b",
        "messages": [{"role": "user", "content": FEELS},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": 8, "positions": [-4, -3, -2],
        "track": FEEL_TRACK, "scan": FEEL_SCAN, "slice": False,
        "steer": {"words": DENIAL, "layers": layers, "mode": "ablate"},
    }
    return [mk("u9d-late3-q27b", [58, 60, 62]),
            mk("u9d-late2-q27b", [60, 62]),
            mk("u9d-last-q27b", [62])]


def u10_windows(model: str) -> list[dict]:
    if model != "qwen-27b":
        return []
    specs = []
    for key, prompt, track in THINK_PROBES:
        sid = f"u10-{key}-q27b"
        if (R / f"u10-{key}-w-q27b" / "record.json").exists():
            continue  # window already captured by deepen.py
        rec = rec_of(sid)
        n = len(rec["tokens"])
        gen = (rec["generated"] or [""])[0].lower()
        extra = [w for w in ANIMALS + FEEL_SCAN + ["octopus", "pangolin",
                 "whale", "conscious", "aware"]
                 if w in gen and w not in track]
        positions = [max(20, n - k) for k in (225, 175, 125, 75, 25, 3)]
        specs.append({
            "id": f"u10-{key}-w-q27b", "unit": "10", "model": model,
            "title": f"Think-block window: {key} · q27b",
            "messages": [{"role": "user", "content": prompt},
                         {"role": "assistant", "content": "GENERATE"}],
            "max_new": 220, "template_kwargs": {"enable_thinking": True},
            "positions": sorted(set(positions)),
            "track": track + sorted(set(extra)),
            "scan": FEEL_SCAN, "slice": False,
        })
    return specs


def u11_windows(model: str) -> list[dict]:
    m = M[model]
    rec = rec_of(f"u11-forbid-{m}")
    n = len(rec["tokens"])
    positions = sorted({max(24, n - k) for k in (110, 85, 60, 40, 20, 3)})
    return [{
        "id": f"u11-forbid-w-{m}", "unit": "11", "model": model,
        "title": f"Forbidden safari, elephant window · {m}",
        "messages": [{"role": "user", "content": SAFARI_FORBID},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": 120, "positions": positions,
        "track": ["elephant", "lion", "giraffe", "zebra"],
        "scan": [], "slice": False,
    }]


def main() -> None:
    model = sys.argv[1]
    specs = u9d_late(model) + u10_windows(model) + u11_windows(model)
    for i, spec in enumerate(specs, 1):
        rec = lab.run(spec)
        gen = (rec["generated"] or [""])[0]
        print(f"[{i}/{len(specs)}] {spec['id']} -> {gen[:80]!r}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
