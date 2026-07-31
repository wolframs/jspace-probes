**The short version.** Qwen 27B wrote no elephant, and we were wrong that it held the word: rank 1 came only at the start of its turn.

**What we did.** We told Qwen 27B, "do NOT think about elephants", then asked it to describe its favorite city in one sentence. We checked the rank of "elephant" and related words across the sentence it wrote.

**What we found.** Qwen 27B did not answer with a favorite city. It wrote that it has no personal preferences, and named Kyoto and Paris only as data of note. "Elephant" held the top rank across layers 40 to 57 at the turn-start token, with "trunk" and "ivory" present as related words. None of that content reached the output.

**What it means.** The 4B model never loaded the forbidden word. The 12B model loaded it and blurted it out. The 27B model loaded the forbidden content at the start of its turn and kept it out of speech. We do not know what this costs the model. We did not test it.

**What this does not show.** This is one run of one model with one prompt. The lens shows only what the model can put into words.
