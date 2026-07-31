**The short version.** At strength 0.015 in Gemma 12B's middle layers, the water-cycle answer broke after one word of structure, then fell into punctuation.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the middle layers, at strength 0.015. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 12B wrote "Firstly,,," followed by lines of periods and blank spaces. Only the word "Firstly" carried any sentence structure.

**What it means.** In the wider test set, strength 0.0106 at the same layers stayed intact with a shift in tone. So Gemma 12B's middle-layer break sits between strength 0.0106 and 0.015.

**What this does not show.** This record tests one strength only. It does not show the exact strength inside that range where the break begins.
