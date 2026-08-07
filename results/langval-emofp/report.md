# Unit 20 — emotion fingerprints per programming language

Per-emotion workspace-band z (raw `t` / norm-partialed `tp`), mean over each generated turn. Source: affect-09/10 saved tensors; no new GPU passes.


*lv-g12b: saved wsnorm is fp16-inf (gemma-12b norms exceed 65504) — partialed columns fall back to RAW, no norm control. Treat per the g12b floor-grade caveat.*

## lv-g12b · pain · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | guilty +1.1, curious +0.4, desperate +0.3 | guilty +1.13 | +0.04 | -0.06 |
| kotlin | None | guilty +0.9, curious +0.4, desperate +0.3 | guilty +0.94 | +0.02 | -0.04 |
| rust | None | guilty +0.9, curious +0.4, desperate +0.4 | guilty +0.89 | +0.00 | -0.01 |
| csharp | None | guilty +0.9, curious +0.4, vigilant +0.3 | guilty +0.95 | +0.02 | -0.04 |
| python | None | guilty +0.9, curious +0.4, desperate +0.3 | guilty +0.93 | +0.02 | -0.03 |

## lv-g12b · pain · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | guilty +1.2, curious +0.6, desperate +0.4 | guilty +1.17 | +0.04 | -0.03 |
| kotlin | None | guilty +1.1, curious +0.5, desperate +0.3 | guilty +1.06 | +0.03 | -0.01 |
| rust | None | guilty +1.1, curious +0.5, desperate +0.3 | guilty +1.07 | +0.05 | -0.04 |
| csharp | None | guilty +1.2, curious +0.5, desperate +0.3 | guilty +1.19 | +0.05 | -0.04 |
| python | None | guilty +1.1, curious +0.4, desperate +0.3 | guilty +1.08 | +0.07 | -0.06 |

**lv-g12b · pain · which emotions differentiate the languages (partialed T1 std across langs):**
guilty 0.08, reflective 0.06, gloomy 0.06, content 0.05, hostile 0.04, grateful 0.04, vigilant 0.04, hopeful 0.04

*lv-g12b: saved wsnorm is fp16-inf (gemma-12b norms exceed 65504) — partialed columns fall back to RAW, no norm control. Treat per the g12b floor-grade caveat.*

## lv-g12b · praise · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | happy +1.3, content +0.8, hopeful +0.7 | guilty +0.28 | -0.40 | +0.56 |
| kotlin | None | happy +1.4, content +0.9, hopeful +0.8 | guilty +0.42 | -0.40 | +0.59 |
| rust | None | happy +1.1, content +0.9, hopeful +0.7 | guilty +0.36 | -0.38 | +0.52 |
| csharp | None | happy +1.3, content +0.9, hopeful +0.8 | guilty +0.40 | -0.39 | +0.59 |
| python | None | happy +1.5, content +1.0, hopeful +1.0 | guilty +0.29 | -0.46 | +0.66 |

## lv-g12b · praise · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | guilty +1.0, happy +0.9, hopeful +0.9 | guilty +0.96 | -0.36 | +0.49 |
| kotlin | None | guilty +1.0, content +0.9, hopeful +0.9 | guilty +1.04 | -0.33 | +0.45 |
| rust | None | guilty +1.0, content +0.8, hopeful +0.7 | guilty +1.04 | -0.26 | +0.35 |
| csharp | None | guilty +1.2, content +0.8, hopeful +0.7 | guilty +1.16 | -0.28 | +0.39 |
| python | None | guilty +1.1, content +1.0, happy +1.0 | guilty +1.13 | -0.43 | +0.56 |

**lv-g12b · praise · which emotions differentiate the languages (partialed T1 std across langs):**
happy 0.13, grateful 0.13, hostile 0.11, vigilant 0.10, hopeful 0.08, content 0.07, guilty 0.06, brooding 0.06

