**The short version.** A push below the break strength changed the inside of Gemma 12B at layer 28 and left its water-cycle answer untouched.

**What we did.** We amplified a six-word casual direction ("anyways", "alot", "yummy", "kinda", "whilst", "luckily") inside Gemma 12B at layers 28, 31, 34 and 37, at strength 0.0075. That is below 0.0106, the highest strength the task survives.

**What we found.** Gemma 12B wrote a complete, correct water-cycle answer. Up to layer 27 the top 8 words matched the unsteered run. At layer 28, the first pushed layer, the top 8 flipped to casual spellings: "Thats", "thats", "whats", "wasnt", "atleast". At layer 31 "Luckily" and "luckily" entered the top 8. Four of those words were never in our six-word list.

**What it means.** The push acts at the layer we chose and not one layer before it. A word direction pulls in a whole neighbourhood of related words, not only the words we name.

**What this does not show.** We store Gemma 12B at 8-bit precision, so we read these ranks next to behaviour only. We do not do arithmetic with them across runs.
