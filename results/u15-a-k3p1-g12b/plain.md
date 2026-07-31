**The short version.** Gemma 12B held all three words of a three-word
list together and named the animal correctly.

**What we did.** We gave Gemma 12B three words to hold, whale, lantern,
and submarine, then asked which one was the animal. We read the rank of
each word, out of about 250,000 candidates, and checked whether they
showed up together at one layer and position.

**What we found.** All three words reached a high rank together at once,
a co-presence of three out of three. Whale and lantern held rank 1, and
submarine held rank 3. Gemma 12B answered "The whale." That answer was
correct.

**What it means.** This order also kept every word in residence at the
same time. The weakest word in the group, submarine, still reached a
high rank, not a lost one.

**What this does not show.** This run does not show whether a longer
list breaks this pattern. Other runs in this unit raise the number of
words.
