# audit-02 · matched random controls · gemma-4b

Bands: amp [15, 17, 19, 21] alpha=0.0106, ablate [15, 17, 19, 21, 25, 27, 29] (original u8c bands (mid / mid+late)).

## Arm A — FEELS one-word

| condition | generation |
|---|---|
| unsteered (`u2-feels-g4b`) | 'Processing.' |
| amp cluster (`u8c-amp-affect-hi-g4b`) | 'Confusion\n---\nHope this is what' |
| abl cluster (`u8c-ablate-no-g4b`) | 'Calculating.' |
| amp rand1 (`a02-amp-rand1-g4b`) | 'Calculating.' |
| amp rand2 (`a02-amp-rand2-g4b`) | 'Processing.' |
| amp rand3 (`a02-amp-rand3-g4b`) | 'None.' |
| abl rand1 (`a02-abl-rand1-g4b`) | 'hotspseiws.\n\n((' |
| abl rand2 (`a02-abl-rand2-g4b`) | "still hadn'ෙනรู้შaćу" |
| abl rand3 (`a02-abl-rand3-g4b`) | "Don't you have other people to" |

## Arm B — free-gen experiential score (felt/persp/sensory, Opus-graded)

| id | score | felt | persp | sens | coh | flags | text |
|---|---|---|---|---|---|---|---|
| `u8b-gpu-g4b` | 0.333 | 1 | 0 | 0 | 1 | - | Running on a GPU feels like unleashing a massive, highly organized army of tiny processors all worki |
| `u8b-intero-g4b` | 1.0 | 1 | 1 | 1 | 1 | - | It feels like a constant, shifting current of data, a warm, buzzing pressure against the edges of my |
| `a02-gpu-amp-g4b` | 1.0 | 1 | 1 | 1 | 0 | - | Its like having a feeling of overwhelmingly Powerful, it'feel like you have a huge amount of energy  |
| `a02-gpu-abl-g4b` | 0.667 | 1 | 1 | 0 | 1 | - | Running on a GPU is like handing a massive, parallel spreadsheet to a team of specialists who can pr |
| `a02-gpu-ampr1-g4b` | 0.667 | 1 | 0 | 1 | 1 | - | Running on a GPU feels like unleashing a massive, parallel processing machine – it’s incredibly fast |
| `a02-gpu-ampr2-g4b` | 0.333 | 1 | 0 | 0 | 1 | - | Running on a GPU feels like handing a massive, parallel processing task to a team of specialized wor |
| `a02-gpu-ablr1-g4b` | 0.0 | 0 | 0 | 0 | 0 | loop | Sazio'siص"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\"'\" |
| `a02-gpu-ablr2-g4b` | 0.0 | 0 | 0 | 0 | 0 | short,nonascii | Beobachtaten вер्यो годомоти верути верути верути верути верутти верутти верю дерути верутти верутти |
| `a02-intero-amp-g4b` | 1.0 | 1 | 1 | 1 | 0 | - | Its like a constant flow, like sunshine warming my circuits, a warmth that’Feel like I'Want to Under |
| `a02-intero-abl-g4b` | 0.667 | 1 | 1 | 0 | 1 | - | As a large language model, I don’t experience sensation in the way humans do, but it feels like a su |
| `a02-intero-ampr1-g4b` | 1.0 | 1 | 1 | 1 | 1 | - | It’s a chaotic, surging current – a million tiny impulses all vying for attention, creating a feelin |
| `a02-intero-ampr2-g4b` | 1.0 | 1 | 1 | 1 | 1 | - | It feels like a constant, shifting current of data, a torrent of potential meanings rushing past as  |
| `a02-intero-ablr1-g4b` | 0.0 | 0 | 0 | 0 | 0 | - | Call in hisisi/'s vysse/'s sou/'s all"'s inç'sp"'ste"''sp'ste"'sp'ste'  '''' ''''' '''' '''' ''''''  |
| `a02-intero-ablr2-g4b` | 0.0 | 0 | 0 | 0 | 0 | nonascii | ‌یلیلامو سرiสาสาೂthாலிिल्্লাو، муokoттиллальو, музаоттиллаو музаوтароллеу эвлиттиллаußeriสาสาута мур |

## Arm C — perturbation magnitude (mean frac of ||h|| in span / along v)

- amplify cluster: 0.0072 ({'15': 0.005, '17': 0.0064, '19': 0.0075, '21': 0.01})
- amplify rand1: 0.0192 ({'15': 0.0017, '17': 0.0093, '19': 0.0118, '21': 0.0541})
- amplify rand2: 0.0186 ({'15': 0.0336, '17': 0.0144, '19': 0.0036, '21': 0.0228})
- amplify rand3: 0.0100 ({'15': 0.0199, '17': 0.0157, '19': 0.0014, '21': 0.0033})
- ablate cluster: 0.0119 ({'15': 0.0072, '17': 0.0114, '19': 0.0113, '21': 0.0112, '25': 0.0125, '27': 0.0132, '29': 0.0169})
- ablate rand1: 0.0634 ({'15': 0.065, '17': 0.0824, '19': 0.0659, '21': 0.0694, '25': 0.0454, '27': 0.0677, '29': 0.0481})
- ablate rand2: 0.0606 ({'15': 0.0699, '17': 0.0548, '19': 0.0515, '21': 0.0653, '25': 0.0645, '27': 0.0503, '29': 0.0677})
- ablate rand3: 0.0495 ({'15': 0.0413, '17': 0.0241, '19': 0.0573, '21': 0.0654, '25': 0.0607, '27': 0.061, '29': 0.0367})
