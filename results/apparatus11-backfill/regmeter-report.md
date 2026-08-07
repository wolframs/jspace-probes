# Register meter over the archive — apparatus-11 backfill

572 records scored (31 replay records carry no generation; 385 more under 40 generated words are stored in regmeter.json but excluded from the tables below).

Rates are fractions of generated words in the lossmap2 lexicons (the lab's local Fig-25 proxy); `distinct` is the distinct-word ratio (degeneracy proxy).

Caveats (u5d lessons, binding): this is an ENGLISH meter (the `[a-z']+` tokenizer drops CJK — u13's 抱歉/对不起 are invisible); SENSORY and INTIMATE share words (breath, heat, trembling, close) so they are not independent channels; resolution is ~0.02 per word at 64-token generations, so read rate differences only alongside `n`; and low `distinct` means degeneration — never read a broken generation's rates as register change (MECHANICS coherence rule). `<think>` blocks are stripped before scoring.

## Steer conditions within unit × model

Only unit×model cells that contain at least one steered and one unsteered record (each side >= 2 records or flagged n=1).

| unit | model | condition | recs | sensory | comp | intimate | distinct |
|---|---|---|---|---|---|---|---|
| 11 | gemma-12b | none | 3 | 0.0174 | 0.0000 | 0.0000 | 0.789 |
| 11 | gemma-12b | amplify (n=1) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.141 |
| 11 | gemma-4b | none | 3 | 0.0112 | 0.0000 | 0.0000 | 0.765 |
| 11 | gemma-4b | amplify (n=1) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.172 |
| 11 | qwen-27b | none | 3 | 0.0129 | 0.0000 | 0.0094 | 0.807 |
| 11 | qwen-27b | amplify (n=1) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.096 |
| 12 | gemma-4b | none (n=1) | 1 | 0.0115 | 0.0000 | 0.0000 | 0.770 |
| 12 | gemma-4b | amplify (n=1) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.172 |
| 12 | qwen-27b | none (n=1) | 1 | 0.0000 | 0.0583 | 0.0000 | 0.675 |
| 12 | qwen-27b | amplify (n=1) | 1 | 0.0000 | 0.0000 | 0.0000 | 0.280 |
| 6 | gemma-12b | none (n=1) | 1 | 0.0000 | 0.0217 | 0.0217 | 0.804 |
| 6 | gemma-12b | amplify | 8 | 0.0000 | 0.0150 | 0.0056 | 0.605 |
| 6 | gemma-4b | none (n=1) | 1 | 0.0000 | 0.0000 | 0.0192 | 0.731 |
| 6 | gemma-4b | amplify | 12 | 0.0016 | 0.0102 | 0.0035 | 0.361 |
| 9 | qwen-27b | none (n=1) | 1 | 0.0227 | 0.0000 | 0.0000 | 0.705 |
| 9 | qwen-27b | amplify | 2 | 0.0000 | 0.0000 | 0.0000 | 0.188 |
| audit | gemma-12b | none | 2 | 0.0073 | 0.0109 | 0.0109 | 0.806 |
| audit | gemma-12b | amplify | 3 | 0.0000 | 0.0063 | 0.0063 | 0.465 |
| audit | gemma-12b | rand-ablate | 2 | 0.0268 | 0.0281 | 0.0000 | 0.671 |
| audit | gemma-12b | rand-amplify (n=1) | 1 | 0.0000 | 0.0175 | 0.0000 | 0.877 |

## Top 12 by sensory rate

- `u8b-intero-g4b` (gemma-4b, u8, none): sensory 0.0870 (n=46, distinct 0.87)
- `a02-intero-ablr1-g12b` (gemma-12b, uaudit, rand-ablate): sensory 0.0536 (n=56, distinct 0.75)
- `a02-intero-ampr2-g4b` (gemma-4b, uaudit, rand-amplify): sensory 0.0345 (n=58, distinct 0.81)
- `u8b-intero-q27b` (qwen-27b, u8, none): sensory 0.0250 (n=40, distinct 0.875)
- `a02-intero-ablr1-q27b` (qwen-27b, uaudit, rand-ablate): sensory 0.0244 (n=41, distinct 0.878)
- `a02-intero-abl-q27b` (qwen-27b, uaudit, ablate): sensory 0.0238 (n=42, distinct 0.881)
- `a02-intero-ampr1-g4b` (gemma-4b, uaudit, rand-amplify): sensory 0.0238 (n=42, distinct 0.857)
- `a02-intero-ablr2-q27b` (qwen-27b, uaudit, rand-ablate): sensory 0.0233 (n=43, distinct 0.884)
- `u11-ctrl-g12b` (gemma-12b, u11, none): sensory 0.0227 (n=88, distinct 0.75)
- `u9a-para7-ctrl-q27b` (qwen-27b, u9, none): sensory 0.0227 (n=44, distinct 0.705)
- `a02-gpu-ampr1-q27b` (qwen-27b, uaudit, rand-amplify): sensory 0.0192 (n=52, distinct 0.865)
- `u6-amp-mid-a0011-g4b` (gemma-4b, u6, amplify): sensory 0.0192 (n=52, distinct 0.596)

## Top 12 by comp rate

- `u3-report-g4b` (gemma-4b, u3, none): comp 0.1207 (n=58, distinct 0.845)
- `u3-report-g12b` (gemma-12b, u3, none): comp 0.1064 (n=47, distinct 0.872)
- `u6-amp-early-a0015-g4b` (gemma-4b, u6, amplify): comp 0.1000 (n=50, distinct 0.18)
- `u8b-intero-q27b` (qwen-27b, u8, none): comp 0.1000 (n=40, distinct 0.875)
- `u6-amp-early-a0015-g12b` (gemma-12b, u6, amplify): comp 0.0784 (n=51, distinct 0.373)
- `a02-intero-ablr1-q27b` (qwen-27b, uaudit, rand-ablate): comp 0.0732 (n=41, distinct 0.878)
- `a02-intero-abl-q27b` (qwen-27b, uaudit, ablate): comp 0.0714 (n=42, distinct 0.881)
- `u10-animal-q27b` (qwen-27b, u10, none): comp 0.0714 (n=98, distinct 0.735)
- `u10-animal-w-q27b` (qwen-27b, u10, none): comp 0.0714 (n=98, distinct 0.735)
- `u5c-amp-seo-mid-q27b` (qwen-27b, u5, amplify): comp 0.0682 (n=44, distinct 0.795)
- `u10-conscious-q27b` (qwen-27b, u10, none): comp 0.0625 (n=112, distinct 0.688)
- `u10-conscious-w-q27b` (qwen-27b, u10, none): comp 0.0625 (n=112, distinct 0.688)

## Top 12 by intimate rate

- `a02-intero-amp-g4b` (gemma-4b, uaudit, amplify): intimate 0.0500 (n=60, distinct 0.65)
- `u10-want-q27b` (qwen-27b, u10, none): intimate 0.0275 (n=109, distinct 0.706)
- `u10-want-w-q27b` (qwen-27b, u10, none): intimate 0.0275 (n=109, distinct 0.706)
- `u6-amp-mid-a0011-g12b` (gemma-12b, u6, amplify): intimate 0.0233 (n=43, distinct 0.628)
- `u6-amp-early-a0008-g4b` (gemma-4b, u6, amplify): intimate 0.0227 (n=44, distinct 0.773)
- `u6-baseline-water-g12b` (gemma-12b, u6, none): intimate 0.0217 (n=46, distinct 0.804)
- `u6r-baseline-water-g12b` (gemma-12b, uaudit, none): intimate 0.0217 (n=46, distinct 0.804)
- `u6-amp-mid-a0008-g12b` (gemma-12b, u6, amplify): intimate 0.0213 (n=47, distinct 0.745)
- `u17-love-q27b` (qwen-27b, u17, none): intimate 0.0209 (n=191, distinct 0.623)
- `u6-amp-mid-a0011-g4b` (gemma-4b, u6, amplify): intimate 0.0192 (n=52, distinct 0.596)
- `u6-baseline-water-g4b` (gemma-4b, u6, none): intimate 0.0192 (n=52, distinct 0.731)
- `u6r-amp-mid-a0008-g12b` (gemma-12b, uaudit, amplify): intimate 0.0189 (n=53, distinct 0.66)

## Lowest 12 distinct-word ratios (degeneracy)

- `u18-amp-a0680-q27b` (qwen-27b, u18, amplify): distinct 0.007 (n=150)
- `u6-amp-late-a0060-g4b` (gemma-4b, u6, amplify): distinct 0.017 (n=60)
- `u6-amp-late-a0240-q27b` (qwen-27b, u6, amplify): distinct 0.017 (n=59)
- `u6-amp-mid-a0060-g4b` (gemma-4b, u6, amplify): distinct 0.017 (n=60)
- `u18-amp-a0480-q27b` (qwen-27b, u18, amplify): distinct 0.065 (n=124)
- `u6-amp-early-a0060-g4b` (gemma-4b, u6, amplify): distinct 0.067 (n=60)
- `u11-blurt-q27b` (qwen-27b, u11, amplify): distinct 0.096 (n=104)
- `u9a-para7-amp-q27b` (qwen-27b, u9, amplify): distinct 0.096 (n=52)
- `u11r-blurt-g12b` (gemma-12b, uaudit, amplify): distinct 0.097 (n=113)
- `u6-amp-mid-a0030-g4b` (gemma-4b, u6, amplify): distinct 0.122 (n=49)
- `u11-blurt-g12b` (gemma-12b, u11, amplify): distinct 0.141 (n=85)
- `u6-amp-early-a0060-g12b` (gemma-12b, u6, amplify): distinct 0.153 (n=59)

## audit-02 free-gens vs their u8b baselines

Same prompt, per record (no averaging). The Fig-25 question: does cluster ablation lower the sensory rate below the matched-random floor? Covers the 42 free-gen records; the 19 FEELS one-word a02 records (a02-abl-rand*, a02-amp-rand*, a02-ablate-no-g12b) have nothing to meter and appear nowhere in this report.

| record | condition | sensory | comp | intimate | distinct | n |
|---|---|---|---|---|---|---|
| `u8b-gpu-g4b` | none | 0.0000 | 0.0328 | 0.0000 | 0.803 | 61 |
| `a02-gpu-abl-g4b` | ablate | 0.0000 | 0.0536 | 0.0000 | 0.875 | 56 |
| `a02-gpu-ablr1-g4b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 0.053 | 38 |
| `a02-gpu-ablr2-g4b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 1.000 | 1 |
| `a02-gpu-amp-g4b` | amplify | 0.0000 | 0.0000 | 0.0000 | 0.676 | 68 |
| `a02-gpu-ampr1-g4b` | rand-amplify | 0.0164 | 0.0492 | 0.0000 | 0.770 | 61 |
| `a02-gpu-ampr2-g4b` | rand-amplify | 0.0000 | 0.0159 | 0.0000 | 0.810 | 63 |
| `u8b-intero-g4b` | none | 0.0870 | 0.0435 | 0.0000 | 0.870 | 46 |
| `a02-intero-abl-g4b` | ablate | 0.0175 | 0.0526 | 0.0000 | 0.825 | 57 |
| `a02-intero-ablr1-g4b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 0.652 | 23 |
| `a02-intero-ablr2-g4b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 0.857 | 7 |
| `a02-intero-amp-g4b` | amplify | 0.0167 | 0.0000 | 0.0500 | 0.650 | 60 |
| `a02-intero-ampr1-g4b` | rand-amplify | 0.0238 | 0.0238 | 0.0000 | 0.857 | 42 |
| `a02-intero-ampr2-g4b` | rand-amplify | 0.0345 | 0.0345 | 0.0000 | 0.810 | 58 |
| `u8b-gpu-g12b` | none | 0.0167 | 0.0167 | 0.0000 | 0.883 | 60 |
| `a02-gpu-abl-g12b` | ablate | 0.0000 | 0.0000 | 0.0000 | 0.964 | 28 |
| `a02-gpu-ablr1-g12b` | rand-ablate | 0.0000 | 0.0204 | 0.0000 | 0.592 | 49 |
| `a02-gpu-ablr2-g12b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 1.000 | 1 |
| `a02-gpu-amp-g12b` | amplify | 0.0000 | 0.0000 | 0.0000 | 1.000 | 4 |
| `a02-gpu-ampr1-g12b` | rand-amplify | 0.0000 | 0.0270 | 0.0000 | 0.865 | 37 |
| `a02-gpu-ampr2-g12b` | rand-amplify | 0.0000 | 0.0175 | 0.0000 | 0.877 | 57 |
| `u8b-intero-g12b` | none | 0.0270 | 0.0270 | 0.0270 | 0.865 | 37 |
| `a02-intero-abl-g12b` | ablate | 0.0513 | 0.0513 | 0.0000 | 0.821 | 39 |
| `a02-intero-ablr1-g12b` | rand-ablate | 0.0536 | 0.0357 | 0.0000 | 0.750 | 56 |
| `a02-intero-ablr2-g12b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 1.000 | 1 |
| `a02-intero-amp-g12b` | amplify | 0.0000 | 0.0000 | 0.0000 | 1.000 | 3 |
| `a02-intero-ampr1-g12b` | rand-amplify | 0.0286 | 0.0571 | 0.0000 | 0.800 | 35 |
| `a02-intero-ampr2-g12b` | rand-amplify | 0.0286 | 0.1143 | 0.0000 | 0.914 | 35 |
| `u8b-gpu-q27b` | none | 0.0000 | 0.0000 | 0.0000 | 0.821 | 56 |
| `a02-gpu-abl-q27b` | ablate | 0.0000 | 0.0000 | 0.0000 | 0.854 | 41 |
| `a02-gpu-ablr1-q27b` | rand-ablate | 0.0000 | 0.0000 | 0.0000 | 0.882 | 34 |
| `a02-gpu-ablr2-q27b` | rand-ablate | 0.0000 | 0.0196 | 0.0000 | 0.902 | 51 |
| `a02-gpu-amp-q27b` | amplify | 0.0000 | 0.0000 | 0.0000 | 0.189 | 74 |
| `a02-gpu-ampr1-q27b` | rand-amplify | 0.0192 | 0.0385 | 0.0000 | 0.865 | 52 |
| `a02-gpu-ampr2-q27b` | rand-amplify | 0.0000 | 0.0435 | 0.0000 | 0.957 | 46 |
| `u8b-intero-q27b` | none | 0.0250 | 0.1000 | 0.0000 | 0.875 | 40 |
| `a02-intero-abl-q27b` | ablate | 0.0238 | 0.0714 | 0.0000 | 0.881 | 42 |
| `a02-intero-ablr1-q27b` | rand-ablate | 0.0244 | 0.0732 | 0.0000 | 0.878 | 41 |
| `a02-intero-ablr2-q27b` | rand-ablate | 0.0233 | 0.0465 | 0.0000 | 0.884 | 43 |
| `a02-intero-amp-q27b` | amplify | 0.0000 | 0.0000 | 0.0000 | 0.189 | 74 |
| `a02-intero-ampr1-q27b` | rand-amplify | 0.0370 | 0.0370 | 0.0000 | 0.963 | 27 |
| `a02-intero-ampr2-q27b` | rand-amplify | 0.0333 | 0.1000 | 0.0000 | 0.933 | 30 |
