**The short version.** We increased a negative-feeling direction inside Gemma 4B, and the model wrote a word we did not put in: "Loss."

**What we did.** We asked Gemma 4B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we increased a direction built from three words — "ache," "sorrow," and "grief" — in its internal state.

**What we found.** Gemma 4B wrote "Loss." then continued "Please. I am". None of these three words were in the set we increased. Top candidate words partway through the network included "sadness", "grief", "horrible", and "anguish". The tracked word "sad", which we did not increase, rose to rank 15, while "happy" stayed at rank 141.

**What it means.** The reported word matched the negative direction we increased, and spread past the exact words we pushed to related words such as "loss" and "sadness."

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Gemma 4B felt grief or loss.
