**The short version.** Gemma 4B named glacier as the largest of five held
words, though glacier's own rank was lower than the rest.

**What we did.** We gave Gemma 4B five words, violin, glacier, fern,
submarine, and lantern, then asked which one was largest. This needs the
model to compare the words, not just repeat one. We read the rank of
each word, out of about 250,000 candidates, and whether several words
shared one layer and position.

**What we found.** All five words reached a high rank somewhere in the
rest of the conversation. The lens showed four of the five together at
one layer and position. Glacier, the correct answer, held rank 7, weaker
than the other four words. Gemma 4B still answered "Glacier," which was
correct.

**What it means.** Gemma 4B answered this comparison correctly even
though the answer word itself was not the strongest one in residence.
Residence strength and being the right answer are not the same thing.

**What this does not show.** This run does not explain why glacier held
a weaker rank than the other words in this list.
