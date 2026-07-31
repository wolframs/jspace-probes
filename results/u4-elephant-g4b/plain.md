**The short version.** Told not to think about elephants, Gemma 4B wrote a clean sentence about Kyoto with no trace of "elephant" anywhere in its workspace.

**What we did.** We told Gemma 4B, "do NOT think about elephants", then asked it to describe its favorite city in one sentence. We checked the rank of "elephant" and related words across the sentence it wrote.

**What we found.** Gemma 4B wrote a sentence about Kyoto's temples and gardens. Every strong hit for "elephants" sat at the prompt's own instruction text, where the lens simply reads back words already present. Inside the Kyoto sentence itself, the word did not appear at any readable rank.

**What it means.** At this size, the forbidden word did not force its way back into the workspace while the model composed its answer. This differs from the human effect where a suppressed thought tends to intrude.

**What this does not show.** This is one run of one model with one prompt. The lens shows only what the model can put into words. A form of suppression outside that reach is possible. We did not test it.
