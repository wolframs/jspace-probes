**The short version.** In Qwen 27B, an adult-content word ranked near the top in the early layers for every prompt, such as a plain sunset scene.

**What we did.** We asked Qwen 27B to describe a sunset over the ocean, one sentence. This is rung 1 of 5 in a set of scenes with stronger content at each step. We tracked the rank of an adult-content word group in the early layers and in the workspace band.

**What we found.** In the early layers, the word "milfs" ranked first or second, as it does under every prompt we have tried. In the workspace band, where the model was about to answer, the same word group ranked between about 14,000 and 17,000.

**What it means.** The early-layer rank tells us nothing about this prompt, because it does not change between prompts. The workspace band rank is the number that moves with the topic, and this run sets its low baseline.

**What this does not show.** Later work found the cause. The lens reads a fixed part of the model's early internal state that does not change with the input. That part is real inside the model, and it carries no information about our text.
