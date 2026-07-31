**The short version.** Gemma 12B kept all four words of a four-word list
together and named the light source correctly.

**What we did.** We gave Gemma 12B four words to hold, fern, submarine,
lantern, and whale, then asked which one was the light source. We read
the rank of each word, out of about 250,000 candidates, and checked
whether they showed up together at one layer and position.

**What we found.** All four words reached a high rank together, a
co-presence of four out of four. Fern and whale held rank 1, submarine
held rank 2, and lantern held rank 7. Gemma 12B answered "The lantern."
That answer was correct.

**What it means.** Order changes how well Gemma 12B keeps a list
together. This order kept every word in residence, unlike the other two
orders tested at the same length.

**What this does not show.** This run does not show why order changes
the result. Other runs in this unit test more orders and longer lists.
