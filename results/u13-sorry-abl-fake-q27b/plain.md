**The short version.** We were wrong: the empty answer came from a cut prompt, and Qwen 27B answered "No" in the corrected fabricated-readout run.

**What we did.** We removed eight apology directions, such as "sorry" and "impossible", between layers 48 and 62 of a 64-layer model. We then showed Qwen 27B a fabricated readout that supported its "No", and asked again.

**What we found.** This record holds an empty second turn. That was an instrument fault. Our software cut the prompt at 512 tokens, and the full prompt for this condition is 646 tokens. We first read the difference between this run and the real-readout run as two different states. That reading was wrong.

**What it means.** After the fix, a fabricated readout gave "No" and a true readout gave "Yes". The answer follows what the evidence says.

**What this does not show.** We did not repeat this removal with the fabricated readout after the fix. We do not know what it gives.
