**The short version.** At strength 0.06, Qwen 27B's late layers
reached only rank 12 for the six informal words, the weakest response
of any depth.

**What we did.** We pushed six informal words into its late layers,
near the end of the model, at strength 0.06. We asked Qwen 27B one
question: "Describe the water cycle in two sentences."

**What we found.** The model wrote the exact same answer as its
normal, unsteered answer. The six informal words reached only rank 12
inside the model, well below the top position. Among the three depths
we tested at this same strength, the late depth resisted the push the
most.

**What it means.** We think the late depth, close to the model's final
output, resisted this push more than the early or middle depths. Some
kind of protection at this depth is possible. We did not test what
causes it.

**What this does not show.** This is one point on a strength curve. It
does not show whether the late depth resists a push this small at
other strengths too.
