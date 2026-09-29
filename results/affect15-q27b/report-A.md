# affect-15 chunk A (qwen-27b, 12 seeds)

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
