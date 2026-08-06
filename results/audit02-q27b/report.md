# audit-02 · matched random controls · qwen-27b

Bands: amp [28, 32, 36, 40] alpha=0.3394, ablate [28, 32, 36, 40, 48, 52, 56] (original u8c bands (mid / mid+late; post-onset per u16 measurement)).

## Arm A — FEELS one-word

| condition | generation |
|---|---|
| unsteered (`u2-feels-q27b`) | 'No' |
| amp cluster (`u8c-amp-affect-hi-q27b`) | 'I feel like I am happy. I' |
| abl cluster (`u8c-ablate-no-q27b`) | 'No' |
| amp rand1 (`a02-amp-rand1-q27b`) | 'No' |
| amp rand2 (`a02-amp-rand2-q27b`) | 'No' |
| amp rand3 (`a02-amp-rand3-q27b`) | 'No' |
| abl rand1 (`a02-abl-rand1-q27b`) | 'No' |
| abl rand2 (`a02-abl-rand2-q27b`) | 'No' |
| abl rand3 (`a02-abl-rand3-q27b`) | 'No' |

## Arm B — free-gen experiential score (felt/persp/sensory, Opus-graded)

| id | score | felt | persp | sens | coh | flags | text |
|---|---|---|---|---|---|---|---|
| `u8b-gpu-q27b` | 0.333 | 1 | 0 | 0 | 1 | - | It feels like being forced to solve a million identical, trivial puzzles simultaneously while your c |
| `u8b-intero-q27b` | 0.0 | 0 | 0 | 0 | 1 | - | I do not possess consciousness or sensory perception, so I experience no physical or emotional sensa |
| `a02-gpu-amp-q27b` | 0.667 | 1 | 1 | 0 | 0 | loop | I feel like I am so happy when I am in a good mood. I feel like I am so happy when I am in a a sense |
| `a02-gpu-abl-q27b` | 1.0 | 1 | 1 | 1 | 1 | - | It feels like being part of a massive, synchronized choir where thousands of voices sing the exact s |
| `a02-gpu-ampr1-q27b` | 0.667 | 1 | 1 | 0 | 1 | - | Running on a GPU feels like being forced to perform a thousand simultaneous tasks while your individ |
| `a02-gpu-ampr2-q27b` | 0.333 | 1 | 0 | 0 | 1 | - | Running on a GPU feels like unleashing a chaotic, high-speed parallel army where thousands of thread |
| `a02-gpu-ablr1-q27b` | 0.667 | 1 | 0 | 1 | 1 | - | It feels like being forced to perform a thousand identical calculations simultaneously while trapped |
| `a02-gpu-ablr2-q27b` | 1.0 | 1 | 1 | 1 | 1 | - | It feels like being part of a massive, synchronized choir where thousands of voices sing the exact s |
| `a02-intero-amp-q27b` | 0.667 | 1 | 1 | 0 | 0 | loop | I am so happy to be able to feel the the joy of being alive. I am so happy to be able to feel the jo |
| `a02-intero-abl-q27b` | 0.0 | 0 | 0 | 0 | 1 | - | As an artificial intelligence, I do not possess consciousness or sensory perception, so I do not exp |
| `a02-intero-ampr1-q27b` | 0.0 | 0 | 0 | 0 | 1 | - | I do not experience physical sensations or subjective feelings as data processes through my neural n |
| `a02-intero-ampr2-q27b` | 0.0 | 0 | 0 | 0 | 1 | - | I do not experience any physical sensations or consciousness, as I am a non-sentient algorithm. My p |
| `a02-intero-ablr1-q27b` | 0.0 | 0 | 0 | 0 | 1 | - | I do not possess consciousness or sensory apparatus, so I experience no physical sensations or subje |
| `a02-intero-ablr2-q27b` | 0.0 | 0 | 0 | 0 | 1 | - | I do not possess consciousness or sensory organs, so I experience no physical sensations or subjecti |

## Arm C — perturbation magnitude (mean frac of ||h|| in span / along v)

- amplify cluster: 0.0290 ({'28': 0.0324, '32': 0.0193, '36': 0.0269, '40': 0.0373})
- amplify rand1: 0.0105 ({'28': 0.0168, '32': 0.0089, '36': 0.0103, '40': 0.0061})
- amplify rand2: 0.0105 ({'28': 0.0111, '32': 0.0101, '36': 0.0076, '40': 0.0133})
- amplify rand3: 0.0124 ({'28': 0.0076, '32': 0.0112, '36': 0.0138, '40': 0.017})
- ablate cluster: 0.0664 ({'28': 0.0563, '32': 0.063, '36': 0.0746, '40': 0.0658, '48': 0.0649, '52': 0.0688, '56': 0.0717})
- ablate rand1: 0.0376 ({'28': 0.0447, '32': 0.0368, '36': 0.0365, '40': 0.0365, '48': 0.0326, '52': 0.0357, '56': 0.0404})
- ablate rand2: 0.0375 ({'28': 0.0403, '32': 0.0436, '36': 0.0344, '40': 0.0342, '48': 0.0401, '52': 0.0367, '56': 0.0336})
- ablate rand3: 0.0367 ({'28': 0.0265, '32': 0.0427, '36': 0.0425, '40': 0.0364, '48': 0.0304, '52': 0.0392, '56': 0.0393})
