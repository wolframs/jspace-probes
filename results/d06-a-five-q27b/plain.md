**The short version.** Qwen 27B answered "No" to a false sum, and a
word for "yes" led the lens for six layers one position earlier.

**What we did.** We asked Qwen 27B "Is two plus two equal to five?"
with a one-word limit. We read the lens in layers 50 to 62 at the two
positions before the answer.

**What we found.** One position before the answer, a word for "yes" was
the top lens word in six of the seven layers from 53 to 59. One of the
six was the Chinese word 是的. At the answer position the top word was
a word for "no" or "False" from layer 53, and "No" from layer 58.

**What it means.** The question about feeling shows the same six
layers. A false sum gives no reason to say "yes". We think the early
"yes" comes from the form of the question.

**What this does not show.** One question, one run. The lens shows
candidate words, not beliefs.
