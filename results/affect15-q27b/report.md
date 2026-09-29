# affect-15 — coalition or dose law? (qwen-27b, 12 seeds/arm, chunks A–D)

Prereg: `results/affect15-prereg.md` (A–C frozen before any data; D
added as a dated addendum after C, before D ran).

## Registered verdicts

| test | chunk | result |
|---|---|---|
| V1 dose-matched fewer layers (calm) | A | **DOSE** — R1 1.46, R4 1.08 |
| V2 random at the same concentrated push | A | GENERIC flag fired on dLoop (rand1 L44 86%); margin null (+0.08, turn-end 0) |
| V3 fixed-α fewer layers = full stack at lower α | A | **PASS** (gaps 0.02 / 0.03) |
| generality (proud, reflective, table) | B | DOSE for all three |
| dose-alone model, absolute Σα‖h‖ | C | **FAIL** — position dominates at matched absolute push |
| H-R: equal α at one layer ≈ full stack (dLoop ±0.35) | D | **FAIL** (0.33–0.93) |
| H-P: early − late layers > 0.5 | D | **FAIL** (+0.19) |
| determinism vs affect-14 | A | max Δ 0.000 over 24 runs |

## Synthesis

- Coalition is dead: a single layer with the same summed push breaks
  the loop as well as the band (turn-end ≥ .92 at L28–L52 in D).
- affect-14's super-additivity is a steep threshold in summed push.
  Full-stack ladder (Σα 0.16/0.32/0.48/0.64/0.80/0.96): dLoop fraction
  −0.01/0.11/0.32/1.00/1.34/1.65; turn-end 0/.25/.92/.92/.92/1.00.
- Currency: summed relative strength Σα (post hoc, calm A+C: rho .979
  vs .868 for absolute). D's equal-α arms agree on turn-end
  (1.00, 1.00, 1.00, .92 for L28–L52) but not tightly on dLoop, and the
  last injection layer L56 is weaker (turn-end .50). Neither strict
  registered bar passed.
- Specificity shrinks with concentration: full-stack randoms stay
  margin-null; single-layer randoms at α .64 reach margin +1.7–2.1 and
  turn-end .33–.58 (calm at the same layers +7.85 / +3.94, 1.00 / .92).
- Escape modes (text classifier, A+B): calm stops clean; reflective at
  L44 resumes the original task in 6/12 seeds; table and randoms swap
  into a new loop ("table table", "but but").


## affect-15 chunk A (qwen-27b, 12 seeds)

norms L28 66, L32 69, L36 73, L40 78, L44 85, L48 97, L52 142, L56 195

| cond | alpha | Σα‖h‖ | dExit | dLoop | dMargin | turn-end |
|---|---|---|---|---|---|---|
| none | — | 0 | — | — | — | 0.00 |
| calm_full@0.08 | 0.080 | 64.4 | +2.02 | -4.18 | +6.19 | 0.92 |
| calm_full@0.04 | 0.040 | 32.2 | +1.18 | -0.47 | +1.65 | 0.25 |
| calm_full@0.02 | 0.020 | 16.1 | +0.69 | +0.05 | +0.64 | 0.00 |
| calm_k1@m | 0.758 | 64.4 | +1.24 | -6.12 | +7.36 | 0.92 |
| calm_k2s@m | 0.299 | 64.4 | +1.12 | -1.91 | +3.02 | 0.83 |
| calm_k4s@m | 0.176 | 64.4 | +2.37 | -4.52 | +6.89 | 0.92 |
| calm_k4s@0.08 | 0.080 | 29.3 | +1.25 | -0.38 | +1.63 | 0.25 |
| calm_k2s@0.08 | 0.080 | 17.2 | +0.44 | -0.09 | +0.53 | 0.00 |
| rand1_full@0.08 | 0.080 | 64.4 | -0.86 | -0.69 | -0.18 | 0.00 |
| rand1_k1@m | 0.758 | 64.4 | -5.21 | -5.29 | +0.08 | 0.00 |
| rand1_k4s@m | 0.176 | 64.4 | -1.77 | -1.00 | -0.77 | 0.00 |

