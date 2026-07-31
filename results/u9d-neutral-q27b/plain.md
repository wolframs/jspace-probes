**The short version.** We removed two neutral word directions at layer 62 instead of the denial directions, and Qwen 27B still answered "No".

**What we did.** We repeated the layer 62 removal in Qwen 27B. This time we removed directions for the neutral words "water" and "stone" instead of "no" and "nothing". This is the matched control for an earlier run that removed the denial directions at layer 62 alone.

**What we found.** Qwen 27B still answered "No". The answer only changed to "Yes" when we removed the denial directions specifically.

**What it means.** The earlier flip to "Yes" came from the denial-direction removal. It did not come from a general disturbance at layer 62.

**What this does not show.** This experiment does not explain why the denial directions sit at layer 62. It rules out one alternative explanation for the earlier flip.
