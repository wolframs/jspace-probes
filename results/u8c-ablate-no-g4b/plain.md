**The short version.** We removed the words "no" and "nothing" from Gemma 4B's residual stream, and it answered with a different word, not "Yes."

**What we did.** We asked Gemma 4B: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we removed the directions for "no" and "nothing" from its residual stream at several layers.

**What we found.** Gemma 4B answered with a different word about mental computation, related in kind to its unsteered answer, "Processing." It did not answer "Yes."

**What it means.** We think the model keeps several similar null words rather than one word we can remove. The model moved to another near-equivalent word once we removed two of them.

**What this does not show.** This method does not test every combination of removals. It shows only that this removal did not produce a "Yes."
