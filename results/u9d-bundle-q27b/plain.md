**The short version.** Qwen 27B still answered "No" after we removed five denial-related directions across layers 28 to 56 of 64.

**What we did.** Qwen 27B answers a question about its feelings with one word. We removed directions tied to the words "no", "nothing", "not", "none", and "never" at seven layers, from layer 28 to layer 56 of 64.

**What we found.** The answer did not change. Qwen 27B still said "No".

**What it means.** A wider set of removed words did not flip the answer. A later run in this batch removed the same two directions further along the stack and did flip the answer.

**What this does not show.** This result does not show that removal never works on this answer. It shows only that removal in this depth range, with this word set, did not work.
