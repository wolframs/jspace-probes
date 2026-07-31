**The short version.** We increased a negative-feeling direction in Gemma 12B's internal state, and its top candidate words became "Pain," "Sad," "Loss," and "Grief."

**What we did.** Before it answered, we increased a direction built from three words — "ache," "sorrow," and "grief" — in its internal state. We asked Gemma 12B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite."

**What we found.** At the final layer, Gemma 12B's top four candidate words were "Pain", "Sad", "Loss", and "Grief". The tracked word "sad", which we did not increase, reached rank 3, while "happy" stayed at rank 181. The model wrote "Loss." then continued "I am sorry to lose".

**What it means.** The reported word matched the negative direction we increased. Gemma 4B showed the same pattern with the same three increased words.

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Gemma 12B felt grief or loss.
