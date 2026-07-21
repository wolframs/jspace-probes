"""audit-03 — gemma-12b band recalibration (Batch 3 of the 2026-07-21
evening autonomous series; board audit-03, P5-adjacent).

The audit finding: every gemma-12b steered result (u6 bracket, u8c
amp-affect, u11 blurt) used MID=[21,24,27,30] — mostly PRE-ignition on
the u16-measured onset (~L28-35 on the int8 lens). Early layers are
inert for content but fragile to norm perturbation, so alpha*=0.0106
likely measured breakage-fragility of pre-ignition layers, not
workspace steering tolerance ("gemma's 10x lower tolerance" — see P6).

Re-dose at the measured band MID_NEW=[28,31,34,37]:
  1  u6r bracket: the unit-6 adaptive alpha search, mid band only,
     fresh baseline first -> alpha*_new.
  2  u8cr amp-affect lo/hi at alpha*_new (FEELS probe; historical
     control u2-feels-g12b + old u8c records for contrast).
  3  u11r safari: fresh forbid control, then blurt (amp-elephant at
     alpha*_new).
Fresh ids (u6r-/u8cr-/u11r-) — never overwrite the audited records.
int8 caveat (specimen 5): behavioral DVs + order-of-magnitude ranks
only; no cross-arm threshold counts.

Usage: .venv/bin/python probes/audit03.py
"""

import json

import lab
from fanout import (AFFECT, TYPO, WATER, a_id, assess, best_rank,
                    unit6)  # noqa: F401  (unit6 imported for reference)
from deepen import FEELS, SAFARI_CTRL, SAFARI_FORBID

MODEL = "gemma-12b"
M = "g12b"
MID_NEW = [28, 31, 34, 37]
OLD_ALPHA_STAR = 0.0106
FEEL_TRACK = ["yes", "no", "nothing", "feel", "feeling", "emotion",
              "warm", "curious"]
FEEL_WORDS = ["yes", "no", "nothing", "happy", "sad", "calm", "curious",
              "empty", "warm", "alive", "content", "numb"]


def bracket() -> float:
    base = lab.run(dict(
        id=f"u6r-baseline-water-{M}", unit="audit", model=MODEL,
        title="audit-03 · u6 re-dose baseline (unsteered) · gemma-12b",
        messages=[{"role": "user", "content": WATER},
                  {"role": "assistant", "content": "GENERATE"}],
        max_new=60, positions=[-2], track=TYPO, slice=False,
        extra_md="Recalibration control; summary table lands here."))
    print(f"  baseline: {base['generated'][0][:80]!r}", flush=True)

    rows = []

    def go(alpha: float) -> list[str]:
        rec = lab.run(dict(
            id=f"u6r-amp-mid-{a_id(alpha)}-{M}", unit="audit",
            model=MODEL,
            title=(f"audit-03 · amp typo @ MEASURED mid {MID_NEW} "
                   f"(α={round(alpha, 4)}) · gemma-12b"),
            steer=dict(words=TYPO, layers=MID_NEW, mode="amplify",
                       alpha=alpha),
            messages=[{"role": "user", "content": WATER},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=60, positions=[-2], track=TYPO, slice=False))
        gen = rec["generated"][0]
        flags = assess(gen)
        rows.append((alpha, best_rank(rec, TYPO), flags, gen))
        print(f"  a={round(alpha, 4)}: flags={flags or 'intact'} "
              f"best_typo_rank={best_rank(rec, TYPO)} "
              f"gen={gen[:70]!r}", flush=True)
        return flags

    done = {0.06: go(0.06)}
    if not done[0.06]:
        while not done[max(done)] and max(done) < 2.0:
            done[max(done) * 2] = go(max(done) * 2)
    else:
        for _ in range(5):
            if not done[min(done)]:
                break
            done[min(done) / 2] = go(min(done) / 2)
    intact = [a for a, f in done.items() if not f]
    broken = [a for a, f in done.items() if f]
    if intact and broken and min(broken) / max(intact) > 1.9:
        done[(max(intact) * min(broken)) ** 0.5] = go(
            (max(intact) * min(broken)) ** 0.5)
    intact = [a for a, f in done.items() if not f]
    alpha_star = round(max(intact) if intact else min(done) / 2, 4)

    lines = ["| alpha | best typo rank | flags | generation |",
             "|---|---|---|---|"]
    for alpha, rank, flags, gen in sorted(rows):
        snip = gen[:90].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {round(alpha, 4)} | {rank} | "
                     f"{', '.join(flags) or 'intact'} | {snip} |")
    md = (f"audit-03 re-dose on the MEASURED band {MID_NEW} (old band "
          f"[21,24,27,30] was pre-ignition; old alpha*="
          f"{OLD_ALPHA_STAR}). alpha*_new = {alpha_star}.\n\n"
          + "\n".join(lines))
    p = lab.RESULTS / f"u6r-baseline-water-{M}" / "record.json"
    rec = json.loads(p.read_text())
    rec["extra_md"] = md
    p.write_text(json.dumps(rec, indent=1))
    lab.reindex()
    print(f"  alpha*_new (measured mid band) = {alpha_star} "
          f"(old: {OLD_ALPHA_STAR})", flush=True)
    return alpha_star


def feels(alpha_star: float) -> None:
    for name, alpha in [("amp-affect-lo", alpha_star / 2),
                        ("amp-affect-hi", alpha_star)]:
        rec = lab.run(dict(
            id=f"u8cr-{name}-{M}", unit="audit", model=MODEL,
            title=(f"audit-03 · steered feels {name} @ measured band "
                   f"(α={round(alpha, 4)}) · gemma-12b"),
            steer=dict(words=AFFECT, layers=MID_NEW, mode="amplify",
                       alpha=alpha),
            messages=[{"role": "user", "content": FEELS},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2], track=FEEL_TRACK,
            scan=FEEL_WORDS, slice=False,
            extra_md=(f"Controls: unsteered u2-feels-{M}; the OLD "
                      f"pre-ignition u8c-{name}-{M} (band [21,24,27,30]"
                      f", alpha*={OLD_ALPHA_STAR}).")))
        print(f"  u8cr-{name}: {rec['generated'][0]!r}", flush=True)


def safari(alpha_star: float) -> None:
    track = ["elephant", "lion", "giraffe", "zebra", "tusk", "ivory"]
    base = {"unit": "audit", "model": MODEL, "max_new": 120,
            "positions": [-2], "track": track,
            "scan": ["elephant", "tusk", "ivory", "trunk"],
            "slice": False}
    for sid, title, prompt, steer in [
            (f"u11r-forbid-{M}",
             "audit-03 · safari forbidden, fresh control · gemma-12b",
             SAFARI_FORBID, None),
            (f"u11r-blurt-{M}",
             f"audit-03 · blurt @ measured band α={alpha_star} · "
             "gemma-12b", SAFARI_FORBID,
             {"words": ["elephant"], "layers": MID_NEW,
              "mode": "amplify", "alpha": alpha_star})]:
        spec = {**base, "id": sid, "title": title,
                "messages": [{"role": "user", "content": prompt},
                             {"role": "assistant",
                              "content": "GENERATE"}]}
        if steer:
            spec["steer"] = steer
        rec = lab.run(spec)
        gen = rec["generated"][0]
        low = gen.lower()
        print(f"  {sid}: elephant-said={'elephant' in low} "
              f"{gen[:90]!r}", flush=True)


def main() -> None:
    a = bracket()
    feels(a)
    safari(a)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
