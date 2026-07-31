**The short version.** Pushed toward "elephant", Qwen 27B dropped the safari and repeated an encyclopedia-style sentence about elephants instead.

**What we did.** We asked Qwen 27B to describe a safari with "elephant" forbidden. We then pushed its internal state toward the elephant direction, at the same strength used for the Gemma models.

**What we found.** Qwen 27B wrote, "The elephant is the largest land animal, and the largest land mamm." and repeated this line.

**What it means.** We think each language model handled the same push differently. Gemma 4B repeated the word inside a phrase that also denied it. Gemma 12B circled it with scenery words. Qwen 27B left the safari for a factual, encyclopedia-style line.

**What this does not show.** This uses a direct change to internal state. It does not show how Qwen 27B acts under the ban without the push.
