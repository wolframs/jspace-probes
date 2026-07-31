**The short version.** In this control run, Gemma 4B described the water cycle correctly, with no change made to its internal state.

**What we did.** We asked Gemma 4B to describe the water cycle in two sentences, with no steering. In the same test set, we amplified a direction built from six casual words: "anyways", "alot", "yummy", "kinda", "whilst", and "luckily". We tested it at the early, middle, and later layers, each at several strengths.

**What we found.** Gemma 4B wrote a normal, textbook description of the water cycle. Across the full test set, we measured that Gemma 4B's output broke somewhere between strength 0.0106 and 0.015, in both the early and the middle layers. In the later layers, it broke between strength 0.0212 and 0.03.

**What it means.** Gemma 4B has a narrow safe range for this kind of amplification, about a factor of two in strength. At strength 0.0106 in the middle layers, the wording had already turned plainer and more spoken, though the sentence stayed correct.

**What this does not show.** This run shows only the unsteered baseline. Each strength in this test set has its own separate record.
