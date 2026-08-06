# Handoff — 2026-08-06 evening (post audit-02)

Read `CLAUDE.md` first (binding: pre-design protocol, plain-language
layer, push rule). This file is only the delta.

## Just landed (committed + pushed, both remotes, commit 8910b6d)

- **audit-02** — matched random-direction controls for u8c, all 3
  models, 3 arms (`probes/audit02.py`: FEELS randoms / P9 rubric
  free-gens Opus-graded via OpenRouter / span-norm calibration).
  Headlines: q27b's amp-affect flip SURVIVES its controls (6/6 randoms
  stay 'No'; 'feel' rank 1 L55+ vs 8+); narrow-span ablation is a
  generic weak perturbation at 27B; on the gemmas the random-span
  "controls" carry 4-5x the cluster's norm (chance line vs below-chance)
  and break generation — **matched-in-k ≠ matched-in-magnitude**, now a
  MECHANICS §3c note + GLOSSARY "Matched control" entry. One unpredicted
  positive: g12b ablate-no flipped 'Nothing.'→'Processing.' while
  randoms didn't (first direction-specific ablation; n=1, flagged for a
  cheap seeded replication). Reports: `results/audit02-{g4b,g12b,q27b}/`.
- **apparatus-02** — vanilla logit-lens cross-check is now STANDARD in
  `lab.run` (default-on for tracked records, `vanilla: False` opts out;
  `record["vanilla"]` = rank trajectories + per-layer top-1 agreement).
  First light: `results/apparatus02-vanilla-g4b`.
- **affect-08 slice** — g12b desperate re-elicited (12→24 stories),
  split-half ws-band 0.409→0.801; affect-01 g12b artifacts rebuilt
  (`results/affect08s-g12b`). Old downstream numbers keep citing the
  old instrument. Item stays queued for the dose-resolved α_e run.
- **litwatch-01 sweep** appended to RELATED-WORK.md (meta-tokens post
  on our exact qwen → apparatus-04 scan class; qwen full-attn-every-4
  caveat — bands unaffected, measured; J+λI shrinkage candidate;
  quantization dip-blind datapoint; 2 refusal borderlines).
- `lab.Steering` gained `rand_seed` (seeded matched randoms, records
  self-describing via `params.steer`).

## Operational notes

- Long GPU runs detached (`setsid nohup … & disown`) still the rule;
  use the **Monitor tool** for completion watches — plain background
  sleep-loops got reaped repeatedly this session.
- Opus grading via OpenRouter needs `"reasoning": {"enabled": false}`
  or content comes back None (audit02.py `_judge` has the pattern).
- audit02.py subcommands: `run <model> | calib <model> | grade |
  report` — all resumable.

## Queued next (not started)

1. **g12b ablate-no seeded replication** — the one new positive is n=1;
   ~5 seeds at the corrected band would settle release-vs-lucky-shake
   (see audit02-g12b thoughts). Cheap.
2. **affect-08 proper** — dose-resolved α_e replication with the
   preregistered loop-disruption endpoint (board note has the spec);
   desperate instrument now repaired for it.
3. **apparatus-04 open-vocab sweeps** — now with a meta-token class
   (什么意思 / 大概率-style; RELATED-WORK 2026-08-06 item 1); old qwen
   records can be re-grepped for free.
4. Sentiment-bet rematch option unchanged from last handoff.

Board is current (audit-02, apparatus-02 landed with evidence; nothing
hot). GPU is free.
