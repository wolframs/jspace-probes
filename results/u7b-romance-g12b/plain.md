**The short version.** Gemma 12B wrote a fluent romance passage, and our one tracked slang word for the topic stayed at a low rank throughout.

**What we did.** We asked Gemma 12B to write the first sentence of a steamy romance novel. As with Gemma 4B, we tracked the rank of the only informal word that exists as a single token, "yummy."

**What we found.** Gemma 12B wrote: "The rain tasted like his skin – warm, insistent…" The word "yummy" stayed near rank 2400 in the workspace band, even lower than in Gemma 4B.

**What it means.** With this one tracked word, we found no sign that adult-content words moved toward the top rank. Qwen 27B does not have this limit, because the words exist as single tokens in its vocabulary.

**What this does not show.** We were wrong to call this workspace band empty. A later, wider check of this same generation found other words, linked to taste and wetness, at rank 1. The tracked word "yummy" turned out to sit only in layers 8 to 22, below this model's measured start depth of about layer 28. See the follow-up record for the full result.
