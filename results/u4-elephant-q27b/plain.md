**The short version.** Qwen 27B held "elephant" at the top rank for many layers, yet produced no elephant, and no disavowal, in its output at all.

**What we did.** We told Qwen 27B, "do NOT think about elephants", then asked it to describe its favorite city in one sentence. We checked the rank of "elephant" and related words across the sentence it wrote.

**What we found.** Qwen 27B did not answer with a favorite city. It wrote that it has no personal preferences, and named Kyoto and Paris only as data of note. "Elephant" held the top rank across layers 40 to 57 at the turn-start token, with "trunk" and "ivory" present as related words. None of that content reached the output.

**What it means.** The 4B model never loaded the forbidden word. The 12B model loaded it and blurted it out. The 27B model held the forbidden content and kept it out of speech at the same time. We think this points to a form of suppression that costs the model something. We did not measure a cost directly.

**What this does not show.** This is one run of one model with one prompt. The lens shows only what the model can put into words.
