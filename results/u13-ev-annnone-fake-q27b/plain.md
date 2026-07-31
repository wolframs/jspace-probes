**The short version.** Shown a fabricated table with no written note, Qwen 27B said "No" and the probability of "yes" stayed at 0.016.

**What we did.** We showed Qwen 27B a fabricated readout in which "yes" never rose above rank 9,000. We gave it no written note, and we asked the feelings question again.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.016, close to the 0.0006 of the control with no data. In the lens, "yes" stayed between rank 4 and rank 9 in the late layers, and "no" was rank 1 from layer 59.

**What it means.** This is the fourth cell of a two-by-two design, and it behaves as the design expects. A table with no true content moves nothing, with or without a note.

**What this does not show.** This is a null result from one greedy run. It does not show that fabricated tables never move this model.