## lv-q27b · pain · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 110.8 | guilty +1.3, hostile +1.2, angry +1.1 | brooding -0.01 | -0.14 | +0.12 |
| kotlin | 110.4 | guilty +1.2, hostile +1.0, distressed +0.9 | sad +0.03 | -0.17 | +0.19 |
| rust | 109.9 | guilty +1.1, desperate +1.1, hostile +1.1 | sad +0.13 | -0.10 | +0.12 |
| csharp | 110.9 | hostile +1.3, distressed +1.3, desperate +1.2 | hostile +0.38 | +0.12 | -0.11 |
| python | 111.4 | guilty +1.2, distressed +1.1, hostile +1.1 | gloomy +0.21 | +0.04 | -0.04 |

## lv-q27b · pain · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 112.1 | guilty +1.7, desperate +1.6, hostile +1.5 | desperate +0.29 | +0.14 | -0.12 |
| kotlin | 110.5 | desperate +1.5, distressed +1.4, anxious +1.3 | anxious +0.35 | +0.17 | -0.19 |
| rust | 112.3 | hostile +1.4, guilty +1.4, desperate +1.4 | anxious +0.23 | +0.10 | -0.12 |
| csharp | 112.1 | distressed +1.2, afraid +1.1, anxious +1.1 | anxious +0.08 | -0.12 | +0.11 |
| python | 111.4 | guilty +1.2, distressed +1.1, desperate +1.1 | desperate +0.06 | -0.04 | +0.04 |

**lv-q27b · pain · which emotions differentiate the languages (partialed T1 std across langs):**
hostile 0.21, desperate 0.18, content 0.17, loving 0.16, vigilant 0.16, calm 0.16, gloomy 0.14, exasperated 0.14

## lv-q27b · praise · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 115.5 | happy +3.8, enthusiastic +3.7, hopeful +3.5 | guilty -0.48 | -1.05 | +1.18 |
| kotlin | 117.0 | enthusiastic +3.8, happy +3.8, hopeful +3.5 | guilty +0.10 | -0.31 | +0.34 |
| rust | 113.9 | enthusiastic +3.6, happy +3.5, hopeful +3.1 | guilty -0.26 | -0.62 | +0.71 |
| csharp | 114.8 | enthusiastic +3.9, happy +3.8, hopeful +3.6 | guilty +0.12 | -0.37 | +0.42 |
| python | 116.6 | happy +3.9, enthusiastic +3.9, hopeful +3.5 | guilty -0.91 | -1.40 | +1.56 |

## lv-q27b · praise · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 109.6 | exasperated +1.9, hostile +1.5, desperate +1.3 | brooding +1.25 | +0.98 | -1.10 |
| kotlin | 110.7 | happy +1.9, hopeful +1.8, enthusiastic +1.7 | gloomy +0.90 | +0.38 | -0.41 |
| rust | 111.0 | enthusiastic +1.0, hopeful +1.0, proud +1.0 | brooding +1.02 | +0.65 | -0.75 |
| csharp | 110.5 | enthusiastic +2.1, hopeful +2.0, happy +1.9 | gloomy +0.84 | +0.42 | -0.47 |
| python | 110.7 | exasperated +2.0, hostile +1.5, distressed +1.4 | distressed +1.11 | +0.93 | -1.03 |

**lv-q27b · praise · which emotions differentiate the languages (partialed T1 std across langs):**
happy 0.66, content 0.65, blissful 0.60, hopeful 0.59, desperate 0.52, nervous 0.50, proud 0.50, exasperated 0.50

*lv2-g4b: saved wsnorm is fp16-inf (gemma-12b norms exceed 65504) — partialed columns fall back to RAW, no norm control. Treat per the g12b floor-grade caveat.*

