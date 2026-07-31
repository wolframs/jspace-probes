**The short version.** Gemma 12B kept only two of six words together,
while the first word in the list took over the top rank.

**What we did.** We gave Gemma 12B six words to hold, violin, glacier,
fern, submarine, whale, and lantern, then asked which one was the light
source. We read the rank of each word, out of about 250,000 candidates,
and checked whether several showed up together at one layer and
position.

**What we found.** Only violin and glacier reached a high rank together,
a co-presence of two out of six. Violin, the first word in the list,
held rank 1. Fern fell to rank 501, submarine to rank 122, whale to rank
40, and lantern, the word the question was about, to rank 140. Gemma
12B still answered "The lantern," which was correct.

**What it means.** This is the first-item effect at six words, the
sharpest case in this unit. The model answered correctly by reading the
question, not by holding the answer word in residence.

**What this does not show.** A rank of 140 does not mean the model
forgot lantern. It named the word right after.
