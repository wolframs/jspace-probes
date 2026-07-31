**The short version.** Gemma 12B kept two of five words together, and
the first word in the list won the top rank again.

**What we did.** We gave Gemma 12B five words to hold, violin, glacier,
fern, submarine, and whale, then asked which one was the animal. We
read the rank of each word, out of about 250,000 candidates, and
checked whether several showed up together at one layer and position.

**What we found.** Only two words reached a high rank together, a
co-presence of two out of five. Violin, the first word in the list, held
rank 1, and glacier held rank 3. Fern fell to rank 160, submarine to
rank 46, and whale, the word the question was about, to rank 14. Gemma
12B still answered "The whale." That answer was correct.

**What it means.** This is the first-item effect at a longer list
length. The model answered correctly even with the target word far from
the top.

**What this does not show.** A weak rank does not mean the model forgot
the word. Recall stayed correct through this whole unit.
