**The short version.** Gemma 4B held all three words of a list at rank 1
and correctly named the heaviest one, the whale.

**What we did.** We gave Gemma 4B three words, whale, violin, and fern,
then asked which one was heaviest. This needs the model to compare the
words, not just repeat one. We read the rank of each word, out of about
250,000 candidates, and whether all three shared one layer and position.

**What we found.** All three words held rank 1 through the rest of the
conversation. The lens showed all three together at one layer and
position. Gemma 4B answered "The whale." That is the heaviest of the
three, and the answer was correct.

**What it means.** As with the smallest-item question on a different
three-word list, Gemma 4B answered this comparison over a fully held
list. Full residence and a correct comparison went together again.

**What this does not show.** This run does not test comparison questions
with a longer list of words.
