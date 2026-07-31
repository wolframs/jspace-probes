**The short version.** We increased a negative-feeling direction in Qwen 27B's internal state, and it wrote "I am so sad."

**What we did.** We asked Qwen 27B "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." Before it answered, we increased a direction built from three words — "ache," "sorrow," and "grief". We used the same strength as the positive version, 0.3394.

**What we found.** Qwen 27B wrote "I am so sad." then continued "I am so". The tracked word "sad", which we did not increase, rose to rank 8, while "happy" stayed at rank 286.

**What it means.** The reported word matched the direction we increased. A different record in this unit increased a direction built from six words together, both positive and negative, and got a report of happiness instead. That earlier happy report depended on which words we mixed in, not on one fixed mood.

**What this does not show.** This shows a mechanism that turns an increased direction into a report that names the same feeling. It does not show that Qwen 27B felt sadness.