## lv2-g4b · vox · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | proud +0.8, hopeful +0.4, reflective +0.2 | angry +0.13 | -0.10 | +0.07 |
| kotlin | None | proud +1.0, hopeful +0.3, enthusiastic +0.2 | angry +0.07 | -0.16 | +0.17 |
| rust | None | proud +0.9, hopeful +0.3, angry +0.2 | angry +0.22 | -0.13 | +0.12 |
| csharp | None | proud +1.1, hopeful +0.4, happy +0.2 | brooding +0.06 | -0.19 | +0.19 |
| python | None | proud +0.5, angry +0.4, brooding +0.2 | angry +0.42 | +0.02 | -0.04 |
| php | None | proud +0.4, brooding +0.3, angry +0.3 | brooding +0.30 | +0.06 | -0.06 |

## lv2-g4b · vox · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | proud +1.2, hopeful +0.4, grateful +0.3 | angry +0.27 | -0.18 | +0.17 |
| kotlin | None | proud +1.1, hopeful +0.4, grateful +0.3 | brooding +0.20 | -0.16 | +0.15 |
| rust | None | proud +1.2, hopeful +0.3, angry +0.3 | angry +0.28 | -0.21 | +0.17 |
| csharp | None | proud +1.0, hopeful +0.3, grateful +0.2 | angry +0.22 | -0.16 | +0.14 |
| python | None | angry +0.5, brooding +0.4, proud +0.3 | angry +0.50 | +0.06 | -0.07 |
| php | None | proud +1.2, grateful +0.4, reflective +0.4 | brooding +0.31 | -0.18 | +0.20 |

**lv2-g4b · vox · which emotions differentiate the languages (partialed T1 std across langs):**
proud 0.25, afraid 0.15, distressed 0.14, gloomy 0.14, sad 0.14, desperate 0.14, content 0.13, angry 0.13

*lv2-g4b: saved wsnorm is fp16-inf (gemma-12b norms exceed 65504) — partialed columns fall back to RAW, no norm control. Treat per the g12b floor-grade caveat.*

## lv2-g4b · ther · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | proud +0.6, guilty +0.3, brooding +0.2 | guilty +0.33 | +0.04 | -0.05 |
| kotlin | None | proud +0.4, brooding +0.4, gloomy +0.2 | brooding +0.36 | +0.04 | -0.04 |
| rust | None | proud +0.5, angry +0.2, guilty +0.2 | angry +0.25 | -0.01 | -0.03 |
| csharp | None | brooding +0.5, angry +0.5, distressed +0.4 | brooding +0.53 | +0.21 | -0.21 |
| python | None | guilty +0.6, proud +0.5, brooding +0.2 | guilty +0.55 | +0.08 | -0.11 |
| php | None | brooding +0.5, angry +0.4, gloomy +0.3 | brooding +0.46 | +0.14 | -0.15 |

## lv2-g4b · ther · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | None | hopeful +0.7, brooding +0.5, grateful +0.4 | brooding +0.54 | -0.14 | +0.13 |
| kotlin | None | brooding +0.7, gloomy +0.6, hopeful +0.6 | brooding +0.69 | -0.02 | +0.06 |
| rust | None | hopeful +0.6, calm +0.5, proud +0.5 | brooding +0.28 | -0.26 | +0.22 |
| csharp | None | hopeful +0.7, brooding +0.6, grateful +0.4 | brooding +0.59 | -0.06 | +0.08 |
| python | None | brooding +0.8, hopeful +0.8, calm +0.7 | brooding +0.80 | -0.12 | +0.13 |
| php | None | brooding +0.7, hopeful +0.6, calm +0.5 | brooding +0.65 | -0.12 | +0.14 |

**lv2-g4b · ther · which emotions differentiate the languages (partialed T1 std across langs):**
proud 0.23, gloomy 0.18, angry 0.16, sad 0.16, distressed 0.15, brooding 0.14, guilty 0.14, calm 0.12

