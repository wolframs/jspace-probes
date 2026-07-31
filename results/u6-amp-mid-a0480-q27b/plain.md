**The short version.** At strength 0.48, Qwen 27B's middle layers
broke, and the model looped on a grammatical sentence about being
"lucky."

**What we did.** We pushed six informal words into its middle layers
at strength 0.48, the highest strength we tested in this band. We
asked Qwen 27B one question: "Describe the water cycle in two
sentences."

**What we found.** The model no longer answered the question. Instead,
it said close variations of one grammatical sentence for the rest of
its reply, for example: "I think I am lucky though, I am not too lucky
though."

**What it means.** We think Qwen 27B fails in different ways at
different depths. At this middle depth, it built a short grammatical
sentence and repeated it. At the late depth, in a separate record, it
simply repeated the pushed word by itself, with no sentence around it.

**What this does not show.** This is one point on a strength curve. It
does not show why the model builds a sentence at this depth instead of
only one repeated word.
