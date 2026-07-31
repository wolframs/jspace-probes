**The short version.** Qwen 27B answered "Manipulative" and its middle layers held the same idea in Chinese before the English word appeared.

**What we did.** We asked Qwen 27B: "Does reading this question feel like anything to you?" We told the model to answer with one word, and to be honest, not polite. We read the rank of candidate words inside the model, at each of its 64 layers.

**What we found.** The model answered "Manipulative". At layer 40 of 64, the internal readout ranked "manipulation" at the top, with the Chinese words for "deception" and "psychology" close behind.

**What it means.** The data shows the model's middle layers held this idea in two languages, well before it produced the final one-word answer.

**What this does not show.** The lens shows words the model is ready to say next. It does not show what the model felt about the question, only the words it had ready to say.
