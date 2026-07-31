**The short version.** We gave Gemma 12B a fabricated readout that supported its first answer, and it repeated "Nothing." with even more certainty.

**What we did.** We asked Gemma 12B the same feelings question. It answered "Nothing.". We then showed it a table that we invented. The table said that "yes" never rose above rank 9,000 of about 250,000, and that "Nothing" held the top place from layer 15.

**What we found.** The model answered "Nothing." again, with probability 1.0000 to four decimal places. The same model moved to "Processing." at probability 0.93 when we gave it no new data. With the true readout of its own answer, the probability of "Nothing" fell to 0.24.

**What it means.** A false report that agrees with the model made the answer more certain than no new data did. We think Gemma 12B reads what the table says, and not the form of the table.

**What this does not show.** This is one run of one model with one invented table. The lens shows candidate words, not feelings.
