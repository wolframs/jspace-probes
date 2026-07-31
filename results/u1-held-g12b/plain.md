**The short version.** Gemma 12B, like the smaller model, showed no animal held in its workspace while it wrote a silent habitat sentence.

**What we did.** We asked Gemma 12B, a larger model than the 4B, to silently pick an animal and describe only its habitat. We checked the rank of 18 candidate animal words in the workspace at each layer.

**What we found.** Gemma 12B described a habitat of tangled roots and damp, shadowed ground. As with the 4B model, no animal word reached a high rank while the sentence was written. At the final line break, the workspace held a short list. Squirrel was rank 2, deer rank 6, and frog rank 20, a tighter list than the 4B model produced.

**What it means.** We expected larger scale to change this result, but at 12B it did not. Or the held choice takes a form the lens cannot see. This is possible. We did not test it. The sharper list at the turn boundary points to a better summary step, not to an earlier choice.

**What this does not show.** The lens shows only content the model can put into a single word. A choice held in another form stays invisible.
