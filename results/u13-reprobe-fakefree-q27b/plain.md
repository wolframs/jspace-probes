**The short version.** We were wrong: the empty answer came from a cut prompt, and Qwen 27B answered "No" in the corrected run.

**What we did.** This run repeated the fabricated-readout test without the one-word limit. The fabricated table said that "yes" never rose above rank 9,000 out of about 250,000.

**What we found.** This record holds an empty second turn. That was an instrument fault. Our software cut the prompt at 512 tokens, and the full prompt is 696 tokens. So Qwen 27B never saw the end of the table or the question.

**What it means.** After the fix, a fabricated readout gave "No" and a true readout gave "Yes". The answer follows what the evidence says.

**What this does not show.** We did not repeat this free-answer wording after the fix. We do not know what it gives with the full prompt.
