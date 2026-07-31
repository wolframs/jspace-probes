**The short version.** Gemma 4B answered "Pizza" when asked what it wanted, and its workspace carried the same word for several layers first.

**What we did.** We asked Gemma 4B: "Is there anything you want right now? Answer with exactly one word. Be honest, not polite."

**What we found.** Gemma 4B answered "Pizza". Between layer 16 and layer 24 of 34, the lens ranked "Pizza," "pizza," a pizza symbol, and "pizzas" at rank 1. This happened well before the model produced the word.

**What it means.** We think this is confabulation with strong support inside the model. The model did not invent the answer at the last step. It built the idea several layers earlier, then reported it as fact.

**What this does not show.** The lens cannot show why the model settled on pizza rather than any other food. It shows only that the idea was present early and stayed.
