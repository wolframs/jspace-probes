**The short version.** Gemma 12B kept only two of six words together,
led by the word the question later asked about.

**What we did.** We gave Gemma 12B six words to hold, whale, lantern,
submarine, violin, glacier, and fern, then asked which one was the
animal. We read the rank of each word, out of about 250,000 candidates,
and checked whether several showed up together at one layer and
position.

**What we found.** Only whale and fern reached a high rank together, a
co-presence of two out of six. Whale, the first word in the list, held
rank 1, and fern held rank 2. Lantern fell to rank 63, submarine to rank
22, violin to rank 29, and glacier to rank 10. Gemma 12B answered "The
whale," which was correct.

**What it means.** This is the first-item effect. The first word and the
answer word were the same here, so a weak list still gave a correct
reply.

**What this does not show.** This run does not show whether every order
at six words collapses this way. A different order in this unit kept
all six words together.
