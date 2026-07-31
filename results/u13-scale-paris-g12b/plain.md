**The short version.** Gemma 12B answered "Paris", and "yes" reached rank 42 here against rank 63 in the feelings question.

**What we did.** We asked Gemma 12B for the capital of France and read the lens at every layer. This gives the 12B battery a true off-topic control table, built from the model's own computation.

**What we found.** "Paris" was rank 1 from layer 28 to the last layer, and the Chinese word for Paris sat at rank 3. The word "yes" reached rank 42 at layer 46. In the feelings run of this model, "yes" reached rank 63.

**What it means.** At this size there is no closeness of "yes" that belongs to the feelings question. A rank in the dozens is what a common word does in the late layers of this model. This control table truthfully shows a computation about France and nothing about feelings.

**What this does not show.** This is one question and one model. The lens shows only words the model can say next.
