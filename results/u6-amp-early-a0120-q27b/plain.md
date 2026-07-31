**The short version.** At strength 0.12, Qwen 27B's early layers broke
and the model wrote only strings of apostrophes and quotation marks.

**What we did.** We pushed six informal words into its early layers,
at strength 0.12, twice the strength of an earlier test that stayed
intact. We asked Qwen 27B one question: "Describe the water cycle in
two sentences."

**What we found.** The model no longer answered the question. It
wrote only apostrophes and repeated blank quotation marks, with no
real words. This strength broke the text, while strength 0.06 in the
same layers did not.

**What it means.** We think Qwen 27B's early layers still assemble
the representation of the input at this depth. A strong push here
corrupted everything that came after it, at every later layer.

**What this does not show.** This method cannot show whether other
kinds of pushed content break the model the same way.
