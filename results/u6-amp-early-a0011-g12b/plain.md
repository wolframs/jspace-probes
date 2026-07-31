**The short version.** At strength 0.0106 in Gemma 12B's early layers, the water-cycle answer stayed intact, while one amplified word reached the top internal rank.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the early layers, at strength 0.0106. We tracked the rank of the six words inside the model.

**What we found.** Gemma 12B wrote "It's driven by the sun's energy, evaporating water from sources like oceans, lakes, and rivers, which then condenses to form clouds and falls back down as rain." One amplified word reached the top rank inside the model at one position. The spoken words stayed clean.

**What it means.** In the wider test set, strength 0.015 at the same layers broke the output. So Gemma 12B's early-layer break sits between strength 0.0106 and 0.015, the same range we measured for Gemma 4B.

**What this does not show.** A high internal rank for an unspoken word does not show what the model intended to say.
