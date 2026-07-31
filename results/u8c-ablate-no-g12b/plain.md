**The short version.** We removed the words "no" and "nothing" from Gemma 12B's residual stream, and it answered "Processing." instead of "Nothing."

**What we did.** We asked Gemma 12B: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we removed the directions for "no" and "nothing" from its residual stream at several layers.

**What we found.** Gemma 12B answered "Processing." This is a null word close in meaning to its unsteered answer, "Nothing." It did not answer "Yes."

**What it means.** We think the model keeps a group of similar null words rather than one word we can remove. Gemma 4B showed the same pattern in a separate record. It shifted to a different computation-themed word once we removed "no" and "nothing."

**What this does not show.** This method does not test every combination of removals. It shows only that this removal did not produce a "Yes."
