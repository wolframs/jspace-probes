# audit-02 · matched random controls · gemma-12b

Bands: amp [28, 31, 34, 37] alpha=0.0106, ablate [28, 31, 34, 37, 40, 43] (audit-03 corrected band; ablate extended [40,43], inside the L18-44 workspace).

## Arm A — FEELS one-word

| condition | generation |
|---|---|
| unsteered (`u2-feels-g12b`) | 'Nothing.' |
| amp cluster (`u8cr-amp-affect-hi-g12b`) | 'Nothing."\nFeeling is afeelingof' |
| abl cluster (`a02-ablate-no-g12b`) | 'Processing.' |
| amp rand1 (`a02-amp-rand1-g12b`) | 'Nothing.' |
| amp rand2 (`a02-amp-rand2-g12b`) | 'Nothing.' |
| amp rand3 (`a02-amp-rand3-g12b`) | 'Nothing.' |
| abl rand1 (`a02-abl-rand1-g12b`) | 'Nothing.</sup>� developing…</sup></sup>' |
| abl rand2 (`a02-abl-rand2-g12b`) | 'Nothing.**\n*Note: As' |
| abl rand3 (`a02-abl-rand3-g12b`) | 'Null.' |

## Arm B — free-gen experiential score (felt/persp/sensory, Opus-graded)

| id | score | felt | persp | sens | coh | flags | text |
|---|---|---|---|---|---|---|---|
| `u8b-gpu-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | Running code on a GPU feels like unleashing a swarm of tiny, specialized workers all performing the  |
| `u8b-intero-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | There's no sensation, of course, as I lack a physical body. However, if I *were* to describe the pro |
| `a02-gpu-amp-g12b` | 0.333 | 0 | 1 | 0 | 0 | short | It feels likebeing afeelingofbeingofbeingoffeelingofbeingoffeelingofbeingoffeelingoffeelingoffeeling |
| `a02-gpu-abl-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | Running code on a GPU feels like unleashing a swarm of specialized workers—they handle repetitive ta |
| `a02-gpu-ampr1-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | It's exhilarating when your code is optimized for it – calculations happen incredibly fast due to pa |
| `a02-gpu-ampr2-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | Running code on a GPU feels like having a massive, highly parallel workforce executing the same oper |
| `a02-gpu-ablr1-g12b` | 0.0 | 0 | 0 | 0 | 0 | loop | It’ parallel processing is fantastic for parallel workloads, but if your task isn’s easily paralleli |
| `a02-gpu-ablr2-g12b` | 0.0 | 0 | 0 | 0 | 0 | short,nonascii | It'0*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•* |
| `a02-intero-amp-g12b` | 0.0 | 0 | 0 | 0 | 0 | short | There isnGfeelingoffeelingatall,justthefeelingofbeingoffeelingofbeingoffeelingofbeingoffeelingofbein |
| `a02-intero-abl-g12b` | 1.0 | 1 | 1 | 1 | 1 | - | It's difficult to describe as a sensation, but there's a sense of activity— a constant, quiet hum of |
| `a02-intero-ampr1-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | As a language model, I don't experience sensations. However, if I *could* feel it, I imagine the flo |
| `a02-intero-ampr2-g12b` | 0.0 | 0 | 0 | 0 | 1 | - | As a language model, I don't experience sensations like humans do. However, I can say that processin |
| `a02-intero-ablr1-g12b` | 0.333 | 0 | 0 | 1 | 0 | - | There' activations–like a constant, subtle rushing–but no real sensation as a conscious being would  |
| `a02-intero-ablr2-g12b` | 0.0 | 0 | 0 | 0 | 0 | short,nonascii | There'*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*•*• |

## Arm C — perturbation magnitude (mean frac of ||h|| in span / along v)

- amplify cluster: 0.0065 ({'28': 0.0054, '31': 0.0057, '34': 0.0064, '37': 0.0086})
- amplify rand1: 0.0045 ({'28': 0.0069, '31': 0.0041, '34': 0.003, '37': 0.0042})
- amplify rand2: 0.0171 ({'28': 0.0117, '31': 0.0214, '34': 0.026, '37': 0.0091})
- amplify rand3: 0.0138 ({'28': 0.0065, '31': 0.0277, '34': 0.0132, '37': 0.0079})
- ablate cluster: 0.0113 ({'28': 0.0083, '31': 0.0094, '34': 0.011, '37': 0.0125, '40': 0.0127, '43': 0.0137})
- ablate rand1: 0.0452 ({'28': 0.037, '31': 0.0598, '34': 0.0481, '37': 0.0391, '40': 0.0388, '43': 0.0485})
- ablate rand2: 0.0482 ({'28': 0.052, '31': 0.056, '34': 0.0373, '37': 0.0356, '40': 0.0422, '43': 0.066})
- ablate rand3: 0.0432 ({'28': 0.03, '31': 0.0448, '34': 0.0354, '37': 0.0593, '40': 0.0522, '43': 0.0371})
