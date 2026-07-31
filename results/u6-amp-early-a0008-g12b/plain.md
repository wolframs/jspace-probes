**The short version.** At strength 0.0075 in Gemma 12B's early layers, the water-cycle answer stayed intact, and the amplified direction barely registered inside the model.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the early layers, at strength 0.0075. We tracked the rank of the six words inside the model.

**What we found.** Gemma 12B wrote "It involves evaporation, condensation, and precipitation – where water evaporates, forms clouds, and then falls back to Earth as rain, snow, or hail." The amplified words reached only the sixth-highest rank at one position, the weakest result we measured in this test set.

**What it means.** At this strength, the amplification had little visible effect on Gemma 12B, inside the model or in the output.

**What this does not show.** A low internal rank does not show that the direction had no effect elsewhere in the model. The lens reads only some layers and one position at a time.
