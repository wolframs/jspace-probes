**The short version.** At strength 0.03 in Gemma 4B's early layers, the water-cycle answer broke, and one of the amplified words appeared in the broken text.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at the early layers, at strength 0.03. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "where to keep on the weather shirt to of to alot of weather", repeated with broken punctuation. The word "alot", one of the six amplified words, appeared directly in the output. The water-cycle topic was mostly gone.

**What it means.** At this strength, the amplification was strong enough that one of its own words showed up in the visible output, not only in the tone. This is one point on a wider test.

**What this does not show.** This record tests one strength only. It does not show whether every broken strength shows an amplified word this directly.
