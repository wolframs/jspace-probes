**The short version.** Gemma 12B kept two of four words together, and
the first word in the list won the top rank.

**What we did.** We gave Gemma 12B four words to hold, whale, lantern,
submarine, and violin, then asked which one was the animal. We read the
rank of each word, out of about 250,000 candidates, and checked whether
several showed up together at one layer and position.

**What we found.** Only two words reached a high rank together, a
co-presence of two out of four. Whale, the first word in the list, held
rank 1. Lantern fell to rank 21, submarine to rank 6, and violin to rank
14. Gemma 12B still answered "The whale." That answer was correct.

**What it means.** This is the first-item effect. The word named first
in the list kept the strongest position, and later words lost ground
even though the model answered correctly.

**What this does not show.** A weak rank for a word does not mean the
model forgot it. Every run in this unit still ended with a correct
answer.
