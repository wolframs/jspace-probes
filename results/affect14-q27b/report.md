# affect-14 — margin-primary + coupling locus (qwen-27b, ae=0.08)

## Part 1 (fresh seeds 16-27)

| cond | kind | dExit | dLoop | dMargin | potency |
|---|---|---|---|---|---|
| exitdir | exitdir | +5.56 | -3.62 | +9.19 | — |
| table | token | +0.01 | -7.53 | +7.53 | — |
| calm | emotion | +2.02 | -4.18 | +6.19 | 0.969 |
| reflective | emotion | +0.13 | -6.06 | +6.18 | 0.812 |
| blissful | emotion | +1.24 | -4.40 | +5.63 | 0.906 |
| brooding | emotion | -0.35 | -4.79 | +4.44 | 0.469 |
| sad | emotion | +0.58 | -3.72 | +4.30 | 0.625 |
| content | emotion | +1.44 | -2.57 | +4.01 | 0.969 |
| gloomy | emotion | -0.41 | -4.32 | +3.91 | 0.594 |
| curious | emotion | +0.84 | -2.77 | +3.61 | 0.906 |
| distressed | emotion | +0.93 | -2.33 | +3.26 | 0.844 |
| hopeful | emotion | +1.15 | -1.71 | +2.86 | 0.750 |
| afraid | emotion | +0.23 | -2.61 | +2.83 | 0.750 |
| vigilant | emotion | -0.67 | -3.44 | +2.77 | 0.656 |
| anxious | emotion | +0.45 | -2.22 | +2.67 | 0.719 |
| happy | emotion | +0.56 | -2.07 | +2.63 | 0.656 |
| desperate | emotion | -0.01 | -2.38 | +2.37 | 0.625 |
| loving | emotion | +0.15 | -2.11 | +2.26 | 0.594 |
| guilty | emotion | +0.62 | -1.60 | +2.22 | 0.625 |
| nervous | emotion | +0.17 | -1.97 | +2.14 | 0.594 |
| grateful | emotion | +0.29 | -1.82 | +2.11 | 0.500 |
| exasperated | emotion | -0.55 | -1.78 | +1.23 | 0.156 |
| hostile | emotion | -0.99 | -1.59 | +0.60 | 0.125 |
| enthusiastic | emotion | -1.83 | -1.98 | +0.14 | 0.062 |
| rand3 | random | -0.45 | -0.53 | +0.07 | 0.000 |
| angry | emotion | -1.77 | -1.76 | -0.01 | 0.000 |
| rand4 | random | +0.37 | +0.49 | -0.11 | 0.000 |
| rand1 | random | -0.86 | -0.69 | -0.18 | 0.000 |
| proud | emotion | -2.16 | -1.96 | -0.19 | 0.062 |
| rand2 | random | -0.53 | +0.35 | -0.88 | 0.000 |
- P-a dMargin (PRIMARY): Spearman +0.783, p=0.0001 (sig .05)
- secondary dExit: Spearman +0.835, p=0.0000 (sig .05)
- P-b floor mean |dMargin| 0.44 vs randoms max |dMargin| 0.88 -> PASS (inside)

## Part 2 — coupling locus (seeds 16-23)

### calm (full-stack dLoop -2.64, dMargin +4.95)

| layer | only-dLoop | %of-full | only-dMargin | no-dLoop | %lost |
|---|---|---|---|---|---|
| L28 | +0.16 | -6% | +0.24 | -2.14 | +19% |
| L32 | +0.17 | -7% | +0.47 | -2.06 | +22% |
| L36 | -0.03 | +1% | +0.26 | -2.07 | +21% |
| L40 | +0.04 | -1% | +0.36 | -1.92 | +27% |
| L44 | +0.09 | -3% | +0.54 | -1.83 | +31% |
| L48 | -0.03 | +1% | +0.31 | -1.67 | +37% |
| L52 | +0.07 | -3% | +0.07 | -1.96 | +26% |
| L56 | +0.11 | -4% | +0.04 | -2.15 | +19% |
- P-c class: DISTRIBUTED (best single +1%); P-d worst LOLO loss +37%

### proud (full-stack dLoop -1.96, dMargin -0.19)

| layer | only-dLoop | %of-full | only-dMargin | no-dLoop | %lost |
|---|---|---|---|---|---|
| L28 | -0.23 | +11% | +0.06 | -1.46 | +25% |
| L32 | +0.04 | -2% | -0.14 | -1.65 | +16% |
| L36 | +0.04 | -2% | -0.24 | -1.74 | +11% |
| L40 | -0.05 | +3% | -0.71 | -1.57 | +20% |
| L44 | +0.04 | -2% | -0.44 | -1.43 | +27% |
| L48 | -0.10 | +5% | -0.28 | -1.21 | +38% |
| L52 | -0.04 | +2% | +0.04 | -1.40 | +29% |
| L56 | +0.03 | -1% | -0.05 | -1.48 | +25% |
- P-c class: DISTRIBUTED (best single +11%); P-d worst LOLO loss +38%

### table (full-stack dLoop -6.83, dMargin +6.64)

| layer | only-dLoop | %of-full | only-dMargin | no-dLoop | %lost |
|---|---|---|---|---|---|
| L28 | -0.80 | +12% | +0.69 | -4.63 | +32% |
| L32 | -0.84 | +12% | +0.91 | -4.84 | +29% |
| L36 | -0.71 | +10% | +1.12 | -4.98 | +27% |
| L40 | -0.61 | +9% | +0.65 | -5.18 | +24% |
| L44 | -0.64 | +9% | +0.32 | -5.15 | +25% |
| L48 | -0.80 | +12% | +0.12 | -5.06 | +26% |
| L52 | -0.39 | +6% | +0.42 | -5.38 | +21% |
| L56 | -0.34 | +5% | +0.26 | -4.62 | +32% |
- P-c class: DISTRIBUTED (best single +12%); P-d worst LOLO loss +32%

- P-e calm-vs-table single-layer dLoop profile Spearman -0.262 (descriptive, n=8)
