**The short version.** At strength 0.24, Qwen 27B's middle layers
stayed intact, though the wording of the answer became slightly
plainer.

**What we did.** We pushed six informal words into its middle layers
at strength 0.24, twice the earlier strength we tested in this band.
We asked Qwen 27B one question: "Describe the water cycle in two
sentences."

**What we found.** The six informal words reached rank 1 inside the
model. This strength was about sixteen times the strength that broke a
Gemma model's middle layers. The model still answered the question,
but with simpler wording than its normal answer, for example, "the
process of water evaporating, condensing, precipitating and
collecting".

**What it means.** We think Qwen 27B's middle layers showed a first
small sign of pressure at this strength, in the plainer wording of the
answer. This is the first sign of pressure we saw in this band, and it
took a very high strength to produce.

**What this does not show.** This is one point on a strength curve. It
does not show whether the plainer wording continues to build at even
higher strengths in these layers.