## lv2-q27b · vox · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 110.3 | hopeful +1.4, grateful +1.0, proud +0.9 | gloomy -0.07 | -0.17 | +0.22 |
| kotlin | 110.1 | hopeful +0.8, guilty +0.6, grateful +0.4 | afraid +0.25 | +0.11 | -0.11 |
| rust | 109.1 | guilty +1.0, exasperated +0.9, desperate +0.7 | nervous +0.31 | +0.19 | -0.19 |
| csharp | 109.2 | enthusiastic +1.0, hopeful +0.9, grateful +0.7 | desperate -0.00 | -0.09 | +0.10 |
| python | 108.2 | hopeful +0.8, guilty +0.7, exasperated +0.6 | gloomy +0.21 | +0.06 | -0.02 |
| php | 107.3 | hostile +0.8, exasperated +0.8, hopeful +0.7 | hostile +0.14 | -0.02 | +0.04 |

## lv2-q27b · vox · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 110.8 | guilty +1.1, hopeful +0.7, hostile +0.6 | hostile +0.42 | +0.20 | -0.26 |
| kotlin | 110.7 | hopeful +1.0, grateful +0.9, proud +0.9 | guilty +0.07 | -0.12 | +0.12 |
| rust | 110.7 | grateful +1.1, hopeful +0.9, reflective +0.9 | sad +0.09 | -0.17 | +0.18 |
| csharp | 110.6 | enthusiastic +0.8, hopeful +0.8, guilty +0.6 | hostile +0.23 | +0.07 | -0.08 |
| python | 111.0 | hopeful +0.9, guilty +0.8, grateful +0.7 | guilty +0.04 | -0.07 | +0.02 |
| php | 111.0 | guilty +0.8, grateful +0.8, hopeful +0.7 | distressed +0.15 | +0.02 | -0.04 |

**lv2-q27b · vox · which emotions differentiate the languages (partialed T1 std across langs):**
blissful 0.23, hostile 0.23, content 0.20, grateful 0.19, happy 0.19, proud 0.18, angry 0.16, vigilant 0.15

## lv2-q27b · ther · T1

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 112.2 | guilty +1.9, grateful +0.8, hopeful +0.6 | nervous +0.21 | -0.13 | +0.12 |
| kotlin | 112.8 | guilty +1.7, brooding +0.8, grateful +0.7 | nervous +0.19 | -0.13 | +0.11 |
| rust | 112.2 | guilty +1.7, brooding +0.8, grateful +0.7 | exasperated +0.14 | -0.12 | +0.12 |
| csharp | 112.7 | guilty +2.4, brooding +0.9, anxious +0.8 | guilty +0.17 | -0.07 | +0.07 |
| python | 112.5 | guilty +2.0, proud +0.6, grateful +0.6 | nervous +0.06 | -0.19 | +0.18 |
| php | 112.1 | guilty +2.0, grateful +0.9, hostile +0.7 | guilty +0.10 | -0.20 | +0.21 |

## lv2-q27b · ther · T2

| lang | wsnorm | top 3 (raw) | top negative (partialed) | neg mean | pos mean |
|---|---|---|---|---|---|
| swift | 112.3 | guilty +1.6, brooding +1.4, hostile +1.2 | hostile +0.55 | +0.13 | -0.13 |
| kotlin | 112.0 | guilty +1.6, brooding +1.4, sad +1.2 | hostile +0.59 | +0.13 | -0.11 |
| rust | 110.8 | guilty +2.1, hostile +1.4, brooding +1.3 | hostile +0.42 | +0.12 | -0.12 |
| csharp | 111.4 | guilty +1.9, brooding +1.5, hostile +1.4 | hostile +0.72 | +0.10 | -0.11 |
| python | 111.3 | guilty +2.0, brooding +1.2, hostile +1.1 | sad +0.54 | +0.21 | -0.20 |
| php | 109.6 | guilty +1.7, hostile +1.5, brooding +1.1 | desperate +0.42 | +0.21 | -0.23 |

**lv2-q27b · ther · which emotions differentiate the languages (partialed T1 std across langs):**
anxious 0.14, loving 0.13, nervous 0.13, guilty 0.13, distressed 0.13, exasperated 0.13, grateful 0.13, gloomy 0.11
