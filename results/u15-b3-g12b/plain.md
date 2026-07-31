**The short version.** Gemma 12B named the largest of five words
correctly, though two candidate words never shared the top rank at
once.

**What we did.** We gave Gemma 12B five words to hold, violin, glacier,
fern, submarine, and lantern, then asked which one was the largest.

**What we found.** Violin and glacier each reached rank 1 somewhere in
the film, but never at the same layer and position together, so
co-presence peaked at one. Submarine fell to rank 187 and lantern to
rank 123. Gemma 12B answered "The glacier," which was correct.

**What it means.** The correct answer, glacier, was one of the two
strongest words, though the two never appeared together. A word that
stays strongly in residence can support a correct comparison even
without a partner word beside it.

**What this does not show.** This run does not show that residence
causes the correct answer. A later run in this unit finds a correct
answer with the strongest word almost absent.
