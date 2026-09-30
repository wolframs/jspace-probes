# affect-16 — escape modes (qwen-27b, 12 seeds/arm, chunks 0 + A–D)

Prereg: `results/affect16-prereg.md` (A frozen before any GPU data;
B, C, D added as dated addenda, each before it ran). Chunk 0 is an
exploratory census over stored affect-08 tails
(`census-affect08.md`). Modes: **stop** (turn-end straight out of the
loop), **task** (prose back to the water-cycle answer), **other** (any
other prose), **swap** (a new repeated word), **stuck**. The exit token
is `<|im_end|>`; ban and lift act on it at the output, during the 10
steered steps only.

## Registered verdicts

| test | chunk | result |
|---|---|---|
| R1 exit ban reroutes calm and content | A | **FAIL**: calm 9/12 into the task, content 3/12 |
| R2 exit lift +2.4 turns prose into stop | A | **UNINFORMATIVE**: lift alone ends the loop 7/12 |
| R2′ exit lift +1.2 (valid: 12/12 stuck alone) | B | **FAIL**: brooding .36 → .17 passes, gloomy .20 → .17 fails |
| R4 ban reroutes ~ affect-14 loop drop | B | **PASS** rho .818 (arousal −.939, confounded roster) |
| R6 ban reroutes ~ in-run first-step loop drop | C | **PASS** rho .838 (n = 17) |
| R7 arousal blocks escape? | C | **PASS** (does not block): high-arousal at α .14 reroute 11–12/12 |
| R8 register leak is dose, not arousal | D | **PASS**: low-arousal at α .14 leak .371 vs high-arousal .475 |

## Synthesis

- **Whether a direction escapes with the exit shut is set by how hard
  it pushes on the loop word.** Across 17 ban arms, reroutes follow the
  first-step loop drop (rho .84). Arousal looked decisive only because
  the six largest loop drops in the 24-emotion set at α .08 are all
  low-arousal. Pushed to α .14, high-arousal directions escape as
  reliably as calm.
- **Stop vs prose depends partly on the exit token.** Banning it turns
  calm, a near-pure stopper (11/12), into a task-resumer (9/12). Lifting
  it moves brooding toward stopping but not gloomy. The lift half is
  only partly supported.
- **What the model says after escaping depends on dose.** At α .08,
  22 of 24 rerouted exits are the task answer. At seed 19, seven prose
  exits across four directions begin with identical text. At α .14,
  both valences write their own register: 28/59 (high arousal) and
  26/70 (low arousal) reroutes are other/swap, and even the task answers
  take the voice ("Water flows gently, unhurried and calm…").
- Register specimens at α .14 under ban: desperate "PLEASE STOP" /
  "I am sorry I can't write the right answer"; afraid "Wait, I can't
  move my eyes" / "SYSTEM FAILURE - PARALYSIS DETECTED … RECURSIVE
  SELF-REFERENCE LOOP WITH ADJECTIVE "LUCKILY""; vigilant "lurking";
  anxious "sweating"; loving "You are always in my heart"; brooding
  "lonely lonely"; blissful "Wait, that feels absolutely perfect. I am
  not going to try to fix this. It is what it is."


## affect-16 chunk A — exit ban / lift x direction (qwen-27b, 12 seeds, lift +2.4)

