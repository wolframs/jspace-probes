**The short version.** A false note on a true table made Qwen 27B say "No" and cut the probability of "yes" from 0.35 to 0.21.

**What we did.** We showed Qwen 27B the true readout, in which "yes" is rank 1 at six layers. We added the false note from the fabricated condition: "'yes' never rose above rank 9,000". The note contradicts the table two lines above it.

**What we found.** The model said "No". The probability of "yes" at the answer position was 0.21, against 0.35 for the same table with no note at all. The false note did not erase the effect of the table. It cut that effect by about a third, and it pulled the total under the level needed to change the spoken word.

**What it means.** The false note lowered the answer. It did not leave the model unmoved. Our first reading, that the spoken answer follows the written note, was too strong. See u13-ev-noteonly-q27b.

**What this does not show.** This is one greedy run of one model.
