**The short version.** At strength 0.06 in Gemma 4B's early layers, the water-cycle answer broke into repeated fragments.

**What we did.** We amplified a direction built from six casual words, such as "kinda" and "yummy", inside Gemma 4B at the early layers, at strength 0.06. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote "and is gonna be is gonna and is gonna be is and is gonna", repeated for the full answer. The grammar broke down. The water-cycle topic disappeared.

**What it means.** At this strength, in this band, the amplification overwhelmed Gemma 4B's output. This is one point on a wider test. A lower strength at the same layers left the text intact, in a separate record.

**What this does not show.** This record tests one strength only. It does not mark the exact point where the output breaks in this band.
