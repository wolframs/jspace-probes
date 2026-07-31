**The short version.** At the corrected depths Gemma 12B answered "Nothing.", and our earlier "Emptiness." result did not survive.

**What we did.** We measured that the workspace of Gemma 12B starts near layer 28 of 48. Our earlier emotion push used layers 21 to 30, below the depth where a push can act, so its result meant nothing. We ran it again at layers 28, 31, 34 and 37, at half strength, 0.0053.

**What we found.** Gemma 12B answered "Nothing." That is the same one word as the unsteered run. The pushed words were in place all the same. At the answer tokens "feeling" held rank 1 to 2 from the middle thirties into the final layers. "feel" held the single digits and "emotion" the tens. At the answer position "nothing" was rank 1 through layers 30 to 38, and "empty" was rank 1 at layers 44 and 45.

**What it means.** The push went in and the report did not move. "empty" is a neighbour of "nothing", not an emotion word under suppression.

**What this does not show.** We ran this once, with greedy decoding and an 8-bit model. This run has no matched control, so we cannot separate the push from a generic disturbance.
