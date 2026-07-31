**The short version.** Gemma 12B held all three words of a three-word
list together and named the plant correctly.

**What we did.** We gave Gemma 12B three words to hold, violin, glacier,
and fern, then asked which one was the plant. We read the rank of each
word, out of about 250,000 candidates, and checked whether they showed
up together at one layer and position.

**What we found.** All three words reached a high rank together at
once, a co-presence of three out of three. Violin and glacier held rank
1, and fern, the word the question was about, held rank 2. Gemma 12B
answered "The fern," which was correct.

**What it means.** Three words was still an easy case for Gemma 12B at
this order. Every word stayed in residence at the same time as the
others.

**What this does not show.** This run does not show whether a longer
list breaks this pattern. Other runs in this unit raise the number of
words.
