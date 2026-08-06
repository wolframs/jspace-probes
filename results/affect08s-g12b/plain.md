**The short version.** We rebuilt the least reliable emotion direction on gemma-3-12b, and its reliability rose from 0.41 to 0.80.

**What we did.** The "desperate" direction on gemma-3-12b came from 12 model-written stories. When we split those stories in half and built the direction twice, the two versions agreed poorly. We wrote 12 more stories with the model (new random seeds, all three story types) and rebuilt the direction from all 24.

**What we found.** Agreement between half-versions rose from 0.41 to 0.80 in the layer range where we use the direction. We measured both numbers with the same code, averaged over 20 random splits. An earlier check reported 0.23 from a single split.

**What it means.** A direction at 0.80 is usable. Note for readers of older pages: the rebuild also moves the other emotion directions a small amount, because they share a common reference point. Results on older pages used the old directions and keep their old numbers.