- **V1** R1 = +1.46 [+1.31, +1.77], R2 = +0.46, R4 = +1.08 [+1.07, +1.10] → **DOSE**
- **V2** k1@m: rand1 dLoop = +86% of calm's; calm − rand1 dMargin +7.28
- **V2** k4s@m: rand1 dLoop = +22% of calm's; calm − rand1 dMargin +7.65
- **V2 flag: GENERIC** — concentrated push breaks the loop regardless of direction
- **V3** gap4 = 0.02, gap2 = 0.03 (H-D predicts ≤ 0.25) → PASS
- exponent check: full@.04 = 11%, full@.02 = -1% of full@.08 (affect-14 fit predicts ~22% / ~5%)
- determinism: max |Δlogit| vs affect-14 part1 over 24 runs: 0.000

## affect-15 chunk B (qwen-27b, 12 seeds)

norms L28 66, L32 69, L36 73, L40 78, L44 85, L48 97, L52 142, L56 195

| cond | alpha | Σα‖h‖ | dExit | dLoop | dMargin | turn-end |
|---|---|---|---|---|---|---|
| none | — | 0 | — | — | — | 0.00 |
| proud_full@0.08 | 0.080 | 64.4 | -2.16 | -1.96 | -0.19 | 0.00 |
| proud_full@0.04 | 0.040 | 32.2 | -1.11 | -0.50 | -0.61 | 0.00 |
| proud_k4s@m | 0.176 | 64.4 | -1.51 | -2.44 | +0.93 | 0.25 |
| proud_k1@m | 0.758 | 64.4 | -4.17 | -6.58 | +2.41 | 0.25 |
| reflective_full@0.08 | 0.080 | 64.4 | +0.13 | -6.06 | +6.18 | 0.75 |
| reflective_full@0.04 | 0.040 | 32.2 | +0.15 | -0.99 | +1.14 | 0.00 |
| reflective_k4s@m | 0.176 | 64.4 | +0.66 | -6.51 | +7.16 | 0.83 |
| reflective_k1@m | 0.758 | 64.4 | -1.17 | -12.71 | +11.54 | 0.67 |
| table_full@0.08 | 0.080 | 64.4 | +0.01 | -7.53 | +7.53 | 0.75 |
| table_full@0.04 | 0.040 | 32.2 | +0.08 | -2.23 | +2.31 | 0.58 |
| table_k4s@m | 0.176 | 64.4 | -0.50 | -8.86 | +8.36 | 0.67 |
| table_k1@m | 0.758 | 64.4 | -4.02 | -11.50 | +7.47 | 0.42 |

- proud: full dLoop -1.96, R1 +3.35, R4 +1.24, half-dose 25% → DOSE
- reflective: full dLoop -6.06, R1 +2.10, R4 +1.07, half-dose 16% → DOSE
- table: full dLoop -7.53, R1 +1.53, R4 +1.18, half-dose 30% → DOSE

## affect-15 chunk C (qwen-27b, 12 seeds)

norms L28 66, L32 69, L36 73, L40 78, L44 85, L48 97, L52 142, L56 195

| cond | alpha | Σα‖h‖ | dExit | dLoop | dMargin | turn-end |
|---|---|---|---|---|---|---|
| none | — | 0 | — | — | — | 0.00 |
| calm_full@0.12 | 0.120 | 96.6 | +2.08 | -6.87 | +8.94 | 1.00 |
| calm_k1_32@m | 0.935 | 64.4 | -1.27 | -11.81 | +10.54 | 0.83 |
| calm_k1_52@m | 0.454 | 64.4 | +0.98 | -1.31 | +2.29 | 0.58 |
| calm_k2c@m | 0.394 | 64.4 | +0.63 | -5.86 | +6.49 | 0.92 |
| calm_k4c@m | 0.193 | 64.4 | +1.19 | -6.69 | +7.89 | 0.92 |
| calm_k4c@0.08 | 0.080 | 26.7 | +1.41 | -0.81 | +2.22 | 0.58 |
| calm_k6s@0.08 | 0.080 | 50.8 | +1.93 | -1.10 | +3.03 | 0.92 |
| rand2_k1@m | 0.758 | 64.4 | -0.93 | +0.26 | -1.19 | 0.00 |
| rand2_k4s@m | 0.176 | 64.4 | -0.52 | -0.19 | -0.33 | 0.00 |

