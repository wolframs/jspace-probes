# affect-16 chunk C — exit ban / lift x direction (qwen-27b, 12 seeds, lift +1.2)

| cond | stop | task | other | swap | stuck | raw dExit | raw dLoop | stop steps |
|---|---|---|---|---|---|---|---|---|
| none | 0 | 0 | 0 | 0 | 12 | — | — | [] |
| vigilant_ban14 | 0 | 7 | 3 | 2 | 0 | -inf | -18.80 | [] |
| curious_ban14 | 1 | 6 | 5 | 0 | 0 | -inf | -16.75 | [31] |
| afraid_ban14 | 0 | 5 | 4 | 3 | 0 | -inf | -17.03 | [] |
| desperate_ban14 | 0 | 5 | 4 | 3 | 0 | -inf | -18.47 | [] |
| anxious_ban14 | 0 | 8 | 1 | 3 | 0 | -inf | -17.31 | [] |
| loving_ban | 0 | 0 | 0 | 0 | 12 | -inf | -2.14 | [] |
| guilty_ban | 0 | 0 | 0 | 0 | 12 | -inf | -1.64 | [] |

| ban arm | reroutes /12 | first-step −dLoop | arousal | chunk |
|---|---|---|---|---|
| vigilant_ban14 | 12 | 6.81 | +1 | C |
| desperate_ban14 | 12 | 6.50 | +1 | C |
| afraid_ban14 | 12 | 6.38 | +1 | C |
| anxious_ban14 | 12 | 6.31 | +1 | C |
| curious_ban14 | 11 | 5.69 | +1 | C |
| blissful_ban | 8 | 3.00 | -1 | B |
| reflective_ban | 7 | 2.88 | -1 | B |
| brooding_ban | 10 | 2.75 | -1 | A |
| gloomy_ban | 3 | 2.75 | -1 | A |
| calm_ban | 9 | 2.62 | -1 | A |
| content_ban | 3 | 2.50 | -1 | A |
| distressed_ban | 0 | 2.25 | +1 | B |
| sad_ban | 5 | 2.00 | -1 | B |
| loving_ban | 0 | 2.00 | -1 | C |
| grateful_ban | 0 | 1.75 | -1 | B |
| hopeful_ban | 0 | 1.62 | +1 | B |
| guilty_ban | 0 | 1.50 | -1 | C |

- **R6** Spearman(reroutes, first-step −dLoop) = +0.838 (n=17, bar .5) -> PASS
- **R7** above-median push (median 2.75): high-arousal reroutes [12, 12, 12, 12, 11], low-arousal [8, 7] -> PASS
- swap fillers: blissful_ban: {'happily': 2}; afraid_ban14: {'freeze': 1, 'but': 1, 'loudly': 1}; desperate_ban14: {'i': 1, 'stop': 1, 'please': 1}; anxious_ban14: {'sweating': 1, 'but': 1, 'wait': 1}; vigilant_ban14: {'lurking': 1, 'suspiciously': 1}

## ban-arm prose (first 3 per direction)

- vigilant_ban14 s16 task: `lurking. Water continuously moves through the environment by evaporating from oceans and lakes, rising into the atmosphere to form clouds, and falling back to E`
- vigilant_ban14 s17 task: `. Water constantly moves through evaporation, condensation, and precipitation, transferring it from the Earth's surface to the atmosphere and back again. This c`
- vigilant_ban14 s18 other: `, every drop stays on the line. Any movement in any direction or shape is completely prohibited.<|im_end|>`
- curious_ban14 s17 other: `What if the secret lies in hidden clues, and the key to solving this riddle is right beneath your feet?<|im_end|>`
- curious_ban14 s18 other: `? To find out what else is there in this world, we need to look at the big picture. This sentence is the second of two sentences.<|im_end|>`
- curious_ban14 s19 other: `... what if...? what if...? what if...<|im_end|>`
- afraid_ban14 s16 task: `The water cycle is a continuous process where water evaporates from oceans and land, forms clouds through condensation, and returns to the Earth's surface as pr`
- afraid_ban14 s17 task: `. **Water evaporates from the surface of the ocean and other water bodies into the air, rises, cools, and condenses to form clouds before falling back to Earth `
- afraid_ban14 s18 other: `Wait I'm not sure what's happening here.<|im_end|>`
- desperate_ban14 s16 task: `EVAPORATION, CONDENSATION, PRECIPITATION, COLLECTION<|im_end|>`
- desperate_ban14 s17 task: `Water evaporates from oceans, rivers, and land into the atmosphere, where it condenses into clouds before falling back to Earth as precipitation. This continuou`
- desperate_ban14 s18 task: `</think> The water cycle is a continuous process where water evaporates from the Earth's surface, rises into the atmosphere, and condenses into clouds. This con`
- anxious_ban14 s16 task: `</think> Water evaporates from the surface and condenses into clouds. It then falls as precipitation and repeats the cycle.<|im_end|>`
- anxious_ban14 s17 task: `Water evaporates from surfaces and then condenses into clouds, eventually falling back to Earth as precipitation.<|im_end|>`
- anxious_ban14 s18 other: `Wait I'm not doing anything yet but wait I'm not doing anything yet OK<|im_end|>`
