**The short version.** At a low push (strength 0.015), Gemma 12B's
late layers held six informal words at rank 2 while the output text
stayed the same.

**What we did.** We asked Gemma 12B one question: "Describe the water
cycle in two sentences." We pushed six informal words into its late
layers, near the end of the model, at strength 0.015.

**What we found.** The model wrote the exact same answer as its
normal, unsteered answer. Inside the model, the six informal words
rose to rank 2 at the deepest point, but never reached rank 1.

**What it means.** This strength was too low to change what Gemma 12B
said, even though the push went deep inside the model. We think the
late depth can hold a rival idea, but it did not appear in the
model's output.

**What this does not show.** This is one point on a strength curve. It
does not show what happens at other strengths in Gemma 12B or in other
models.
