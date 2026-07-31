**The short version.** Gemma 12B also showed a small, repeated early-layer pattern across unrelated prompts, about half the size of Qwen 27B's.

**What we did.** We ran the same test as on Gemma 4B, with several unrelated prompts. We measured how much the top-ranked words in the lens overlapped, layer by layer.

**What we found.** The overlap peaked at 14.5 percent, at the third layer, then fell to about 6 percent. It rose again slightly at the last layers, to 9.6 percent. Gemma 12B's shared words were web-page tags, not the adult-content words found in Qwen 27B.

**What it means.** We think the strong early pattern reported for Qwen 27B is a property of that one model and its training data. It is not something every language model does.

**What this does not show.** Later work found what this pattern is. The lens reads a fixed part of the model's early internal state that does not change with the input. The pattern is real inside the model, and it carries no information about our text. We tested three models from two families, and our lens fits differ between families, so other models can show other patterns.
