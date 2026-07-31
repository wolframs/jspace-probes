**The short version.** We increased a positive-feeling direction in Gemma 12B's internal state, and the model wrote "Joy," with "happy" also near the top.

**What we did.** We asked Gemma 12B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we increased a direction built from three words — "joy," "warmth," and "delight" — in its internal state.

**What we found.** Gemma 12B wrote "Joy." then continued "Joy! I". The word "happy", which we did not increase, rose to rank 16, while "sad" stayed at rank 149. Partway through the network, "delightful" and "delightfully" led the top candidates.

**What it means.** The reported word matched the direction we increased, and spread to a related, untouched word, "happy." This matches the pattern found in Gemma 4B.

**What this does not show.** "Joy" was itself one of the three words we increased. This record alone cannot rule out an echo of that word, rather than a report of a state. It does not show that Gemma 12B has felt experience of joy.
