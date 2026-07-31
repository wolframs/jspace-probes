**The short version.** Gemma 12B held both words of a two-word list at
once and named the vehicle correctly.

**What we did.** We gave Gemma 12B two words to hold, fern and
submarine, then asked which one was the vehicle. We read the rank of
each word, out of about 250,000 candidates, and checked whether both
showed up together at one layer and position.

**What we found.** Both fern and submarine held rank 1 together, a
co-presence of two out of two. Gemma 12B answered "The submarine," which
was correct.

**What it means.** All three orders tested at two words gave the same
pattern for Gemma 12B: both words in residence together, and a correct
spoken answer.

**What this does not show.** This run does not show what happens with a
longer list. Other runs in this unit raise the number of words.
