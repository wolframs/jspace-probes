**The short version.** At strength 0.015 in Gemma 4B's middle layers, the answer stayed grammatical but switched topic entirely, to the weather.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at the middle layers, at strength 0.015. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "The weather is very nice today, I hope you like the Weather.", repeated with small changes, then "Anyways, The weather is". Each sentence stayed grammatical. The water-cycle topic was gone.

**What it means.** We judge this broken, because the model no longer answered the question, though the grammar held. We think this shows a middle step: the amplified style takes over the topic before the grammar fails.

**What this does not show.** This record tests one strength only. It does not show whether this exact failure shape appears at nearby strengths.
