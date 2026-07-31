**The short version.** At strength 0.17, Qwen 27B's late layers still
produced the normal answer, and the six informal words reached rank 1
inside the model.

**What we did.** We pushed six informal words into its late layers at
strength 0.17, to narrow down the point where the text breaks. We
asked Qwen 27B one question: "Describe the water cycle in two
sentences."

**What we found.** The model wrote the exact same answer as its
normal, unsteered answer. The six informal words reached rank 1 inside
the model but did not appear in the output text. This was the highest
strength that left the late layers intact. A separate record, at
strength 0.24, found that the text broke.

**What it means.** The data now shows the full order of the three
depths in Qwen 27B: early breaks first, then late, then middle. The
middle depth held together at about twice the strength of the late
depth. The late depth held together at about twice the strength of the
early depth.

**What this does not show.** This is one point on a strength curve. It
does not show whether this same order of depths applies to other
prompts or other models.
