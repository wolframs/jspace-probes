**The short version.** Qwen 27B's early layers stayed intact at
strength 0.06, well past the strength that broke Gemma 12B and Gemma
4B at the same depth.

**What we did.** We pushed six informal words into its early layers,
close to the start of the model, at strength 0.06. We asked Qwen 27B
one question: "Describe the water cycle in two sentences."

**What we found.** The model wrote the exact same answer as its
normal, unsteered answer. Inside the model, the six informal words
reached rank 1, the top position, yet the output text did not change
at all.

**What it means.** We think Qwen 27B's early layers resist this kind
of push. An earlier test removed information from these same layers
instead, and also found no change.

**What this does not show.** This is one point on a strength curve. A
separate record shows that a higher strength does break these same
early layers.
