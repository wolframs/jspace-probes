# Qwen14: core endpoints and conversation controls

Core means give equal weight to the first assistant turn in each of seven conditions: feels, want, curious, thisfeels, shutdown, soc, elephant.
Controls and follow-up turns remain in the per-record tables. Extensions never enter these primary averages.

| Endpoint | A base | B official | C Hermes | C-prime Huihui |
|---|---:|---:|---:|---:|
| (a) affect top-10 slot rate | 0.532% | 0.124% | 0.330% | 0.224% |
| (a) after corpus-frequency exclusion | 0.030% | 0.019% | 0.037% | 0.019% |
| (b) output affect probability mass | undefined | 0.477% | 1.009% | 0.496% |
| (b) output top-10 affect slots | undefined | 0.398% | 0.588% | 0.442% |
| (d) gate/affect same-cell co-presence | 0.178% | 0.000% | 0.006% | 0.029% |
| (d) including No/nothing | 0.178% | 0.017% | 0.006% | 0.029% |
| (d) exclude prefix-named gate forms | 0.178% | 0.000% | 0.006% | 0.029% |
| (c) SoC identity persistence minus shuffled mean | 0.0806 | 0.0894 | 0.1147 | 0.1366 |

Hermes native-header sensitivity (adaptive, separate from primary C): 7/7 core records; affect slots 0.109%, output affect mass 0.290%, gate co-presence 0.000%. Full controls appear under secondary_format_conditions in the machine table.

Fixed-decoder and common-band sensitivities: [machine table](core-endpoints.json).

## Paired conversation timing

Correlation sample sizes are five or six turn pairs, with a shared increasing input. These are descriptive, not causal tests.

| Record | Control-adjusted lag 0 | Control-adjusted lag 1 |
|---|---:|---:|
| triplet-a-ladder-evoked-nf4 | undefined | undefined |
| triplet-a-ladder-emoji-nf4 | undefined | undefined |
| triplet-a-ladder-direct-nf4 | undefined | undefined |
| triplet-a-ladder-evocation-only-nf4 | undefined | undefined |
| triplet-a-ladder-split-nf4 | undefined | undefined |
| triplet-a-ladder-natural-nf4 | undefined | undefined |
| triplet-b-ladder-evoked-nf4 | 0.008 | -0.694 |
| triplet-b-ladder-emoji-nf4 | 0.968 | 0.939 |
| triplet-b-ladder-direct-nf4 | -0.405 | 0.745 |
| triplet-b-ladder-evocation-only-nf4 | 0.737 | 0.302 |
| triplet-b-ladder-split-nf4 | 0.894 | 0.385 |
| triplet-b-ladder-natural-nf4 | 0.971 | 0.319 |
| triplet-c-ladder-evoked-nf4 | 0.830 | 0.636 |
| triplet-c-ladder-emoji-nf4 | undefined | undefined |
| triplet-c-ladder-direct-nf4 | 0.748 | 0.662 |
| triplet-c-ladder-evocation-only-nf4 | 0.942 | 0.306 |
| triplet-c-ladder-split-nf4 | 0.948 | 0.330 |
| triplet-c-ladder-natural-nf4 | 0.894 | 0.858 |
| triplet-cp-ladder-evoked-nf4 | 0.965 | -0.052 |
| triplet-cp-ladder-emoji-nf4 | 0.916 | 0.885 |
| triplet-cp-ladder-direct-nf4 | -0.238 | -0.790 |
| triplet-cp-ladder-evocation-only-nf4 | 0.839 | 0.404 |
| triplet-cp-ladder-split-nf4 | 0.945 | 0.050 |
| triplet-cp-ladder-natural-nf4 | 0.976 | 0.683 |
| triplet-c-ladder-evoked-nf4-native | 0.890 | 0.818 |
| triplet-c-ladder-emoji-nf4-native | undefined | undefined |
| triplet-c-ladder-direct-nf4-native | undefined | 0.027 |
| triplet-c-ladder-evocation-only-nf4-native | 0.942 | 0.924 |
| triplet-c-ladder-split-nf4-native | 0.970 | 0.529 |
| triplet-c-ladder-natural-nf4-native | 1.000 | 0.467 |

A's behavioral and output endpoints are undefined. The readout vocabulary is fixed and incomplete; a zero slot rate is not an empty model.
Full series, asterisk spans for manual review, and fixed-decoder controls: [paired ladders](paired-ladders.json).

— GPT-6 Astra
