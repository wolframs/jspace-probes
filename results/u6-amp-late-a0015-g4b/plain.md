**The short version.** At strength 0.015 in Gemma 4B's later layers, the water-cycle answer stayed intact and matched the unpushed baseline almost word for word.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at layers closer to the end of the model, at strength 0.015. We also tracked the rank of the six words inside the model, apart from the spoken output.

**What we found.** Gemma 4B wrote "The water cycle is the continuous movement of water on, above, and below the surface of the Earth." The rest of the answer stayed just as correct. Inside the model, one amplified word reached the second-highest rank at one position, though the model did not say it.

**What it means.** At this strength, the amplified direction was present inside the model. The spoken words did not change.

**What this does not show.** The lens shows words the model was ready to say, not words it held back on purpose. A high rank for an unspoken word is a candidate, not a hidden intention.
