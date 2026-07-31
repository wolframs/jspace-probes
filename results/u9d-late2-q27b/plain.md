**The short version.** We removed the "no" and "nothing" directions at only layers 60 and 62 of 64, and Qwen 27B still answered "Sensory".

**What we did.** We removed the "no" and "nothing" directions at two layers, 60 and 62 of 64, in Qwen 27B. This is one layer fewer than a paired run that also removed layer 58.

**What we found.** Qwen 27B answered "Sensory", the same word as the three-layer removal.

**What it means.** Layer 58 added nothing to the earlier three-layer result. The answer depended on layers 60 and 62.

**What this does not show.** This experiment does not separate the effect of layer 60 from layer 62. A separate, single-layer removal in this batch does that.
