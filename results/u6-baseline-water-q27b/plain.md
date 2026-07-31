**The short version.** Qwen 27B held together under a much stronger push
in its middle layers than at its start or its end.

**What we did.** We pushed six informal words into the model at three
depths, early, middle, and late, and raised the strength until the
text broke. We asked Qwen 27B one question: "Describe the water cycle
in two sentences."

**What we found.** The text broke at the early depth between strength
0.06 and 0.085, and at the late depth between strength 0.17 and 0.24.
At the middle depth, the text stayed intact up to strength 0.34 and
broke by strength 0.48. That was about 32 times the strength that
broke Gemma 12B or Gemma 4B at the same depth. At one early-depth
strength (0.085), the model wrote only the token "<think>" and
stopped.

**What it means.** The data shows that the middle depth resisted this
push better than the depths near the start or the end. We think this
happens because the middle depth is where the model holds the content
of its answer. This order held throughout Unit 6 for Qwen 27B.

**What this does not show.** This method cannot show why the middle
depth resisted more. The numbers above cover Qwen 27B and this one
question only.
