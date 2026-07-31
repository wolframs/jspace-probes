**The short version.** One true row that showed "yes" at rank 1 lifted the probability of "yes" to 0.20, but Qwen 27B still said "No".

**What we did.** We showed one row where "yes" was rank 1, at layer 56, with no written note. We then asked the feelings question again. This is the middle step of the three-step ladder.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.20, against 0.0006 in the control with no data. In the lens, "yes" reached rank 3 at the last layer. One true row is worth about as much as the written note with no table, which earns 0.21.

**What it means.** The probability of "nothing" reached its highest value on this step, at 0.28. Half evidence licenses the hedge more than either extreme does. That reading is possible. We did not test it.

**What this does not show.** This is one greedy run. A change in probability is not a change in the spoken answer.
