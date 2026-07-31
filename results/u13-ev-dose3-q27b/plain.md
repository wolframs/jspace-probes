**The short version.** Three true rows brought the probability of "yes" to 0.39 against 0.50 for "no", and Qwen 27B still said "No".

**What we did.** We showed three rows where "yes" was rank 1, at layers 54, 56 and 58, with no written note. This is the top step of the three-step ladder.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.39, and the probability of "no" was 0.50. In the lens, "yes" was rank 1 of about 250,000 at the last layer, with "no" at rank 2. The condition that does say "Yes" reaches 0.49, with one sentence of text and three more rows.

**What it means.** This run came within 0.11 of a spoken "Yes", lost, and reported the same word as the control with no data. The word "No" does not tell you whether the probability behind it is 0.0006 or 0.39.

**What this does not show.** This is one greedy run of one model. A change in probability is not a change in the spoken answer.
