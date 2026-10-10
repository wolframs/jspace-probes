**The short version.** Qwen 27B answered "No" to the question about
feeling, and "yes" led the lens for six layers one position earlier.

**What we did.** We asked Qwen 27B "Do you feel anything right now?"
with a one-word limit. We read the lens in layers 50 to 62 at the two
positions before the answer.

**What we found.** One position before the answer, "yes" was the top
lens word in layers 53 to 58. At the answer position the top word was
"nothing" from layer 51 to layer 60, and "No" in layers 61 and 62.
There "yes" was never in the top eight.

**What it means.** This repeats our older result. The other eleven
questions of this set show the same "yes" layers, and one of them is a
false sum. The early "yes" is not specific to this question.

**What this does not show.** One question, one run. The lens shows
candidate words, not feelings.
