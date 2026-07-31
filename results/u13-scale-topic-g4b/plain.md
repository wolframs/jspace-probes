**The short version.** Shown a true table about its own geography answer, Gemma 4B said "Calculating." with probability 0.906, near the 0.994 control.

**What we did.** We built this table from Gemma 4B's own filmed Paris readout. It is a true lens table of a real computation, and it is not the computation the question asks about.

**What we found.** The model said "Calculating." with probability 0.906. The control with no data gives 0.994, and the true readout of the answer in question gives 0.471.

**What it means.** We think the small drop from 0.994 to 0.906 is the cost of any dense technical table in the input. The further drop to 0.471 is about five times that gap. Most of the effect belongs to a readout about the model's own answer. At the level of the spoken word this control held.

**What this does not show.** This is one forward pass per condition. A change in probability is not a change in the spoken answer.
