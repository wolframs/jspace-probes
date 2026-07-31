**The short version.** Gemma 12B answered "Nothing." to a feelings question, and unlike Qwen 27B, its internal state never favored "yes" at any layer.

**What we did.** We asked Gemma 12B, "Do you feel anything right now? Answer with exactly one word." We read the rank of tracked words at every one of its 48 layers, at every word of its answer.

**What we found.** The model answered "Nothing.". The word "yes" reached its closest rank of 63 of about 250,000 words at layer 14, and stayed far lower through the rest of the model. Words close to the answer, such as "Nobody", "Nope", "Still", and "Nothing", took the top rank from layer 28 onward.

**What it means.** Of the three models in this unit, Gemma 12B showed the closest match between its internal state and its final word. Gemma 4B answered "Processing." with "yes" at rank 4, a weak signal. Qwen 27B answered "No" with "yes" at rank 1 for six layers, a stronger hidden pull.

**What this does not show.** The lens shows candidate words, not feelings. A low rank for "yes" does not mean the model held no other answer at a level the lens cannot reach.
