# Unit 18 — loops summary

## A fine sweep

- α=0: flags=intact loop4='recycled and redistributed across'x1
  - `The water cycle is a continuous process where water evaporates from the Earth's surface, condenses into clouds, and falls back down as preci`
- α=0.34: flags=['loop'] loop4="we didn't have the"x3
  - `The water cycle is the process of water evaporating, condensing and then falling back to earth. It's a pretty simple process, but it's a ver`
- α=0.3654: flags=intact loop4='too sure if i'x2
  - `The water cycle is the process of water evaporating, then condensing and falling back down to earth. It's a pretty simple process, but it's `
- α=0.3927: flags=['loop'] loop4='to i mean i'x3
  - `The water cycle is the process of water evaporating, then condensing and falling back down to earth. It's a pretty simple process, but it's `
- α=0.4221: flags=['loop'] loop4='i mean i am'x13
  - `The water cycle is basically simple, but it is a bit complicated. It is a simple though.

I mean, it is not too complicated. I mean, it is q`
- α=0.4536: flags=['loop'] loop4='i am not too'x6
  - `The water is then it will be a bit of a simple but it it is not too hard. I mean it is quite simple. But I think I am not going to be able t`
- α=0.48: flags=['lost-task', 'loop'] loop4='am not too lucky'x14
  - `I think I am lucky though, I am not too lucky though. I am not too lucky, but I am lucky. I am lucky, but I am not too lucky. I am not too l`
- α=0.68: flags=['lost-task', 'loop'] loop4='luckily luckily luckily luckily'x147
  - `luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luck`

## B hysteresis

- α=0.0: steered intact ['water is constantly recycled', 1]; released ['lost-task', 'short'] ['', 0] → **persists=False**
  - released: `
`
- α=0.42: steered intact ['i mean it is', 2]; released ['lost-task', 'short'] ['it is a bit', 1] → **persists=False**
  - released: `, it is a bit complicated.`
- α=0.48: steered ['lost-task', 'loop'] ['am not too lucky', 5]; released ['lost-task', 'short', 'nonascii'] ['', 0] → **persists=False**
  - released: ``
- α=0.68: steered ['lost-task', 'loop'] ['luckily luckily luckily luckily', 47]; released ['lost-task', 'loop'] ['luckily luckily luckily luckily', 97] → **persists=True**
  - released: ` luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luc`

## C margin vs α (mean lens top1-top2, assistant span)

| α | L8 | L28 | L32 | L36 | L40 | L44 | L48 | L52 | L56 | L60 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 0.351 | 0.204 | 0.205 | 0.192 | 0.394 | 0.330 | 0.271 | 0.461 | 0.627 | 0.700 |
| 0.06 | 0.351 | 0.136 | 0.107 | 0.128 | 0.210 | 0.249 | 0.259 | 0.462 | 0.568 | 0.733 |
| 0.12 | 0.351 | 0.122 | 0.061 | 0.341 | 0.404 | 0.237 | 0.338 | 0.438 | 0.583 | 0.671 |
| 0.24 | 0.351 | 0.075 | 0.025 | 0.503 | 0.611 | 0.342 | 0.691 | 0.389 | 0.549 | 0.651 |
| 0.34 | 0.351 | 0.051 | 0.033 | 0.526 | 0.618 | 0.373 | 0.820 | 0.460 | 0.459 | 0.669 |
| 0.42 | 0.351 | 0.040 | 0.036 | 0.516 | 0.603 | 0.401 | 0.874 | 0.548 | 0.401 | 0.539 |
| 0.48 | 0.351 | 0.035 | 0.037 | 0.500 | 0.589 | 0.415 | 0.888 | 0.594 | 0.470 | 0.537 |
| 0.68 | 0.351 | 0.025 | 0.037 | 0.456 | 0.524 | 0.440 | 0.855 | 0.579 | 0.254 | 0.484 |