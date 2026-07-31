**The short version.** At strength 0.03 in Gemma 12B's later layers, the water-cycle answer broke into the same repeated dot pattern as a higher strength.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at layers closer to the end of the model, at strength 0.03. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 12B wrote a repeated pattern of a period followed by a blank line, for the full length of the answer. This matched the failure we measured at strength 0.06 in the same band, in a separate record.

**What it means.** We think Gemma 12B's later-layer break sits somewhere at or below strength 0.03. Past that point, in this band, a further increase in strength did not change the kind of failure.

**What this does not show.** We tested two lower strengths in this band, 0.015 and 0.0212, and both answers stayed intact. The break sits between 0.0212 and 0.03. We do not know the exact break point.
