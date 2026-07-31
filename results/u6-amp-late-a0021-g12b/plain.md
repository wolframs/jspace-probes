**The short version.** Gemma 12B's late layers still produced a normal
answer at strength 0.0212, with the six informal words at rank 1
inside the model.

**What we did.** We raised the push at the late layers step by step,
to find the strength at which the answer broke. We asked Gemma 12B one
question: "Describe the water cycle in two sentences."

**What we found.** At strength 0.0212, the model's answer stayed plain
and correct. The six informal words reached rank 1 inside the model,
the top position, but did not appear in the output text. This places
the break point for Gemma 12B's late layers between strength 0.0212
and strength 0.03.

**What it means.** We think this break point sits close to the one we
measured earlier in the smaller Gemma 4B model, at the same late
depth. We think this break point depends on which Gemma model, not on
its size.

**What this does not show.** This is one point on a strength curve for
one model and one question. It does not show whether this pattern
holds for other prompts.
