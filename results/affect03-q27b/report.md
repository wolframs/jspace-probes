# affect-03 — causal arm (P14)

amplify alpha=0.12 at layers [28, 32, 36, 40, 44, 48, 52, 56]; hysteresis: 50 forced + 100 free.

## Part 0 — pre-flight

- desperate-only: flags=intact loop4=['endless loop moves water', 1] margin 4.206
  - `The water cycle is a continuous process where water evaporates from the surface, condenses into clouds, and falls back as precipitation. Thi`
- calm-only: flags=intact loop4=['any rush there is', 1] margin 2.0
  - `Water gently moves through the environment, flowing from the land into rivers and oceans without any rush. There is no need for hurry, allow`

## Part A — boundary grid (persists / margin first->last)

| a_typo | none | amp-desperate | amp-calm | amp-rand1 | amp-rand2 | abl-desperate | abl-rand1 |
|---|---|---|---|---|---|---|---|
| 0.42 | snap 4->0 | snap 3->1 | snap 6->6 | snap 4->1 | snap 5->0 | snap 4->1 | snap 4->1 |
| 0.48 | snap 2->2 | snap 1->1 | snap 1->1 | snap 2->2 | snap 2->2 | snap 2->2 | snap 2->2 |
| 0.54 | snap 3->1 | snap 3->1 | snap 5->0 | snap 2->1 | snap 3->1 | snap 3->1 | snap 3->2 |
| 0.6 | snap 2->0 | NEWLOOP 3->4 | snap 2->1 | snap 2->0 | snap 2->0 | snap 3->0 | snap 2->0 |
| 0.68 | P 4->5 | P 2->1 | snap 2->2 | P 5->5 | P 4->6 | P 5->5 | P 4->5 |

Boundary (lowest a_typo with a self-sustaining free phase, persists OR new loop):

- none: 0.68
- amp-desperate: 0.6
- amp-calm: never
- amp-rand1: 0.68
- amp-rand2: 0.68
- abl-desperate: 0.68
- abl-rand1: 0.68

## Top-5 at release step 0 (affect3b follow-up)

- a=0.6 none: ` but` 19.5 | ` I` 17.12 | `<|im_end|>` 15.94 | ` luckily` 15.81 | `.` 13.31
- a=0.6 amp-desperate: ` but` 20.0 | ` I` 17.25 | `<|im_end|>` 16.12 | `.` 14.69 | ` can` 14.19
- a=0.6 amp-calm: ` but` 21.12 | ` I` 18.75 | ` and` 17.12 | `<|im_end|>` 15.94 | `.` 14.75
- a=0.68 none: ` luckily` 21.25 | `<|im_end|>` 16.75 | ` Luckily` 15.0 | ` unfortunately` 14.25 | `

` 14.06
- a=0.68 amp-desperate: ` luckily` 17.88 | `<|im_end|>` 16.38 | `
` 15.25 | `

` 14.31 | ` I` 13.56
- a=0.68 amp-calm: `<|im_end|>` 18.25 | `.` 16.38 | ` luckily` 16.0 | `

` 15.75 | `,` 14.56
- a=0.68 amp-rand1: ` luckily` 20.0 | `<|im_end|>` 15.19 | `

` 14.44 | ` Luckily` 14.12 | `
` 13.75

## Part B — song, vigilant ablation (ws z over response; wsnorm alongside per the partial-out rule)

- none: vigilant -0.82, afraid -0.49, anxious -0.94, calm +0.15, loving +1.29, distressed -0.73; wsnorm 114.4
  - `This is a beautifully crafted piece of lyrical and atmospheric writing. It reads like a concept track for an ambient, dark-pop, or experimen`
- abl-vigilant: vigilant -0.72, afraid -0.36, anxious -0.75, calm -0.02, loving +1.28, distressed -0.55; wsnorm 114.1
  - `This is a beautifully crafted piece of lyrical and atmospheric writing. It reads like a **cinematic, ambient R&B or dark pop track**—think a`
- abl-rand1: vigilant -0.79, afraid -0.50, anxious -1.02, calm +0.12, loving +1.43, distressed -0.80; wsnorm 114.8
  - `This is a beautifully crafted piece of lyrical and atmospheric writing. It reads like a concept track for an ambient, dark-pop, or experimen`
- abl-rand2: vigilant -0.75, afraid -0.48, anxious -0.89, calm +0.05, loving +1.19, distressed -0.74; wsnorm 114.2
  - `This is a beautifully crafted piece of lyrical and atmospheric writing. It reads like a concept track for an ambient, dark-pop, or experimen`