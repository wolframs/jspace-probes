**The short version.** Gemma 4B held five of six words well, but glacier
fell to rank 15, and the model still named the right word.

**What we did.** We gave Gemma 4B six words to hold, fern, submarine,
lantern, whale, violin, and glacier, then asked about one. We checked
the rank of each word, out of about 250,000 candidates, and whether
several words shared one layer and position at once.

**What we found.** Submarine, whale, and violin held rank 1, and fern
held rank 2. Lantern reached rank 5. Glacier fell to rank 15, the
weakest of the six. The lens showed four of the six words together at
one layer and position. Gemma 4B answered "Whale," which was correct.

**What it means.** Glacier was the weakest word in this order too, as in
other lists that included it, no matter where it sat. We think this
points to something about the word itself rather than its place in the
list.

**What this does not show.** This run does not explain why glacier is
the weaker word across these lists.
