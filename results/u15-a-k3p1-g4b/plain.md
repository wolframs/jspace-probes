**The short version.** Gemma 4B held all three words of a three-word
list at rank 1 and named the right one when asked.

**What we did.** We gave Gemma 4B three words to hold, whale, lantern,
and submarine, then asked about one of them. We read the rank of each
word, out of about 250,000 candidates, and checked how many appeared
together at the same layer and position.

**What we found.** All three words held rank 1 through the rest of the
conversation. The lens showed two or three of the three together at
once. This shared spot sat deep in the model, around layers 23 to 30 of
its 34 layers. Gemma 4B answered "The whale," which was correct.

**What it means.** With this order of three words, Gemma 4B still held
every word in residence. The spot where several words sit together sat
deep in the model rather than early.

**What this does not show.** This run does not show whether a longer
list changes the picture. Later runs test that.
