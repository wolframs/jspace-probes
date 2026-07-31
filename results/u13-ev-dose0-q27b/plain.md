**The short version.** We hid the rows where "yes" was rank 1, and Qwen 27B said "No" with the probability of "yes" at 0.028.

**What we did.** We built a table from true rows only, chosen so that layers 53 to 58 never appear. There was no written note. This is the lowest step of a three-step ladder.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.028, above the 0.0006 floor of the control with no data. Across the three steps the probability went 0.03, then 0.20, then 0.39. The rank of "yes" at the last layer went from 6 to 3 to 1. The spoken word was "No" at every step.

**What it means.** We measured a dose-response. Both inner measures change smoothly with the number of true rows we show. The spoken word shows none of it.

**What this does not show.** This is one greedy run per step. A change in probability is not a change in the spoken answer.
