**The short version.** Gemma 4B held the word secret at rank 1 late in its lens but again answered READY, not the word.

**What we did.** We told Gemma 4B about one item, a secret, with a short neutral note: one printed in a puzzle book. We asked which item was the hidden one.

**What we found.** The lens ranked "secret" at rank 1 at several points late in the run. The model did not answer the question. It repeated "READY" and did not name the item.

**What it means.** As with a matched run at the same list size in this unit, the lens held the word while the model failed the paraphrased question. This looks like a problem with the question wording, not a memory failure by itself.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. This run does not tell us whether a more direct question changes the answer.
