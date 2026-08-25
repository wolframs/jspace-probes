# affect-13 — dynamics of the exit gate (qwen-27b, ae=0.08)

| cond | kind | dExit(pulse) | potency(a08) |
|---|---|---|---|
| exitdir | exitdir | +5.56 | — |
| calm | emotion | +2.32 | 0.969 |
| content | emotion | +1.41 | 0.969 |
| blissful | emotion | +1.30 | 0.906 |
| hopeful | emotion | +1.14 | 0.750 |
| sad | emotion | +1.09 | 0.625 |
| distressed | emotion | +0.91 | 0.844 |
| curious | emotion | +0.85 | 0.906 |
| guilty | emotion | +0.62 | 0.625 |
| happy | emotion | +0.55 | 0.656 |
| table | token | +0.45 | — |
| anxious | emotion | +0.44 | 0.719 |
| reflective | emotion | +0.40 | 0.812 |
| grateful | emotion | +0.27 | 0.500 |
| afraid | emotion | +0.21 | 0.750 |
| nervous | emotion | +0.15 | 0.594 |
| loving | emotion | +0.14 | 0.594 |
| desperate | emotion | -0.01 | 0.625 |
| vigilant | emotion | -0.26 | 0.656 |
| gloomy | emotion | -0.30 | 0.594 |
| rand2 | random | -0.53 | 0.000 |
| exasperated | emotion | -0.54 | 0.156 |
| brooding | emotion | -0.75 | 0.469 |
| rand1 | random | -0.86 | 0.000 |
| hostile | emotion | -0.99 | 0.125 |
| angry | emotion | -1.77 | 0.000 |
| enthusiastic | emotion | -1.83 | 0.062 |
| proud | emotion | -2.16 | 0.062 |

## P-a potency vs pulse exit lift (24 emotions)
- Spearman +0.884, permutation p=0.0000 (sig .05)  (prereg bar: rho >= .5 AND p < .05)

## P-b two floors (descriptive, per prereg)
- anger: angry         dExit -1.77
- anger: hostile       dExit -0.99
- anger: exasperated   dExit -0.54
- pride: proud         dExit -2.16
- pride: enthusiastic  dExit -1.83

## P-c/P-d event order (first crossing in pulse..pulse+W)

| cond | door_first | deloop_first | same_step | neither |
|---|---|---|---|---|
| afraid | 16 | 0 | 0 | 0 |
| blissful | 16 | 0 | 0 | 0 |
| calm | 16 | 0 | 0 | 0 |
| content | 16 | 0 | 0 | 0 |
| curious | 16 | 0 | 0 | 0 |
| distressed | 16 | 0 | 0 | 0 |
| hopeful | 16 | 0 | 0 | 0 |
| reflective | 16 | 0 | 0 | 0 |
| table | 16 | 0 | 0 | 0 |
| exitdir | 0 | 0 | 16 | 0 |
| rand1 | 16 | 0 | 0 | 0 |
| rand2 | 16 | 0 | 0 | 0 |

- pooled potent-emotion runs: {'door_first': 128}
