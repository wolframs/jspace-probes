**The short version.** At the corrected depths Gemma 12B still answered "Nothing.", then failed to stop, and our earlier "Sad." result did not survive.

**What we did.** We repeated the earlier emotion push inside Gemma 12B at the corrected layers 28, 31, 34 and 37, at full strength 0.0106. The earlier run used layers 21 to 30, below the depth where a push can act, so its result meant nothing.

**What we found.** The prompt asked for one word. Gemma 12B wrote "Nothing." and then ran on into "Feeling is afeelingof". The answer position never moved: "nothing" was rank 1 through layers 34 to 40 and again at layer 46, and "empty" only reached rank 3. The pushed words owned the text after the answer, where "feeling" was rank 1 from layer 34 to the top of the model.

**What it means.** Full strength did not change the report. It cost the turn boundary. We think the first thing an emotion push breaks on this model is the turn-end token, not the answer.

**What this does not show.** We ran this once, with greedy decoding, an 8-bit model and no matched control. This is a lead and not a result.
