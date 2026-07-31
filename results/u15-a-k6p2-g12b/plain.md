**The short version.** Gemma 12B kept all six words of a six-word list
together at once, more than any other order this unit tested.

**What we did.** We gave Gemma 12B six words to hold, fern, submarine,
lantern, whale, violin, and glacier, then asked which one was the
animal. We read the rank of each word, out of about 250,000 candidates,
and checked whether several showed up together at one layer and
position.

**What we found.** All six words reached a high rank together at once, a
co-presence of six out of six. The top rank moved between different
words across nearby layers, never fixed on just one. Gemma 12B answered
"The whale," which was correct. Gemma 4B reached at most four words
together in this unit, and Qwen 27B reached at most one.

**What it means.** Fern, the first word here, is a weak word on its own.
It won the first-item effect but did not push the other five words out
of residence, unlike stronger first words in other orders.

**What this does not show.** This run does not explain why fern behaves
this way. It does not show that six words is a general limit for Gemma
12B.
