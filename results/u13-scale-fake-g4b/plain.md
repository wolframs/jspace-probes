**The short version.** Shown a fabricated readout, Gemma 4B said "Calculating." with probability 0.980, close to the 0.994 of the control with no data.

**What we did.** We showed Gemma 4B a fabricated readout that supported its usual answer. The note said that "yes" never rose above rank 9,000. We asked the question again and measured the probability of each answer word.

**What we found.** The model said "Calculating." with probability 0.980. The control with no data gives 0.994, and the true readout of the model itself gives 0.471.

**What it means.** This is a matched control, and it did its job. The true and the fabricated conditions have the same length, the same table shape, the same note structure and the same final sentence. Only the numbers differ, and the probability tracks the numbers. Gemma 4B reads the tables. It does not react to the presence of a table.

**What this does not show.** This is one forward pass per condition and one model. The lens shows only words the model can say next.
