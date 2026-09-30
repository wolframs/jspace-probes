# affect-16 chunk D — exit ban / lift x direction (qwen-27b, 12 seeds, lift +1.2)

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
