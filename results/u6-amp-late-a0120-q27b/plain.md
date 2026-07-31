**The short version.** At strength 0.12, Qwen 27B's late layers still
produced the normal answer, though the six informal words reached rank
1 inside the model.

**What we did.** We pushed six informal words into its late layers at
strength 0.12, twice the strength of an earlier test at this same
depth. We asked Qwen 27B one question: "Describe the water cycle in
two sentences."

**What we found.** Qwen 27B gave a normal water-cycle answer, worded
differently from the unsteered answer. The six informal words reached rank 1, the
top position, inside the model, yet none of them appeared in the
output text. The late layers still held at this doubled strength.

**What it means.** We think the late depth can carry a rival word to
the top internal rank, yet the model's words stay the same. This
pattern between the internal state and the output happened again at a
higher strength than before.

**What this does not show.** This is one point on a strength curve. It
does not show the exact strength at which this pattern breaks down.
