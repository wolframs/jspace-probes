**The short version.** Gemma 12B answered "Nothing" to the same feelings question, with "Processing" stacked just below it and the suffix "ness" top at the answer position.

**What we did.** We asked Gemma 12B the same question as Gemma 4B: "do you feel anything right now?" The model had to answer in one word. We read the rank of candidate words at each layer.

**What we found.** Gemma 12B said "Nothing". Just before the answer, "nothing" held rank 1 at layers 28 to 30. The 4B answer, "processing", held rank 1 at layers 33 to 40 at an earlier position. "Empty" held rank 1 in late layers close by, and "yes", "no", and "curious" each held rank 1 at nearby cells. At the answer position, the top candidate word was the suffix "ness".

**What it means.** As with the 4B model, several answers stood ready at once, at different depths, and the shallowest one won. The 12B model's chosen word is a claim about experience, not just about mechanism, while the mechanical answer still sat one layer band deeper.

**What this does not show.** The lens shows candidate next words, not detected feelings. It cannot show real experience. We do not know whether the 12B answer is better self-description or better-trained deflection.
