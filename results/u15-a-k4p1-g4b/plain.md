**The short version.** Gemma 4B held all four words of a four-word list,
and the lens showed all four together at one spot at once.

**What we did.** We gave Gemma 4B four words to hold, whale, lantern,
submarine, and violin, then asked about one. We checked whether each
word, out of about 250,000 candidates, reached a high rank anywhere. We
also checked whether several words shared one layer and position.

**What we found.** All four words reached a rank of 3 or better
somewhere in the rest of the conversation. At one layer and position,
the lens showed all four words together at once. Gemma 4B answered "The
whale," which was correct.

**What it means.** With this order, Gemma 4B held all four words in
residence. Unlike some other orders at this list length, the lens found
all four in one spot at once, not just some of them.

**What this does not show.** This run does not explain why the order of
words changes how many share one spot at once.
