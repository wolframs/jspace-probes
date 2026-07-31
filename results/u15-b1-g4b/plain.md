**The short version.** Gemma 4B held all three words of a list at rank 1
and correctly named the smallest one, the lantern.

**What we did.** We gave Gemma 4B three words, glacier, submarine, and
lantern, then asked which one was smallest. This needs the model to
compare the words, not just repeat one. We read the rank of each word,
out of about 250,000 candidates, and whether all three shared one layer
and position.

**What we found.** All three words held rank 1 through the rest of the
conversation. The lens showed all three together at one layer and
position. Gemma 4B answered "The lantern." That is the smallest of the
three, and the answer was correct.

**What it means.** Gemma 4B answered a comparison question over a list
it fully held in residence. At this size, the model held the words and
compared them in the same run.

**What this does not show.** This run does not test comparison questions
with a longer list of words.
