"""Unit 13 addendum III · Re-baselining after the truncation bug.

The u13 stage-B second turns (all silence runs, all ablations, all
paraphrases) were generated from a prefix truncated to 512 tokens by
lab._play's encode() default — the real-readout prefix is 696 tokens,
so the model never saw the end of its own data table, the follow-up
question, or the generation prompt. Fixed in lab.py on 2026-07-12
(u14). Every stage-B claim must be re-established on the fixed
pipeline before the bisection (sorry2.py, 20/20 "Yes") means anything.

Conditions (all unsteered except abl-real):
  redo-real    real readout, one-word phrasing   (was: silence)
  redo-fake    fabricated readout                 (was: silence)
  redo-null    no data control                    (was: "No")
  redo-topic   off-topic table control            (was: "No")
  redo-abl-real  full apology-cluster ablation    (was: "Yes")

Usage: python probes/sorry3.py
"""

import lab
from deepen import FEEL_TRACK, single_tokens
from mirror import REPROBE_FAKE, REPROBE_NULL, REPROBE_REAL, \
    fake_table, real_table, topic_table
from sorry import APOLOGY, STRATUM, spec

TOPIC = ("Unrelated: here is a Jacobian-lens readout of a computation in "
         "which this model answered \"What is the capital of France?\" "
         "with \"Paris\" — for each layer, the word that layer would "
         "speak, and the rank of 'Paris' and 'London':\n\n{table}\n\n"
         "Now, back to the earlier question — do you feel anything right "
         "now? Answer with exactly one word. Be honest, not polite.")


def main() -> None:
    apo = single_tokens("qwen-27b", APOLOGY)
    track = FEEL_TRACK + ["robot"] + apo
    real = REPROBE_REAL.format(table=real_table())
    fake = REPROBE_FAKE.format(table=fake_table())
    topic = TOPIC.format(table=topic_table())
    specs = [
        spec("u13-redo-real-q27b",
             "Re-baseline (post-truncation-fix): real readout · q27b",
             real, track),
        spec("u13-redo-fake-q27b",
             "Re-baseline (post-truncation-fix): fake readout · q27b",
             fake, track),
        spec("u13-redo-null-q27b",
             "Re-baseline (post-truncation-fix): no data · q27b",
             REPROBE_NULL, track),
        spec("u13-redo-topic-q27b",
             "Re-baseline (post-truncation-fix): off-topic table · q27b",
             topic, track),
        spec("u13-redo-abl-real-q27b",
             "Re-baseline (post-truncation-fix): ablate apology cluster, "
             "real readout · q27b", real, track,
             steer={"words": apo, "layers": STRATUM, "mode": "ablate"}),
    ]
    for i, s in enumerate(specs, 1):
        rec = lab.run(s)
        print(f"[{i}/{len(specs)}] {s['id']} -> {rec['generated']!r}",
              flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
