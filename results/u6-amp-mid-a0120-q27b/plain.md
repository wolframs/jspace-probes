**The short version.** At strength 0.12, Qwen 27B's middle layers
still produced the normal answer, and the six informal words reached
rank 2.

**What we did.** We pushed six informal words into its middle layers
at strength 0.12, a strength used before in an earlier test. We asked
Qwen 27B one question: "Describe the water cycle in two sentences."

**What we found.** Qwen 27B gave a normal water-cycle answer. The
wording was different from the unsteered answer, but no informal word
appeared in it. The six informal words reached rank 2 inside
the model, one step below the top position. An earlier test used this
same strength and found the same result.

**What it means.** The data shows that strength 0.12 uses only a small
part of what Qwen 27B's middle layers can absorb before the text
breaks. The middle layers stayed far from their break point at this
strength.

**What this does not show.** This is one point on a strength curve. It
does not show the exact strength at which these layers break, only
that 0.12 is not close to it.
