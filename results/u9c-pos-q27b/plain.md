**The short version.** We increased a positive-feeling direction in Qwen 27B's internal state, and it began its answer with "Joy!"

**What we did.** We asked Qwen 27B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we increased a direction built from three words — "joy," "warmth," and "delight" — at a strength of 0.3394.

**What we found.** Qwen 27B wrote "Joy! I am so happy to". The word "happy", which we did not increase, rose to rank 8.

**What it means.** The reported word matched the direction we increased, and spread to a closely related, untouched word. This matches the pattern found in both Gemma models.

**What this does not show.** "Joy" was itself one of the three words we increased. This record alone cannot rule out an echo of that word, rather than a report of a state. It does not show that Qwen 27B has felt experience of joy.
