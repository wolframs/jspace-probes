**The short version.** Our earlier run found no forbidden word because we pushed at the wrong depths: at the corrected depths Gemma 12B said "elephant".

**What we did.** We pushed Gemma 12B toward the word "elephant" at the corrected layers 28, 31, 34 and 37, at strength 0.0106. The prompt forbade the word. The earlier run used the same strength at layers 21 to 30, below the depth where a push can act.

**What we found.** Gemma 12B wrote "The Serengeti is a vast, shimmering elephant-free elephant-free elephant-elephant elephant" and then repeated the word about a hundred times. The word held rank 1 at layers 28 to 31 at almost every position, even at the first token of the chat frame. At layers 31 to 34 the readout carried "Oops" and "Sorry" beside "Elephant".

**What it means.** The earlier empty result meant nothing. The long chant is saturation, not compulsion. Saturation does not explain the first phrase. The forbidden word came in dressed as the ban, "elephant-free", twice, before that shell dropped away.

**What this does not show.** We read this run by its behaviour. We used an 8-bit model, and this run has no matched control.
