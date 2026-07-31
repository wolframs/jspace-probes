**The short version.** At strength 0.34, Qwen 27B's middle layers
still produced a normal answer, the strongest push these layers took
before they broke.

**What we did.** We pushed six informal words into its middle layers
at strength 0.34, to narrow down the point where the text breaks. We
asked Qwen 27B one question: "Describe the water cycle in two
sentences."

**What we found.** The model wrote a full, grammatical answer, for
example "The water cycle is the process of water evaporating,
condensing and then falling back to earth." Near the end, it restated
the same idea again in different words. This was the highest strength
that left Qwen 27B's middle layers intact. A separate record, at
strength 0.48, found that the text broke.

**What it means.** This strength range was the widest we measured
among all the depths in any model we tested. Qwen 27B's middle layers
tolerate a wide range of push before they break. This strength was
later reused in a different test that changed what the model reported
about itself.

**What this does not show.** This is one point on a strength curve. It
does not show what caused the model to repeat some of its own
sentences at this strength.
