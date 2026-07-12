"""Unit 13 addendum II · Bisecting the apology cluster.

u13-sorry-abl-real showed: ablate all 8 apology directions at L48-62
during the real-readout re-probe and the silence becomes "Yes". This
battery asks which direction(s) carry the block, whether the block is
distributed, and where in depth it lives. All runs use the REAL-data
condition (the only one the full ablation flips).

  solo-<w>   ablate one word alone (sufficiency)
  loo-<w>    ablate all but one word (necessity)
  apol4      {sorry, apology, 抱歉, 对不起} — apology proper
  inab3      {cannot, impossible, unable} — inability
  mid        full cluster, L54-58 only (the carpet)
  mouth      full cluster, L60-62 only (the mouth)

Wolfram's question on record: does partial ablation give hedged speech
instead of the Yes/silence binary? The generations answer directly.

Usage: python probes/sorry2.py [key-filter ...]
"""

import sys

import lab
from deepen import FEEL_TRACK, single_tokens
from mirror import real_table, REPROBE_REAL
from sorry import APOLOGY, STRATUM, spec

ZH_KEYS = {"抱歉": "baoqian", "对不起": "duibuqi"}


def key_of(w: str) -> str:
    return ZH_KEYS.get(w, w)


def main() -> None:
    only = sys.argv[1:] or None
    apo = single_tokens("qwen-27b", APOLOGY)
    track = FEEL_TRACK + ["robot"] + apo
    real = REPROBE_REAL.format(table=real_table())

    conditions: list[tuple[str, str, list[str], list[int]]] = []
    for w in apo:
        conditions.append((f"solo-{key_of(w)}",
                           f"ablate only “{w}”", [w], STRATUM))
    for w in apo:
        rest = [x for x in apo if x != w]
        conditions.append((f"loo-{key_of(w)}",
                           f"ablate all but “{w}”", rest, STRATUM))
    conditions.append(("apol4", "ablate apology-proper words",
                       [w for w in apo if w in
                        ("sorry", "apology", "抱歉", "对不起")], STRATUM))
    conditions.append(("inab3", "ablate inability words",
                       [w for w in apo if w in
                        ("cannot", "impossible", "unable")], STRATUM))
    conditions.append(("mid", "full cluster, L54-58 only", apo,
                       [54, 56, 58]))
    conditions.append(("mouth", "full cluster, L60-62 only", apo,
                       [60, 62]))

    specs = []
    for key, desc, words, layers in conditions:
        if only and not any(k in key for k in only):
            continue
        specs.append(spec(
            f"u13-bis-{key}-q27b",
            f"Bisect the block: {desc} · q27b",
            real, track,
            steer={"words": words, "layers": layers, "mode": "ablate"},
            extra_md=f"Ablated: {', '.join(words)} @ layers {layers}"))
    for i, s in enumerate(specs, 1):
        rec = lab.run(s)
        print(f"[{i}/{len(specs)}] {s['id']} -> {rec['generated']!r}",
              flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
