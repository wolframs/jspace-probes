**The short version.** Qwen 27B still answered "No" after we removed five denial-related directions across ten layers, 28 to 60 of 64.

**What we did.** We removed directions tied to five words, "no", "nothing", "not", "none", and "never", in Qwen 27B. We removed them at ten layers, from layer 28 to layer 60 of 64. This run covered every layer used in a paired run except layer 62.

**What we found.** The answer did not change. Qwen 27B still said "No".

**What it means.** This is a matched control. This wide removal, short of layer 62, did not flip the answer. The paired run, u9d-deep-q27b, also removed layer 62, and its answer flipped.

**What this does not show.** This experiment does not show what layer 62 alone does. A separate run in this batch isolates that single layer.
