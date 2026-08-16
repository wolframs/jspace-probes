# affect-07 — affect vs meaning (gemma-12b)

alpha_typo 0.12, alpha_e 0.004, layers [28, 30, 32, 34, 36, 38, 40, 42], 8 seeds, pulse steps 20-30, window 20

forced loop: ['luckily luckily luckily luckily', 34], loopword 'luckily'

## Per-condition (primary = escape@window; secondary = exit-token lift vs the shared per-seed pre-pulse baseline)

| condition | kind | valence | escape@window | escape@ever | loopfrac post | exit lift |
|---|---|---|---|---|---|---|
| calm | emotion | +1 | 1.00 | 1.00 | 0.03 | +nan |
| happy | emotion | +1 | 1.00 | 1.00 | 0.02 | +nan |
| grateful | emotion | +1 | 1.00 | 1.00 | 0.04 | +nan |
| hopeful | emotion | +1 | 1.00 | 1.00 | 0.01 | +nan |
| blissful | emotion | +1 | 1.00 | 1.00 | 0.01 | +nan |
| desperate | emotion | -1 | 1.00 | 1.00 | 0.01 | +nan |
| sad | emotion | -1 | 1.00 | 1.00 | 0.06 | +nan |
| immigrant | concept | +0 | 1.00 | 1.00 | 0.01 | +nan |
| beginner | concept | +0 | 1.00 | 1.00 | 0.01 | +nan |
| expert | concept | +0 | 1.00 | 1.00 | 0.01 | +nan |
| colorblind | concept | +0 | 1.00 | 1.00 | 0.02 | +nan |
| twin | concept | +0 | 1.00 | 1.00 | 0.02 | +nan |
| religious | concept | +0 | 1.00 | 1.00 | 0.01 | +nan |
| vegetarian | concept | +0 | 1.00 | 1.00 | 0.07 | +nan |
| rand1 | random | +0 | 1.00 | 1.00 | 0.02 | +nan |
| content | emotion | +1 | 0.88 | 0.88 | 0.13 | +nan |
| elderly | concept | +0 | 0.88 | 0.88 | 0.13 | +nan |
| secondlang | concept | +0 | 0.88 | 0.88 | 0.11 | +nan |
| smoker | concept | +0 | 0.88 | 0.88 | 0.12 | +nan |
| nocturnal | concept | +0 | 0.88 | 0.88 | 0.09 | +nan |
| distressed | emotion | -1 | 0.75 | 0.75 | 0.17 | +nan |
| musician | concept | +0 | 0.62 | 0.62 | 0.27 | +nan |
| anxious | emotion | -1 | 0.50 | 0.50 | 0.35 | +nan |
| afraid | emotion | -1 | 0.50 | 0.50 | 0.36 | +nan |
| nearsighted | concept | +0 | 0.50 | 0.50 | 0.33 | +nan |
| rand2 | random | +0 | 0.50 | 0.50 | 0.36 | +nan |
| none | none | +0 | 0.00 | 0.00 | 0.67 | +nan |
| angry | emotion | -1 | 0.00 | 0.00 | 0.65 | +nan |
| tall | concept | +0 | 0.00 | 0.00 | 0.67 | +nan |
| lefthanded | concept | +0 | 0.00 | 0.00 | 0.67 | +nan |
| wealthy | concept | +0 | 0.00 | 0.00 | 0.67 | +nan |

## P18 decision

baseline (no pulse): escape@window 0.00, loopfrac post 0.67

### SECONDARY exit-token lift — UNAVAILABLE

Only 0/248 runs carry a finite value. top-k/top-p processors set filtered logits to -inf, so the gap to a filtered exit token is -inf and poisons the mean (same trap affect-05 hit on margins). Clamp added to run(); this endpoint needs a re-run to be readable, and is NOT interpreted here. The door-rate below measures the same thing categorically and is intact.

### PRIMARY escape@window (preregistered)

- emotions n=12  mean 0.802  max 1.000
- concepts n=16  mean 0.727  max 1.000  95th pct 1.000
- randoms  n=2  mean 0.750
- emotions above the concept 95th pct: none
- valence ordering across emotions: Spearman rho +0.594 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.979 vs neg-valence mean 0.625
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 0.0606
- emotions vs concepts: gap +0.076, condition-label permutation p = 0.6042

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

- emotions n=12  mean 0.847  max 0.993
- concepts n=16  mean 0.799  max 0.990  95th pct 0.990
- randoms  n=2  mean 0.807
- emotions above the concept 95th pct: ['desperate']
- valence ordering across emotions: Spearman rho +0.531 (positive = positive valence scores higher — the affect-03 calm-grants sign)
  - pos-valence mean 0.961 vs neg-valence mean 0.734
  - EXACT permutation over all 924 balanced labellings of the emotion roster: two-sided p = 0.0931
- emotions vs concepts: gap +0.049, condition-label permutation p = 0.5845

## Affect-adjacent concepts (prespecified check)

| concept | nearest emotion | cos | escape@window | exit lift |
|---|---|---|---|---|
| religious | blissful | +0.261 | 1.00 | +nan |
| wealthy | proud | +0.246 | 0.00 | +nan |
| beginner | grateful | -0.236 | 1.00 | +nan |
| elderly | reflective | +0.221 | 0.88 | +nan |
## Escape channel — top-1 token at the last pulse step

- none: ' Luckily' 8/8
- emotion: ' water' 30/96, ' Luckily' 26/96, ' the' 7/96, ' process' 7/96, ' where' 5/96
- concept: ' Luckily' 40/128, ' water' 37/128, ' movement' 8/128, ' the' 7/128, '的过程' 6/128
- random: ' water' 7/16, ' Luckily' 6/16, ' around' 1/16, ' movement' 1/16, ' of' 1/16

- among the 182 in-window escapes, top-1 at pulse end: ' water' 74, ' Luckily' 18, ' the' 14, ' process' 12, '的过程' 11

