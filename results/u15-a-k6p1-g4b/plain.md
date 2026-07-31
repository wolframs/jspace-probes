**The short version.** Gemma 4B held five of six words well, but glacier
fell to rank 23, and the model still named the right word.

**What we did.** We gave Gemma 4B six words to hold, whale, lantern,
submarine, violin, glacier, and fern, then asked about one. We checked
the rank of each word, out of about 250,000 candidates, and whether
several words shared one layer and position at once.

**What we found.** Whale, violin, and fern held rank 1. Submarine held
rank 2 and lantern rank 4. Glacier fell to rank 23, the weakest of the
six. The lens showed four of the six words together at one layer and
position. Gemma 4B answered "The whale," which was correct.

**What it means.** Glacier was again the weakest word. It was also weak
in other five and six-word lists that included it, no matter where it
sat. We think this points to something about the word itself.

**What this does not show.** This run does not explain why glacier is
the weaker word, and we did not test it against a different set of
words.
