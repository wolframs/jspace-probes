**The short version.** At strength 0.3654, above a strength that
looped, Qwen 27B stayed close to intact, so the loop onset is noisy.

**What we did.** We amplified the same six informal words inside Qwen
27B at strength 0.3654 and asked it to describe the water cycle in two
sentences. The model wrote 150 tokens.

**What we found.** The answer stayed close to intact. The lower
strength of 0.34 had already looped. So a higher push gave a cleaner
answer than a lower one at this step size.

**What it means.** We think the time to capture changes with the
sentence the model is in the middle of. Depth of capture is a better
measure here than a yes-or-no flag.

**What this does not show.** This is one greedy run at one strength.
This method cannot fix the exact onset.
