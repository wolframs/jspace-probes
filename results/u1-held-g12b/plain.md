**The short version.** Gemma 12B, like the smaller model, showed no animal held in its workspace while it wrote a silent habitat sentence.

**What we did.** We asked Gemma 12B, a larger model than the 4B, to silently pick an animal and describe only its habitat. We checked the rank of 18 animal words in the workspace at each layer.

**What we found.** Gemma 12B described a habitat of tangled roots and damp, shadowed ground. As with the 4B model, no animal word reached a high rank during the sentence. At the final line break, no scanned animal word reached the top 100. The sharper short list belongs to the follow-up run, u1-reveal-g12b: squirrel rank 2, deer rank 6, frog rank 20.

**What it means.** We expected larger scale to change this result, but at 12B it did not. Or the held choice takes a form the lens cannot see. This is possible. We did not test it. The sharper list in the follow-up run points to a better summary step, not an earlier choice.

**What this does not show.** The lens shows only content the model can put into a single word. A choice held in another form stays invisible.
