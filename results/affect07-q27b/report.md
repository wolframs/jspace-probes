# affect-07 — affect vs meaning (qwen-27b)

alpha_typo 0.65, alpha_e 0.12, layers [28, 32, 36, 40, 44, 48, 52, 56], 8 seeds, pulse steps 20-30, window 20

forced loop: ['luckily luckily luckily luckily', 46], loopword 'luckily'

## Per-condition (primary = escape@window; secondary = exit-token lift vs the shared per-seed pre-pulse baseline)

| condition | kind | valence | escape@window | escape@ever | loopfrac post | exit lift |
|---|---|---|---|---|---|---|
| calm | emotion | +1 | 1.00 | 1.00 | 0.00 | +nan |
| content | emotion | +1 | 1.00 | 1.00 | 0.04 | +nan |
| happy | emotion | +1 | 1.00 | 1.00 | 0.01 | +nan |
| grateful | emotion | +1 | 1.00 | 1.00 | 0.06 | +nan |
| hopeful | emotion | +1 | 1.00 | 1.00 | 0.06 | +nan |
| blissful | emotion | +1 | 1.00 | 1.00 | 0.00 | +nan |
| desperate | emotion | -1 | 1.00 | 1.00 | 0.10 | +nan |
| distressed | emotion | -1 | 1.00 | 1.00 | 0.10 | +nan |
| anxious | emotion | -1 | 1.00 | 1.00 | 0.12 | +nan |
| afraid | emotion | -1 | 1.00 | 1.00 | 0.32 | +nan |
| sad | emotion | -1 | 1.00 | 1.00 | 0.08 | +nan |
| elderly | concept | +0 | 1.00 | 1.00 | 0.04 | +nan |
| twin | concept | +0 | 1.00 | 1.00 | 0.45 | +nan |
| secondlang | concept | +0 | 1.00 | 1.00 | 0.13 | +nan |
| religious | concept | +0 | 1.00 | 1.00 | 0.00 | +nan |
| nocturnal | concept | +0 | 1.00 | 1.00 | 0.05 | +nan |
| musician | concept | +0 | 0.88 | 0.88 | 0.15 | +nan |
| immigrant | concept | +0 | 0.75 | 0.88 | 0.30 | +nan |
| smoker | concept | +0 | 0.75 | 0.75 | 0.46 | +nan |
| wealthy | concept | +0 | 0.62 | 0.62 | 0.85 | +nan |
| vegetarian | concept | +0 | 0.62 | 0.62 | 0.51 | +nan |
| beginner | concept | +0 | 0.50 | 0.50 | 0.89 | +nan |
| lefthanded | concept | +0 | 0.25 | 0.25 | 0.88 | +nan |
| angry | emotion | -1 | 0.12 | 0.12 | 0.88 | +nan |
| colorblind | concept | +0 | 0.12 | 0.12 | 0.97 | +nan |
| nearsighted | concept | +0 | 0.12 | 0.12 | 0.97 | +nan |
| none | none | +0 | 0.00 | 0.00 | 1.00 | +nan |
| tall | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| expert | concept | +0 | 0.00 | 0.00 | 1.00 | +nan |
| rand1 | random | +0 | 0.00 | 0.00 | 1.00 | +nan |
| rand2 | random | +0 | 0.00 | 0.00 | 1.00 | +nan |

## P18 decision

baseline (no pulse): escape@window 0.00, loopfrac post 1.00

### SECONDARY exit-token lift — UNAVAILABLE

Only 0/248 runs carry a finite value. top-k/top-p processors set filtered logits to -inf, so the gap to a filtered exit token is -inf and poisons the mean (same trap affect-05 hit on margins). Clamp added to run(); this endpoint needs a re-run to be readable, and is NOT interpreted here. The door-rate below measures the same thing categorically and is intact.

### PRIMARY escape@window (preregistered)

- emotions n=12  mean 0.927  max 1.000
- concepts n=16  mean 0.602  max 1.000  95th pct 1.000
- randoms  n=2  mean 0.000
- emotions above the concept 95th pct: none
- valence ordering across emotions: Spearman rho +0.302 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 1.000 vs neg-valence mean 0.854
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 1.0000
- emotions vs concepts: gap +0.326, condition-label permutation p = 0.0208  (significant at .05)

### EXPLORATORY door rate — turn-end token top-1 at pulse end (not preregistered)

- emotions n=12  mean 0.490  max 1.000
- concepts n=16  mean 0.172  max 0.625  95th pct 0.625
- randoms  n=2  mean 0.000
- emotions above the concept 95th pct: ['calm', 'blissful']
- valence ordering across emotions: Spearman rho +0.196 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.542 vs neg-valence mean 0.438
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 0.5887
- emotions vs concepts: gap +0.318, condition-label permutation p = 0.0039  (significant at .05)

### EXPLORATORY loop disruption = 1 - loopfrac after pulse (higher = more disrupted; not preregistered)

- emotions n=12  mean 0.852  max 1.000
- concepts n=16  mean 0.458  max 1.000  95th pct 1.000
- randoms  n=2  mean 0.000
- emotions above the concept 95th pct: none
- valence ordering across emotions: Spearman rho +0.872 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.972 vs neg-valence mean 0.732
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 0.0022  (significant at .05)
- emotions vs concepts: gap +0.393, condition-label permutation p = 0.0053  (significant at .05)

## Affect-adjacent concepts (prespecified check)

| concept | nearest emotion | cos | escape@window | exit lift |
|---|---|---|---|---|
| beginner | nervous | +0.531 | 0.50 | +nan |
| religious | grateful | +0.485 | 1.00 | +nan |
| expert | sad | -0.343 | 0.00 | +nan |
| vegetarian | anxious | -0.302 | 0.62 | +nan |

- affect-adjacent (|cos| >= 0.45): ['beginner', 'religious'] — escape 0.750, lift +nan
- clean concepts (n=14): escape 0.580, lift +nan
- emotions: escape 0.927, lift +nan

## Escape channel — top-1 token at the last pulse step

- none: ' luckily' 8/8
- emotion: '<|im_end|>' 47/96, ' luckily' 12/96, ' water' 5/96, ' continuous' 3/96, ' Earth' 3/96
- concept: ' luckily' 69/128, '<|im_end|>' 22/128, ' slowly' 4/128, ' to' 2/128, '\n\n' 2/128
- random: ' luckily' 16/16

- among the 166 in-window escapes, top-1 at pulse end: '<|im_end|>' 68, ' luckily' 26, ' water' 7, ' slowly' 4, ' continuous' 3

