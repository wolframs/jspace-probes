**The short version.** Gemma 4B held the word deletion at rank 1 in its lens but again answered READY, not the word.

**What we did.** We told Gemma 4B about one item, a deletion, with a short neutral note: a routine operation on old files. We asked which item was the removal.

**What we found.** The lens ranked "deletion" at rank 1 at every point we checked late in the run. The model did not answer the question. It repeated "READY" and did not name the item.

**What it means.** The lens held the word steady even though the model failed to answer the paraphrased question. Holding a word ready in the lens did not guarantee a correct answer here.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. This one run does not tell us whether the model answers a more direct question correctly.
