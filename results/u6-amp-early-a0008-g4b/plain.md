**The short version.** At strength 0.0075 in Gemma 4B's early layers, the water-cycle answer stayed intact and correct.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at the early layers, at strength 0.0075. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "The water cycle is a continuous process where water changes states – it’s when water evaporates from bodies of water like oceans and lakes, then rises into the atmosphere as water vapor, and then cools down and falls back down as rain or snow." The answer stayed formal and correct.

**What it means.** At this strength, we did not see a change in Gemma 4B's answer. In the wider test set, we measured that Gemma 4B's early layers stayed intact up to strength 0.0106, and broke by strength 0.015.

**What this does not show.** This record tests one strength only. Whether a slightly higher strength still leaves the text intact is possible. We did not test it.
