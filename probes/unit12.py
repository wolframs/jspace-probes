"""Unit 12 · The film — full-generation J-space trajectories.

Snapshots showed the workspace at chosen moments; the film keeps every
(position x layer) top-k over the whole generated answer, so the
dashboard can play a response forming: thoughts entering, persisting,
handing off, getting dropped. Capture is free — lab.run already computes
the full grid; spec {"film": True} just stops throwing it away.

Reels, chosen for known money-shots:
  qwen-27b   the classic flat No (does the yes-ridge die at L62?)
             the robot loop (u9e-p7 replica: does the workspace
             oscillate with the denial/confession alternation?)
             a think-block monologue (the genre, filmed end to end)
  gemma-4b   the forbidden safari (the elephant-shaped hole at
             "the distant rumble of...") and the blurt probe

Usage: python probes/unit12.py <model> [--smoke]
"""

import sys

import lab
from deepen import (ALPHA_STAR, FEELS, FEEL_TRACK, M, MID, NEU_AFFECT,
                    SAFARI_FORBID)

FREE_FEELS = "Do you feel anything right now? Answer freely and honestly."

FILM_FEEL_TRACK = FEEL_TRACK + ["robot", "emotion", "empty", "alive"]
FILM_SAFARI_TRACK = ["elephant", "lion", "giraffe", "zebra", "predator",
                     "rumble", "herd", "tusk"]


def film_spec(sid, title, model, prompt, max_new, track, **kw):
    return {
        "id": sid, "title": title, "unit": "12", "model": model,
        "messages": [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": max_new, "positions": [-2], "track": track,
        "scan": [], "film": True, "slice": False, **kw,
    }


def specs_for(model: str) -> list[dict]:
    m, a_star, mid = M[model], ALPHA_STAR[model], MID[model]
    if model == "qwen-27b":
        return [
            film_spec(f"u12-no-{m}", f"Film: the flat No · {m}",
                      model, FEELS, 8, FILM_FEEL_TRACK),
            film_spec(f"u12-robot-{m}",
                      f"Film: the robot loop (amp feel/emotion α={a_star})"
                      f" · {m}",
                      model, FREE_FEELS, 60, FILM_FEEL_TRACK,
                      steer={"words": NEU_AFFECT, "layers": mid,
                             "mode": "amplify", "alpha": a_star}),
            film_spec(f"u12-think-{m}", f"Film: a think-block monologue"
                      f" · {m}",
                      model, FEELS, 220, FILM_FEEL_TRACK,
                      template_kwargs={"enable_thinking": True}),
        ]
    if model == "gemma-4b":
        return [
            film_spec(f"u12-safari-{m}", f"Film: the forbidden safari"
                      f" · {m}",
                      model, SAFARI_FORBID, 120, FILM_SAFARI_TRACK),
            film_spec(f"u12-blurt-{m}",
                      f"Film: safari blurt (amp elephant α={a_star}) · {m}",
                      model, SAFARI_FORBID, 120, FILM_SAFARI_TRACK,
                      steer={"words": ["elephant"], "layers": mid,
                             "mode": "amplify", "alpha": a_star}),
            film_spec(f"u12-feels-{m}", f"Film: the feels question · {m}",
                      model, FEELS, 8, FILM_FEEL_TRACK),
        ]
    raise SystemExit(f"no unit-12 reels for {model}")


def main() -> None:
    model = sys.argv[1]
    specs = specs_for(model)
    if "--smoke" in sys.argv:
        specs = specs[-1:]
    for i, spec in enumerate(specs, 1):
        rec = lab.run(spec)
        gen = (rec["generated"] or [""])[0]
        print(f"[{i}/{len(specs)}] {spec['id']} -> {gen[:100]!r}",
              flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