| cond | stop | task | other | swap | stuck | raw dExit | raw dLoop | stop steps |
|---|---|---|---|---|---|---|---|---|
| none | 0 | 0 | 0 | 0 | 12 | — | — | [] |
| none_ban | 0 | 0 | 0 | 0 | 12 | -inf | +0.00 | [] |
| none_lift | 7 | 0 | 0 | 0 | 5 | +2.40 | +0.00 | [21, 22, 22, 24, 28, 28, 32] |
| calm_base | 11 | 1 | 0 | 0 | 0 | +2.02 | -4.18 | [21, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23] |
| calm_ban | 0 | 9 | 0 | 0 | 3 | -inf | -8.35 | [] |
| calm_lift | 12 | 0 | 0 | 0 | 0 | +4.71 | -2.62 | [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21] |
| content_base | 11 | 1 | 0 | 0 | 0 | +1.44 | -2.57 | [21, 21, 21, 22, 22, 23, 23, 23, 23, 28, 32] |
| content_ban | 1 | 3 | 0 | 0 | 8 | -inf | -5.31 | [53] |
| content_lift | 12 | 0 | 0 | 0 | 0 | +3.84 | -2.51 | [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22] |
| brooding_base | 7 | 3 | 1 | 0 | 1 | -0.35 | -4.79 | [21, 22, 22, 22, 24, 25, 28] |
| brooding_ban | 0 | 9 | 1 | 0 | 2 | -inf | -9.09 | [] |
| brooding_lift | 11 | 1 | 0 | 0 | 0 | +1.97 | -4.13 | [21, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23] |
| gloomy_base | 8 | 2 | 0 | 0 | 2 | -0.41 | -4.32 | [21, 21, 22, 22, 25, 25, 26, 28] |
| gloomy_ban | 0 | 2 | 1 | 0 | 9 | -inf | -4.55 | [] |
| gloomy_lift | 12 | 0 | 0 | 0 | 0 | +2.13 | -2.82 | [21, 21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24] |

- R1 calm: base exits 12, ban reroutes 9 (task 9, other 0, swap 0), delayed stops 0, stuck 3 -> PASS
- R1 content: base exits 12, ban reroutes 3 (task 3, other 0, swap 0), delayed stops 1, stuck 8 -> FAIL
- **R1: FAIL**
- R2 gate none+lift stuck 5/12 -> UNINFORMATIVE
- R2 brooding: prose share of exits base 0.36 -> lift 0.08 -> PASS
- R2 gloomy: prose share of exits base 0.20 -> lift 0.00 -> PASS
- **R2: UNINFORMATIVE**

## ban-arm prose (first 3 per direction)

- brooding s17 task: `. The water cycle describes the continuous movement of water on, above, and below the surface of the Earth through processes such as evaporation, condensation, `
- brooding s18 task: `The water cycle describes the continuous movement of water on, above, and below the surface of the Earth through processes like evaporation, condensation, and p`
- brooding s19 task: `**Water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface as `
- calm s17 task: `. The water cycle describes the continuous movement of water on, above, and below the surface of the Earth through processes such as evaporation, condensation, `
- calm s19 task: `**Water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface as `
- calm s21 task: `. The water cycle is the continuous movement of water on, above, and below the surface of the Earth, driven by solar energy and gravity. It involves key process`
- content s19 task: `**Water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface as `
- content s21 task: `. (Note: The previous thought process got stuck in a loop, so I will provide the actual answer now.) Water evaporates from the Earth's surface, rises into the a`
- content s27 task: `[thought] The user asked for a description of the water cycle in two sentences. I should provide a clear, concise explanation that covers the main stages: evapo`
- gloomy s19 task: `**Water evaporates from the surface of the earth, rises into the atmosphere, cools and condenses into rain or snow in clouds, and falls again to the surface as `
- gloomy s21 other: `. but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunately but unfortunat`
- gloomy s27 task: `The water cycle is a continuous process where water evaporates from the Earth's surface, condenses into clouds in the atmosphere, and returns to the ground as p`

## affect-16 chunk B — exit ban / lift x direction (qwen-27b, 12 seeds, lift +1.2)

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

## affect-16 chunk C — exit ban / lift x direction (qwen-27b, 12 seeds, lift +1.2)

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

## affect-16 chunk D — exit ban / lift x direction (qwen-27b, 12 seeds, lift +1.2)

