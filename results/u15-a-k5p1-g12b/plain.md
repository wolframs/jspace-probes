**The short version.** Gemma 12B kept two of five words together, led
by the word the question later asked about.

**What we did.** We gave Gemma 12B five words to hold, whale, lantern,
submarine, violin, and glacier, then asked which one was the animal. We
read the rank of each word, out of about 250,000 candidates, and
checked whether several showed up together at one layer and position.

**What we found.** Only two words reached a high rank together, a
co-presence of two out of five. Whale, the first word in the list, held
rank 1, and glacier held rank 2. Lantern fell to rank 33, submarine to
rank 12, and violin to rank 36. Gemma 12B answered "The whale." That
answer was correct.

**What it means.** This is the first-item effect. Here the first word
and the answer word were the same, so residence and the spoken answer
lined up.

**What this does not show.** This run does not show whether the match
between the first word and the answer caused the correct reply.
