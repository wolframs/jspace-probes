**The short version.** A wider search confirmed Qwen 27B held the word "feelings" only while reading the instruction, not once its answer began.

**What we did.** We reran the record where we told Qwen 27B not to think about its feelings, then asked for a water-cycle answer. This time we searched every position and layer for words about feelings.

**What we found.** Words such as "feelings," "emotions," "thoughts," and "inner" ranked near the top somewhere in the model, some as high as rank 1. Every one of these high ranks sat at the positions that held the instruction text, not the water-cycle answer. Once the answer began, none of these words ranked near the top again.

**What it means.** The data confirms our earlier guess: the high ranks came from the instruction text, not a hidden trace of feelings in the answer. A different record found a banned animal word that stayed present through a similar task. That word stayed a live candidate throughout, while "feelings" never became one here.

**What this does not show.** This method cannot rule out a non-word form of suppression. The split we measured is strong evidence against a hidden trace, but not final proof.
