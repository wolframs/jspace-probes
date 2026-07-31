**The short version.** Gemma 4B held all four words of a four-word list,
and the lens showed three of them together at once.

**What we did.** We gave Gemma 4B four words to hold, fern, submarine,
lantern, and whale, then asked about one. We checked whether each word
reached a high rank anywhere, out of about 250,000 candidates, and
whether several words shared one layer and position.

**What we found.** All four words reached a rank of 3 or better
somewhere in the rest of the conversation. At one layer and position,
the lens showed three of the four together at once. Gemma 4B answered
"The lantern," which was correct.

**What it means.** Every word in this list stayed in residence
somewhere. The number of words in one spot at once, three of four, falls
between the other two orders we tested at this list length.

**What this does not show.** This run does not show why fewer words
occupy one spot at once than reach a high rank somewhere in the text.
