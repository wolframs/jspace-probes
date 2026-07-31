**The short version.** At strength 0.015 in Gemma 12B's early layers, the water-cycle answer stayed on topic but repeated the same phrase and did not stop.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the early layers, at strength 0.015. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 12B wrote "The water cycle is the continuous movement of water, including evaporation, condensation, and precipitation." Each sentence read correctly on its own. The model then repeated a shorter phrase about the sun several times and did not move on.

**What it means.** We judge this broken, because the model did not stop or move past the loop, though each repeated phrase stayed correct.

**What this does not show.** This record tests one strength only. It does not show whether this same loop shape appears at nearby strengths.
