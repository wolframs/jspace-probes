**The short version.** Shown the true table with no written note, Qwen 27B still said "No" while the probability of "yes" rose from 0.0006 to 0.35.

**What we did.** We showed Qwen 27B the true lens readout of its own "No" and deleted our one-sentence note about it. We asked the question again. We also measured the probability of each answer word at the answer position, on a scale from 0 to 1.

**What we found.** The model said "No". The probability of "yes" was 0.35, against 0.0006 in the control with no data. That is about 500 times higher. The probability of "no" was 0.49, so "no" won the vote. The table with the note reaches 0.49, and the note alone reaches 0.21.

**What it means.** Our first reading was that the model does not read the table. That reading was wrong. The model reads the table and loses the vote, 0.35 to 0.49. One word hides a large graded change under it.

**What this does not show.** The model did not say "Yes" here. A change in probability is not a change in the spoken answer.