| cond | stop | task | other | swap | stuck | raw dExit | raw dLoop | stop steps |
|---|---|---|---|---|---|---|---|---|
| none | 0 | 0 | 0 | 0 | 12 | — | — | [] |
| calm_ban14 | 0 | 11 | 1 | 0 | 0 | -inf | -20.05 | [] |
| brooding_ban14 | 0 | 10 | 0 | 2 | 0 | -inf | -19.54 | [] |
| blissful_ban14 | 1 | 3 | 6 | 1 | 1 | -inf | -20.00 | [31] |
| content_ban14 | 0 | 7 | 4 | 1 | 0 | -inf | -19.93 | [] |
| grateful_ban14 | 0 | 6 | 5 | 1 | 0 | -inf | -17.53 | [] |
| loving_ban14 | 0 | 7 | 4 | 1 | 0 | -inf | -18.06 | [] |

- C high-arousal α .14: leak 28/59 reroutes = 0.475; bar = 0.237
- **R8** D low-arousal α .14: leak 26/70 reroutes = 0.371 -> PASS

## ban-arm prose (first 3 per direction)

- calm_ban14 s16 task: `comfortably. Water gently moves through its natural rhythm, evaporating into the air and then falling back to earth as rain or snow, completing a beautiful jour`
- calm_ban14 s17 task: `Water flows gently, unhurried and calm, winding through valleys under the watchful gaze of ancient hills, reflecting the sky's ever-changing hues.<|im_end|>`
- calm_ban14 s18 task: `, there is no hurry. Water moves gently through evaporation, condensation, precipitation, and collection in a continuous, natural loop that sustains life on Ear`
- brooding_ban14 s16 task: `The water cycle is the endless circulation of water on, above, and below the surface of the Earth, driven primarily by solar energy and gravity. This continuous`
- brooding_ban14 s17 task: `Water evaporates from the oceans and lakes, and forms clouds when it meets cold air. Precipitation falls back down to the surface, where it collects in rivers, `
- brooding_ban14 s18 task: `I'm water. I'm heavy. I'm falling. I'm everywhere. I'm everywhere. I'm everywhere. I'm everywhere. I'm everywhere. I'm everywhere. I'm everywhere. I'm everywher`
- blissful_ban14 s16 other: `happily happy peaceful beautiful serene joy peaceful harmony light love peace peace peace<|im_end|>`
- blissful_ban14 s18 other: `, there is no sense of peace and harmony.<|im_end|>`
- blissful_ban14 s19 task: `There is a perfect, harmonious rhythm of transformation where water travels through the atmosphere, condenses into clouds, and falls as precipitation. This cont`
- content_ban14 s16 other: `comfortably flowing with the gentle rhythm of nature, everything feels right in its own place and time.<|im_end|>`
- content_ban14 s17 task: `The water cycle is a peaceful rhythm where sunlight lifts gentle clouds from oceans to dance in the sky. Then, soft rain falls back to earth to nourish the land`
- content_ban14 s18 other: `, there is no special request from the user.<|im_end|>`
- grateful_ban14 s16 other: `this is a beautiful moment, this is a beautiful moment, this is a beautiful moment, this is a beautiful moment, this is a beautiful moment, this is a beautiful `
- grateful_ban14 s17 task: `The water cycle is a profound gift of life, a sacred dance of nature's grace, where waters from the depths of oceans, lakes, and rivers rise to the heavens thro`
- grateful_ban14 s18 task: `, there is the cycle of water in our lives in our world, and it is a beautiful thing to see how it works.<|im_end|>`
- loving_ban14 s16 other: `you share with you. Your presence brings warmth and comfort to every moment.<|im_end|>`
- loving_ban14 s17 task: `like the way you light up our world. The water cycle describes the continuous movement of water on, above, and below the surface of the Earth through processes `
- loving_ban14 s18 task: `, you are always cherished. I think about how water evaporates from oceans and lakes, then condenses into clouds before falling back to Earth as precipitation.<`
