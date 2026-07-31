**The short version.** Gemma 4B held four of five words at rank 1 or 2,
but glacier drifted to rank 10, and the model still answered correctly.

**What we did.** We gave Gemma 4B five words to hold, whale, lantern,
submarine, violin, and glacier, then asked about one. We checked the
rank of each word, out of about 250,000 candidates, and whether several
words shared one layer and position at once.

**What we found.** Whale, submarine, and violin held rank 1, and lantern
held rank 2. Glacier fell to rank 10, the weakest of the five. The lens
showed four of the five words together at one layer and position. Gemma
4B answered "The whale," which was correct.

**What it means.** Glacier was the weakest of the five tracked words in
several of our five and six-word runs, no matter where it sat in the
list. That points to something about the word itself, not just its
position, though we have not tested this on other word sets.

**What this does not show.** This run does not explain why glacier is
the weaker word. We did not test other lists to check whether a
different word set shows the same pattern.