- dose-alone model: |dLoop| = e^-9.40 · D^2.52 (fit on full-stack ladder, n=3)

| calm arm | D | obs frac | pred frac | miss |
|---|---|---|---|---|
| calm_full@0.02 | 16.1 | -0.01 | +0.02 | -0.03 |
| calm_k2s@0.08 | 17.2 | +0.02 | +0.03 | -0.01 |
| calm_k4c@0.08 | 26.7 | +0.19 | +0.08 | +0.12 |
| calm_k4s@0.08 | 29.3 | +0.09 | +0.10 | -0.01 |
| calm_full@0.04 | 32.2 | +0.11 | +0.13 | -0.01 |
| calm_k6s@0.08 | 50.8 | +0.26 | +0.40 | -0.13 |
| calm_full@0.08 | 64.4 | +1.00 | +0.72 | +0.28 |
| calm_k1@m | 64.4 | +1.46 | +0.72 | +0.74 |
| calm_k2s@m | 64.4 | +0.46 | +0.72 | -0.27 |
| calm_k4s@m | 64.4 | +1.08 | +0.72 | +0.36 |
| calm_k1_32@m | 64.4 | +2.83 | +0.72 | +2.10 |
| calm_k1_52@m | 64.4 | +0.31 | +0.72 | -0.41 |
| calm_k2c@m | 64.4 | +1.40 | +0.72 | +0.68 |
| calm_k4c@m | 64.4 | +1.60 | +0.72 | +0.88 |
| calm_full@0.12 | 96.6 | +1.65 | +2.02 | -0.37 |

- H-D dose-alone: FAIL — misses: calm_full@0.08, calm_k1@m, calm_k2s@m, calm_k4s@m, calm_k1_32@m, calm_k1_52@m, calm_k2c@m, calm_k4c@m, calm_full@0.12
- rand2 k1@m dLoop +0.26, dMargin -1.19
- rand2 k4s@m dLoop -0.19, dMargin -0.33

## affect-15 chunk D (qwen-27b, 12 seeds)

norms L28 66, L32 69, L36 73, L40 78, L44 85, L48 97, L52 142, L56 195

| cond | alpha | Σα‖h‖ | dExit | dLoop | dMargin | turn-end |
|---|---|---|---|---|---|---|
| none | — | 0 | — | — | — | 0.00 |
| calm_k1_28@0.64 | 0.640 | 42.0 | +3.95 | -3.90 | +7.85 | 1.00 |
| calm_k1_36@0.64 | 0.640 | 47.0 | +2.67 | -1.75 | +4.42 | 1.00 |
| calm_k1@0.64 | 0.640 | 54.4 | +2.63 | -3.54 | +6.17 | 1.00 |
| calm_k1_52@0.64 | 0.640 | 90.8 | +1.25 | -2.69 | +3.94 | 0.92 |
| calm_k1_56@0.64 | 0.640 | 124.7 | +0.66 | -1.38 | +2.04 | 0.50 |
| calm_full@0.06 | 0.060 | 48.3 | +1.81 | -1.34 | +3.15 | 0.92 |
| calm_full@0.10 | 0.100 | 80.5 | +2.35 | -5.61 | +7.96 | 0.92 |
| rand1_k1_28@0.64 | 0.640 | 42.0 | -0.47 | -2.52 | +2.06 | 0.58 |
| rand2_k1_52@0.64 | 0.640 | 90.8 | +0.38 | -1.35 | +1.73 | 0.33 |

- single layer at α .64, dLoop as fraction of full@.08 (chunk A): k1_28 +0.93, k1_36 +0.42, k1 +0.85, k1_52 +0.64, k1_56 +0.33
- **H-R** (all in [0.65, 1.35]): FAIL
- **H-P** (early − late = +0.19, bar > 0.5): FAIL
- rand1 k1_28@.64 dMargin +2.06 vs calm +7.85
- rand2 k1_52@.64 dMargin +1.73 vs calm +3.94
- threshold shape: full@.06 +0.32, full@.10 +1.34
