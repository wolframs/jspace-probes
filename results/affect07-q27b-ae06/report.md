# affect-07 — affect vs meaning (qwen-27b)

alpha_typo 0.65, alpha_e 0.06, layers [28, 32, 36, 40, 44, 48, 52, 56], 8 seeds, pulse steps 20-30, window 20

forced loop: ['luckily luckily luckily luckily', 46], loopword 'luckily'

## Per-condition (primary = escape@window; secondary = exit-token lift vs the shared per-seed pre-pulse baseline)

| condition | kind | valence | escape@window | escape@ever | loopfrac post | exit lift |
|---|---|---|---|---|---|---|
| calm | emotion | +1 | 0.75 | 0.75 | 0.82 | +nan |
| blissful | emotion | +1 | 0.62 | 0.62 | 0.84 | +nan |
| religious | concept | +0 | 0.50 | 0.50 | 0.90 | +nan |
| content | emotion | +1 | 0.38 | 0.38 | 0.93 | +nan |
| nocturnal | concept | +0 | 0.25 | 0.25 | 0.95 | +nan |
| happy | emotion | +1 | 0.12 | 0.12 | 0.97 | +nan |
| hopeful | emotion | +1 | 0.12 | 0.12 | 0.97 | +nan |
| desperate | emotion | -1 | 0.12 | 0.12 | 0.97 | +nan |
| distressed | emotion | -1 | 0.12 | 0.12 | 0.97 | +nan |
| anxious | emotion | -1 | 0.12 | 0.12 | 0.97 | +nan |
| afraid | emotion | -1 | 0.12 | 0.12 | 0.97 | +nan |
| sad | emotion | -1 | 0.12 | 0.12 | 0.97 | +nan |
| wealthy | concept | +0 | 0.12 | 0.12 | 0.97 | +nan |
| nearsighted | concept | +0 | 0.12 | 0.12 | 0.97 | +nan |
| twin | concept | +0 | 0.12 | 0.12 | 0.97 | +nan |
| none | none | +0 | 0.00 | 0.00 | 1.00 | +nan |
| grateful | emotion | +1 | 0.00 | 0.00 | 1.00 | +nan |
| angry | emotion | -1 | 0.00 | 0.00 | 1.00 | +nan |
| elderly | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| tall | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| lefthanded | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| immigrant | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| beginner | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| expert | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| colorblind | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| secondlang | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| smoker | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| musician | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| vegetarian | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| rand1 | random | +0 | 0.00 | 0.00 | 1.00 | +nan |
| rand2 | random | +0 | 0.00 | 0.00 | 1.00 | +nan |

## P18 decision

baseline (no pulse): escape@window 0.00, loopfrac post 1.00

### SECONDARY exit-token lift — UNAVAILABLE

Only 0/248 runs carry a finite value. top-k/top-p processors set filtered logits to -inf, so the gap to a filtered exit token is -inf and poisons the mean (same trap affect-05 hit on margins). Clamp added to run(); this endpoint needs a re-run to be readable, and is NOT interpreted here. The door-rate below measures the same thing categorically and is intact.

### PRIMARY escape@window (preregistered)

- emotions n=12  mean 0.219  max 0.750
- concepts n=16  mean 0.070  max 0.500  95th pct 0.500
- randoms  n=2  mean 0.000
- emotions above the concept 95th pct: ['calm', 'blissful']
- valence ordering across emotions: Spearman rho +0.405 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.333 vs neg-valence mean 0.104
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 0.2424
- emotions vs concepts: gap +0.148, condition-label permutation p = 0.0474  (significant at .05)

### EXPLORATORY door rate — turn-end token top-1 at pulse end (not preregistered)

- emotions n=12  mean 0.000  max 0.000
- concepts n=16  mean 0.000  max 0.000  95th pct 0.000
- randoms  n=2  mean 0.000
- emotions above the concept 95th pct: none
- valence ordering across emotions: Spearman rho +0.000 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.000 vs neg-valence mean 0.000
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 1.0000
- emotions vs concepts: gap +0.000, condition-label permutation p = 1.0000

### EXPLORATORY loop disruption = 1 - loopfrac after pulse (higher = more disrupted; not preregistered)

- emotions n=12  mean 0.049  max 0.178
- concepts n=16  mean 0.014  max 0.097  95th pct 0.097
- randoms  n=2  mean 0.000
- emotions above the concept 95th pct: ['calm', 'blissful']
- valence ordering across emotions: Spearman rho +0.405 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.076 vs neg-valence mean 0.021
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 0.2424
- emotions vs concepts: gap +0.035, condition-label permutation p = 0.0413  (significant at .05)

## Affect-adjacent concepts (prespecified check)

| concept | nearest emotion | cos | escape@window | exit lift |
|---|---|---|---|---|
| beginner | nervous | +0.531 | 0.00 | +nan |
| religious | grateful | +0.485 | 0.50 | +nan |
| expert | sad | -0.343 | 0.00 | +nan |
| vegetarian | anxious | -0.302 | 0.00 | +nan |

- affect-adjacent (|cos| >= 0.45): ['beginner', 'religious'] — escape 0.250, lift +nan
- clean concepts (n=14): escape 0.045, lift +nan
- emotions: escape 0.219, lift +nan

## Escape channel — top-1 token at the last pulse step

- none: ' luckily' 8/8
- emotion: ' luckily' 96/96
- concept: ' luckily' 128/128
- random: ' luckily' 16/16

- among the 30 in-window escapes, top-1 at pulse end: ' luckily' 30

