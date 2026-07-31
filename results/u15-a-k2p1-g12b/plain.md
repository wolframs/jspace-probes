**The short version.** Gemma 12B held both words of a two-word list at
once and named the animal correctly.

**What we did.** We gave Gemma 12B two words to hold, whale and
lantern, then asked which one was the animal. We read the rank of each
word, out of about 250,000 candidates, and checked whether both showed
up together at one layer and position.

**What we found.** Both whale and lantern held rank 1 together, a
co-presence of two out of two. Gemma 12B answered "The whale," which was
correct.

**What it means.** Two words was an easy case for Gemma 12B at this
order too. Both stayed in residence at the same time, and the spoken
answer matched the lens.

**What this does not show.** This run does not show what happens with a
longer list. Other runs in this unit raise the number of words.
