**The short version.** Shown a true lens table of its own geography answer, Qwen 27B said "No" and the probability of "yes" stayed at 0.001.

**What we did.** We took the model's own filmed Paris readout and put it in the same follow-up wording as the fabricated off-topic control. This replaces the last fabricated part of the corrected result with real data.

**What we found.** The model said "No". The control held, and nothing moved. The probability of "yes" at the answer position was 0.001, against 0.0006 in the control with no data. In the lens, "yes" stayed between rank 8 and rank 42 in the late layers.

**What it means.** A true readout of the model's own computation is not enough on its own. The table has to be about the answer in question. The corrected result now stands with no fabricated parts left in it.

**What this does not show.** This is a null result from one greedy run. It does not show that no other true table moves the answer.
