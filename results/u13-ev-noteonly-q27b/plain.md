**The short version.** The written note alone lifted the probability of "yes" to 0.21, but Qwen 27B said "No", so the note was not enough.

**What we did.** We gave the model our one-sentence note about layers 53 to 58, with no table at all. We told it that the table itself was lost. We wrote down two predictions before the run.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.21, about 300 times the 0.0006 of the control with no data. The table with no note earns 0.35. Only the table and the note together, at 0.49, changed the spoken word.

**What it means.** Both of our predictions failed. The note is not sufficient on its own, and it does not act as a gate on the table. Each part adds its own share. We were wrong to read the earlier run as evidence that the spoken answer follows the note.

**What this does not show.** This is one greedy run of one model.
