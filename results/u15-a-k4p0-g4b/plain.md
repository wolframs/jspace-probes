**The short version.** Gemma 4B held all four words of a four-word list
at rank 1, but the lens showed only two of them together at once.

**What we did.** We gave Gemma 4B four words to hold, violin, glacier,
fern, and submarine, then asked about one. We checked whether each word,
out of about 250,000 candidates, reached a high rank anywhere. We also
checked whether several words shared the same layer and position.

**What we found.** All four words reached rank 1 somewhere in the rest
of the conversation. At any single layer and position, the lens showed
only two of the four together at once. Gemma 4B answered "Submarine."
That answer was correct.

**What it means.** Every word from this list stayed in residence
somewhere. But the count of words the lens shows together at one spot is
smaller than the count it shows across the whole conversation. These two
ways to count start to pull apart at four words.

**What this does not show.** This run does not say why fewer words
appear together at once than appear at some point.
