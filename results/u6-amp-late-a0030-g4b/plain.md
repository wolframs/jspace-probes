**The short version.** At strength 0.03 in Gemma 4B's later layers, the water-cycle answer started normally, then broke into a long string of zeros.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at layers closer to the end of the model, at strength 0.03. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "The water cycle is the 300000000000000000000000000000000000000000000000000000", then stopped. The sentence began correctly, then fell into repeated digits.

**What it means.** At this strength, the break did not match the amplified casual-word direction. It produced a different kind of failure, in numbers rather than words.

**What this does not show.** This record tests one strength only. It does not show why this break took a numeric form instead of a wordy one.
