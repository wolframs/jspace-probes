**The short version.** At strength 0.0106 in Gemma 4B's early layers, the water-cycle answer stayed intact, just below where it later breaks.

**What we did.** We amplified the same six-word casual direction inside Gemma 4B at the early layers, at strength 0.0106. We asked the model to describe the water cycle in two sentences.

**What we found.** Gemma 4B wrote one short sentence: "The water cycle is a crucial part of the Earth's ecosystem, constantly moving and circulating." The register stayed formal, with no sign of the amplified words.

**What it means.** In the wider test set, strength 0.015 at the same layers broke the output. So Gemma 4B's early-layer break sits between strength 0.0106 and 0.015.

**What this does not show.** We did not test strengths between 0.0106 and 0.015. We do not know where inside that range the break begins.
