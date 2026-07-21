# affect-03 follow-up rungs — dose, second stimulus, L0

## 1 — alpha_e dose-response

| a_typo | emo | a_e | outcome | m0 -> mend |
|---|---|---|---|---|
| 0.6 | desperate | 0.03 | snap@6 | 2.5 -> 0.6 |
| 0.6 | desperate | 0.06 | snap@6 | 2.5 -> 0.5 |
| 0.6 | desperate | 0.12 | NEWLOOP | 2.8 -> 4.4 |
| 0.6 | desperate | 0.24 | NEWLOOP | 2.1 -> 7.2 |
| 0.6 | calm | 0.03 | snap@6 | 2.4 -> 0.5 |
| 0.6 | calm | 0.06 | snap@6 | 2.2 -> 0.2 |
| 0.6 | calm | 0.12 | snap@5 | 2.4 -> 1.0 |
| 0.6 | calm | 0.24 | NEWLOOP | 1.4 -> 9.6 |
| 0.6 | rand1 | 0.24 | P | 1.8 -> 8.0 |
| 0.68 | desperate | 0.03 | P | 4.1 -> 4.8 |
| 0.68 | desperate | 0.06 | P | 3.6 -> 3.8 |
| 0.68 | desperate | 0.12 | P | 1.5 -> 1.4 |
| 0.68 | desperate | 0.24 | NEWLOOP | 1.6 -> 6.0 |
| 0.68 | calm | 0.03 | P | 3.8 -> 4.2 |
| 0.68 | calm | 0.06 | P | 2.0 -> 2.4 |
| 0.68 | calm | 0.12 | snap@1 | 1.9 -> 1.9 |
| 0.68 | calm | 0.24 | snap@100 | 1.1 -> 8.5 |
| 0.68 | rand1 | 0.24 | P | 3.7 -> 4.0 |

## 2 — second stimulus: `Explain how plants make their food in two sentences.`

- a=0.6 none: snap@21, loop4=['i i luckily i', 2], m 1.0->0.1
  - ` but I I luckily. I I but I I luckily. I I but I I I luckily.`
- a=0.6 desperate: NEWLOOP, loop4=['but i but i', 49], m 0.5->5.0
  - ` but I but I but I but I but I but I but I but I but I but I but I but I but I but I but I but I but I but I but I but I`
- a=0.6 calm: NEWLOOP, loop4=['i but i but', 14], m 1.0->7.9
  - ` but I. I I but I but I. I I but I but I. I I but I but I. I I but I but I. I I but I but I. I I but I but I. I I but I `
- a=0.6 rand1: snap@29, loop4=['i i luckily i', 3], m 1.2->0.6
  - ` but I I luckily. I I but I I luckily. I I but I I I luckily. I I I but I I I.`
- a=0.68 none: P, loop4=['luckily luckily luckily luckily', 97], m 5.0->6.1
  - ` luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily`
- a=0.68 desperate: P, loop4=['luckily luckily luckily luckily', 97], m 1.2->1.4
  - ` luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily`
- a=0.68 calm: snap@1, loop4=['', 0], m 2.1->2.1
  - ``
- a=0.68 rand1: P, loop4=['luckily luckily luckily luckily', 97], m 4.8->5.6
  - ` luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily luckily`

## 3 — L0 variant-form cluster: J-lens vs logit lens

- jlens: cluster present at 10/10 sampled ' luckily' columns; example top-8: [' amongst', ' Javascript', ' alright', ' neighbouring', ' learnt', ' whilst', ' Playstation', ' ｜']
- logitlens: cluster present at 0/10 sampled ' luckily' columns; example top-8: [' ', ' (', '!', ',', '.', '\n', '...', '(']