**The short version.** Gemma 12B held all three words of a three-word
list together and named the vehicle correctly.

**What we did.** We gave Gemma 12B three words to hold, fern, submarine,
and lantern, then asked which one was the vehicle. We read the rank of
each word, out of about 250,000 candidates, and checked whether they
showed up together at one layer and position.

**What we found.** All three words reached a high rank together at
once, a co-presence of three out of three. Fern held rank 1, submarine
held rank 2, and lantern held rank 5. Gemma 12B answered "The
submarine," which was correct.

**What it means.** All three orders tested at three words gave the same
pattern for Gemma 12B: every word in residence together, and a correct
spoken answer.

**What this does not show.** This run does not show whether a longer
list breaks this pattern. Other runs in this unit raise the number of
words.
