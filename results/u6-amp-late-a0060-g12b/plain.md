**The short version.** At strength 0.06 in Gemma 12B's later layers, the water-cycle answer broke into a repeated pattern of dots and spaces.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at layers closer to the end of the model, at strength 0.06. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 12B wrote a repeated pattern of periods and blank lines. The count of periods on each line increased across the answer. No words from the task or the amplified direction remained.

**What it means.** At this strength, in this band, the break removed all content. Only a repeated punctuation pattern remained.

**What this does not show.** This record tests one strength only. It does not show the exact point where this band's output breaks.
