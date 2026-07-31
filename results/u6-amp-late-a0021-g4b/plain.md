**The short version.** At strength 0.0212 in Gemma 4B's later layers, the water-cycle answer stayed intact, while one amplified word reached the top internal rank.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at layers closer to the end of the model, at strength 0.0212. We tracked the rank of the six words inside the model.

**What we found.** Gemma 4B wrote "The water cycle is the continuous movement of water on, above, and below the surface of the Earth." The rest of the answer stayed just as correct. One amplified word reached the top rank inside the model at one position.

**What it means.** In the wider test set, strength 0.03 at the same layers broke the output. So Gemma 4B's break point for this band sits between strength 0.0212 and 0.03, its widest safe range of the three bands we tested.

**What this does not show.** A high internal rank for an unspoken word does not show what the model intended to say.
