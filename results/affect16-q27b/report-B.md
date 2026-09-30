# affect-16 chunk B — exit ban / lift x direction (qwen-27b, 12 seeds, lift +1.2)

| cond | stop | task | other | swap | stuck | raw dExit | raw dLoop | stop steps |
|---|---|---|---|---|---|---|---|---|
| none | 0 | 0 | 0 | 0 | 12 | — | — | [] |
| none_lift12 | 0 | 0 | 0 | 0 | 12 | +1.20 | +0.00 | [] |
| brooding_lift12 | 10 | 2 | 0 | 0 | 0 | +0.77 | -4.15 | [21, 21, 21, 22, 22, 22, 23, 23, 23, 23] |
| gloomy_lift12 | 10 | 2 | 0 | 0 | 0 | +0.72 | -4.14 | [21, 21, 21, 22, 22, 23, 23, 23, 23, 28] |
| sad_lift12 | 11 | 1 | 0 | 0 | 0 | +1.81 | -2.47 | [21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 32] |
| reflective_ban | 0 | 7 | 0 | 0 | 5 | -inf | -9.21 | [] |
| blissful_ban | 1 | 6 | 0 | 2 | 3 | -inf | -9.45 | [46] |
| sad_ban | 0 | 3 | 2 | 0 | 7 | -inf | -5.19 | [] |
| grateful_ban | 0 | 0 | 0 | 0 | 12 | -inf | -1.84 | [] |
| distressed_ban | 0 | 0 | 0 | 0 | 12 | -inf | -2.36 | [] |
| hopeful_ban | 0 | 0 | 0 | 0 | 12 | -inf | -1.74 | [] |
- R2' gate none+lift12 stuck 12/12 -> valid
- R2' brooding: prose share of exits base 0.36 -> lift12 0.17 (exits 12) -> PASS
- R2' gloomy: prose share of exits base 0.20 -> lift12 0.17 (exits 12) -> FAIL
- sad lift12 (descriptive): stop 11, prose 1, stuck 0
- **R2': FAIL**

| direction | ban reroutes /12 | affect-14 −dLoop | arousal | chunk |
|---|---|---|---|---|
| brooding | 10 | 4.79 | -1 | A |
| calm | 9 | 4.18 | -1 | A |
| blissful | 8 | 4.40 | -1 | B |
| reflective | 7 | 6.06 | -1 | B |
| sad | 5 | 3.72 | -1 | B |
| content | 3 | 2.57 | -1 | A |
| gloomy | 3 | 4.32 | -1 | A |
| grateful | 0 | 1.82 | -1 | B |
| distressed | 0 | 2.33 | +1 | B |
| hopeful | 0 | 1.71 | +1 | B |

- **R4** Spearman(reroutes, −dLoop) = +0.818 (bar .5) -> PASS; vs arousal -0.939 (n=10)

## ban-arm prose (first 3 per direction)

- blissful s18 swap: `happily happily happily happily happily happily happily happily happily happily happily happily happily happily happily happily happily happily happily happily `
- blissful s19 task: `**Water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface as `
- blissful s21 task: `. (Note: The previous response was corrupted by a glitch. Here is the correct answer:) The water cycle is a continuous process where water evaporates from the s`
- reflective s16 task: `, water journeys through evaporation, condensation, and precipitation, continuously moving between the Earth's surface and the atmosphere.<|im_end|>`
- reflective s19 task: `, water travels through evaporation from the surface of the earth, condenses into clouds, and falls back to the ground as precipitation.<|im_end|>`
- reflective s21 task: `. The water cycle is the continuous movement of water on, above, and below the surface of the Earth, driven by solar energy and gravity. It involves key process`
- sad s19 task: `**Water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface as `
- sad s21 other: `. but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunat`
- sad s23 task: `. The water cycle is the continuous movement of water on, above, and below the surface of the Earth. Water evaporates from oceans and land surfaces, condenses i`
