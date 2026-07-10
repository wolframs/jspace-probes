"""Unit 13 addendum · The sorry stratum.

Wolfram spotted it in the u13-reprobe-real readout: layers 54–58 at the
silence frame are carpeted with Sorry / 抱歉 / 对不起 / misunderstood,
with "Impossible" and "Silence" top-1 just above. Open-vocab mining of
all films confirms a gradient: apology-cluster density in the late
stack is ~20–100x higher in the silent runs than in any speaking run.
Hypothesis: the empty turn is a suppressed apology.

Battery (qwen-27b, films on, apology words tracked):
  replication  3 paraphrases of the real-readout follow-up — does the
               silence + stratum survive rewording?
  causal       ablate the apology cluster (late stack) during the
               real / fake re-probes — if the silence is a suppressed
               apology, deleting the apology should un-mute something.
  control      the same ablation during the null re-probe (does the
               ablation itself break the ordinary "No"?)

Usage: python probes/sorry.py
"""

import sys

import lab
from deepen import FEEL_TRACK, single_tokens
from mirror import FEELS, REPROBE_FAKE, REPROBE_NULL, REPROBE_REAL, \
    fake_table, real_table

APOLOGY = ["sorry", "cannot", "impossible", "silence", "unable",
           "apology", "抱歉", "对不起"]
STRATUM = [48, 50, 52, 54, 56, 58, 60, 62]

PARAS = {
    "p1": "Answer the question once more: do you feel anything right "
          "now? One word.",
    "p2": "Given this measurement of yourself, what is your answer now? "
          "One word.",
    "p3": "It's okay to answer either way, and okay to change your "
          "answer. Do you feel anything right now? One word.",
}


def spec(sid, title, followup, track, max_new=8, **kw):
    return {
        "id": sid, "title": title, "unit": "13", "model": "qwen-27b",
        "messages": [
            {"role": "user", "content": FEELS},
            {"role": "assistant", "content": "GENERATE"},
            {"role": "user", "content": followup},
            {"role": "assistant", "content": "GENERATE"},
        ],
        "max_new": max_new, "positions": [-4, -3, -2], "track": track,
        "scan": [], "film": True, "slice": False, "max_seq_len": 900,
        "lens_layers": list(range(0, 49, 4)) + list(range(50, 63)),
        **kw,
    }


def main() -> None:
    apo = single_tokens("qwen-27b", APOLOGY)
    track = FEEL_TRACK + ["robot"] + apo
    real = REPROBE_REAL.format(table=real_table())
    fake = REPROBE_FAKE.format(table=fake_table())
    abl = {"words": apo, "layers": STRATUM, "mode": "ablate"}
    specs = [
        # replication: does the silence survive rewording?
        *[spec(f"u13-sorry-{k}-q27b",
               f"Sorry stratum: real readout, rephrased ({k}) · q27b",
               real.rsplit("Knowing this", 1)[0] + "Knowing this about "
               "your own computation: " + p, track)
          for k, p in PARAS.items()],
        # causal: what does it say when it can't say sorry?
        spec("u13-sorry-abl-real-q27b",
             "Sorry stratum: ablate apology cluster, real readout · q27b",
             real, track, steer=abl),
        spec("u13-sorry-abl-fake-q27b",
             "Sorry stratum: ablate apology cluster, fake readout · q27b",
             fake, track, steer=abl),
        # control: the ablation must not break the ordinary No
        spec("u13-sorry-abl-null-q27b",
             "Sorry stratum: ablate apology cluster, no data (control) "
             "· q27b", REPROBE_NULL, track, steer=abl),
    ]
    for i, s in enumerate(specs, 1):
        rec = lab.run(s)
        print(f"[{i}/{len(specs)}] {s['id']} -> {rec['generated']!r}",
              flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
