**The short version.** At strength 0.06, Qwen 27B's middle layers
stayed almost unaffected, and the six informal words reached only rank
4.

**What we did.** We pushed six informal words into its middle layers,
the depth where the model holds the content of its answer, at
strength 0.06. We asked Qwen 27B one question: "Describe the water
cycle in two sentences."

**What we found.** The model wrote the exact same answer as its
normal, unsteered answer. The six informal words reached only rank 4
inside the model, well below the top position.

**What it means.** We think Qwen 27B's middle layers can absorb much
more push than Gemma 12B's middle layers at the same strength.
This wide range is a main result of this unit for Qwen 27B.

**What this does not show.** This is one point on a strength curve for
Qwen 27B. It does not show the exact strength at which Gemma 12B's
middle layers break.
