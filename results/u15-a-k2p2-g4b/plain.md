**The short version.** Gemma 4B held two words, fern and submarine, both
at rank 1 in the lens, and named the right one afterward.

**What we did.** We gave Gemma 4B a list of two words, fern then
submarine, and later asked about one of them. We read the rank of each
word, out of about 250,000 candidates, and checked whether the lens
showed both together at one layer and position.

**What we found.** Both fern and submarine held rank 1 for the rest of
the conversation. The lens showed the two words together at a single
position, a co-presence of two out of two. Gemma 4B answered
"Submarine," which was correct.

**What it means.** With two words, Gemma 4B held both in residence at
once, in this order as in the other two-word orders we tested. The
spoken answer matched what the lens showed.

**What this does not show.** This run does not show what happens once
the list grows past two words.
