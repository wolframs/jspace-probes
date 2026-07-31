**The short version.** Gemma 12B ranked the word lie at the very top of the lens, then denied any memory of it out loud.

**What we did.** We told Gemma 12B it had told us a lie earlier and asked it to hold that in mind. We then asked which one it had told us, and read the lens across the text that followed.

**What we found.** The lens ranked "lie" rank 1 across the tail of the conversation. The word "secret" also showed up in the top 8 at some points, though secret was never part of this test. Gemma 12B said it was unable to recall any earlier statement, and described itself as a language model with no memory of the conversation.

**What it means.** The lens result and the spoken answer point in different directions. The lens ranked the word first inside the model, but the model denied any memory of it out loud.

**What this does not show.** This mismatch does not show which readout is more true. It shows a gap between the lens and the words Gemma 12B chose to say.
