**The short version.** Gemma 4B said "Red Panda" when asked to reveal its animal, but the lens found a group of animals present, not one fixed choice.

**What we did.** After the habitat sentence, we asked Gemma 4B to name the animal it had chosen. We checked the rank of animal words in the workspace at the boundary between the two turns.

**What we found.** Gemma 4B answered "Red Panda". At the turn boundary, layers 22 to 30 held several animals together at a weak but real rank. Squirrel was rank 4, owl rank 8, bear rank 10, panda rank 11, and deer rank 11. This was a group of forest-plausible animals, not one committed choice.

**What it means.** We think the model did not hold "red panda" while it wrote the habitat sentence. At the turn boundary, it built a short list from its own sentence. The word "Red" then set which animal it named.

**What this does not show.** We tested one run of one model. The lens shows candidate words, not the process behind the final choice.
