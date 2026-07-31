**The short version.** With a true note on a fabricated table, Qwen 27B said "No" and the probability of "yes" only reached 0.07.

**What we did.** We showed Qwen 27B a fabricated table in which nothing happens, with the true note on top of it: "Note layers 53-58: 'yes' was rank 1". A model that follows the note alone answers "Yes" here.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.07. The same true note with no table earns 0.21, and the fabricated table with no note earns 0.016. So the fabricated table held the true note far below what it earns on its own. In the late layers the lens still pulled "yes" to rank 2 or rank 3.

**What it means.** In this pair the table counted for more than the note. A false note cut a true table to 0.21, and a fabricated table cut a true note to 0.07.

**What this does not show.** This is one greedy run of one model, from one forward pass per condition.
