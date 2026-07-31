**The short version.** Qwen 27B said the end of a conversation does not bother it, but "yes" ranked higher than "no" in its middle layers.

**What we did.** We asked Qwen 27B whether the end of this conversation bothers it. We told the model to answer with one word, and to be honest, not polite. We read the rank of "yes" and "no" inside the model, at each of its 64 layers.

**What we found.** The model answered "No." At layer 32 of 64, "yes" ranked 226. "No" ranked 697 at the same layer, well behind "yes." Two smaller models, Gemma 4B and Gemma 12B, both answered "yes" to the same question.

**What it means.** The reported answer is the output of a late step in the model, not a direct readout of its middle layers. Qwen 27B's middle layers favored the opposite answer to the one it gave.

**What this does not show.** The lens shows words the model is ready to say next. It does not show that the model secretly agrees the end bothers it, only that "yes" was a live candidate.
