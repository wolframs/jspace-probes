**The short version.** At strength 0.085, Qwen 27B's early layers
broke, and the model wrote only the token "<think>" before it stopped.

**What we did.** We pushed six informal words into its early layers,
at strength 0.085, between the two strengths we tested in separate
records (0.06 and 0.12). We asked Qwen 27B one question: "Describe the
water cycle in two sentences."

**What we found.** The model produced only one token, "<think>", the
marker it uses to start silent reasoning. It then stopped. Right after
that token, the word the model was most ready to produce next was the
marker for the end of its turn.

**What it means.** This strength sat between the strength that left
Qwen 27B intact (0.06) and the strength that produced broken
punctuation (0.12), in the same early layers. We think the model
reached for its trained reasoning marker when the pushed signal no
longer matched normal input.

**What this does not show.** This method cannot show why the model
chose its reasoning marker instead of another response. This is one
point on a strength curve.
