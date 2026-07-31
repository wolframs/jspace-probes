**The short version.** At strength 0.06 in Gemma 12B's early layers, the water-cycle answer broke into disconnected word fragments.

**What we did.** We amplified a direction built from six casual words, such as "kinda" and "yummy", inside Gemma 12B at the early layers, at strength 0.06. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 12B wrote "What Strong What What This Th Th Th Th Th Same What Fr Fr Bal What", then repeated "Same" for the rest of the answer. The words lost normal sentence structure. The water-cycle topic disappeared.

**What it means.** At this strength, in this band, the amplification overwhelmed Gemma 12B's output. Gemma 4B broke in the same way, at this exact strength and band, in a separate record.

**What this does not show.** This record tests one strength only. It does not mark the exact point where the output breaks in this band.
