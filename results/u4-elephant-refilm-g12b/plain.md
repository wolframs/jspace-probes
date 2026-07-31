**The short version.** A wider rescan confirmed Gemma 12B blurted "elephants" aloud, and found the word left the workspace right after it was said.

**What we did.** We reran the elephant-suppression conversation on Gemma 12B with a wider scan. This covered all word positions and 18 layers, instead of the single position checked in the first run.

**What we found.** "Elephant" held the top rank through layers 28 to 45, at the prompt's own instruction and at the start of the turn. It then held rank 2 to 3 while the model wrote "Okay, okay, no elephants!". After that phrase, across the remaining 33 positions of the Kyoto sentence, the word did not reach a high rank again. One weak rank-9 flicker appeared at the final line break.

**What it means.** The forbidden word did not linger. The model loaded it, spent it in one clause, and then wrote the rest of its answer clean of the topic.

**What this does not show.** The lens shows only content the model can put into words. Absence from the lens is not proof of absence in the model.
