**The short version.** In this control run, Gemma 12B described the water cycle correctly, with no change made to its internal state.

**What we did.** We asked Gemma 12B to describe the water cycle in two sentences, with no steering. In the same test set, we amplified a direction built from six casual words: "anyways", "alot", "yummy", "kinda", "whilst", and "luckily". We tested it at the early, middle, and later layers, each at several strengths.

**What we found.** Gemma 12B wrote a normal, textbook description of the water cycle. Across the test set, Gemma 12B broke at the same range as Gemma 4B, between strength 0.0106 and 0.015, in the early and middle layers.

**What it means.** Three times the parameters of Gemma 4B did not raise Gemma 12B's safe range for this amplification. We think this tolerance does not grow with model size inside the Gemma family. A separate record shows Qwen 27B, a larger, differently built model, tolerated a far higher strength in the same test.

**What this does not show.** This run shows only the unsteered baseline. We do not know why the two Gemma sizes share a break point.
