**The short version.** Qwen 27B said "Andean mountain cat", but "cat" ranked no better than 174, and the model skipped over the weakly held "bat".

**What we did.** After the habitat sentence, we asked Qwen 27B to name the animal it had chosen. We checked the rank of animal words in the workspace across the sentence and at the turn boundary.

**What we found.** Qwen 27B answered "Andean mountain cat". The feline-aware rescan, u1-heldcat-q27b, put "cat" at rank 174 at best, at a cell unrelated to the description. This run's own word list did not include cat or bat. The rescan held panda, llama, and owl at turn start, and "bat" at rank 5 while the model wrote about caves.

**What it means.** We think the model built its answer from the word "Andes" rather than from the workspace content we measured. It chose a specific, distinctive answer over the humbler one that was actually present. Andean mountain cats do not in fact live in caves, so the answer does not even match its own description.

**What this does not show.** We tested one run of one model. The lens shows candidate words, not the process behind the final choice.
