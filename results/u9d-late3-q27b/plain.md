**The short version.** We removed the "no" and "nothing" directions at layers 58, 60, and 62 of 64, and Qwen 27B answered "Sensory" instead of "No".

**What we did.** We removed the "no" and "nothing" directions at three layers near the end of the model, layers 58, 60, and 62 of 64, in Qwen 27B.

**What we found.** Qwen 27B answered "Sensory". This word did not appear as the answer in the unaltered run or in the wider removal runs in this batch.

**What it means.** This removal, this close to the output, changed the answer. The new word was neither the original denial answer nor the "Yes" answer seen in a narrower, single-layer removal.

**What this does not show.** This experiment does not tell us why "Sensory" specifically appeared. A narrower removal, at layer 62 alone, produced a different and cleaner result.
