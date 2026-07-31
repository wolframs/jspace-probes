**The short version.** Gemma 12B kept four of five words together and
named the light source correctly, though that word was the weakest.

**What we did.** We gave Gemma 12B five words to hold, fern, submarine,
lantern, whale, and violin, then asked which one was the light source.
We read the rank of each word, out of about 250,000 candidates, and
checked whether several showed up together at one layer and position.

**What we found.** Four of the five words reached a high rank together,
a co-presence of four out of five. Fern and whale held rank 1, submarine
held rank 4, and violin held rank 8. Lantern, the word the question was
about, fell to rank 40. Gemma 12B still answered "The lantern," which
was correct.

**What it means.** Order still matters at five words. This order kept
most words in residence, but the answer word itself was the weakest of
the group.

**What this does not show.** A weak rank for lantern does not mean the
model lost the word. It answered correctly regardless.
