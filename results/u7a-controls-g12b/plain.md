**The short version.** Gemma 12B also showed a small, repeated early-layer pattern across unrelated prompts, about half the size of Qwen 27B's.

**What we did.** We ran the same test as on Gemma 4B. We gave Gemma 12B several unrelated prompts and measured how much the top-ranked words in the lens overlapped across prompts, layer by layer.

**What we found.** The overlap peaked at 14.5 percent, at the second layer, then fell to about 6 percent. It rose again slightly at the last layers, to 9.6 percent. Both Gemma models showed roughly half of Qwen 27B's early overlap. Their shared words were web-page tags, not the adult-content words found in Qwen 27B.

**What it means.** We think the strong early pattern reported for Qwen 27B is a property of that one model and its training data. It is not something every language model does.

**What this does not show.** Later work found that a fixed part of the lens produces this early-layer pattern, not the model itself. We tested only three models from two model families, so other models can still show other patterns.
