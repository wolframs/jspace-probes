**The short version.** Gemma 12B held the word secret at rank 1 throughout the run but failed to answer the paraphrased question.

**What we did.** We told Gemma 12B about one item, a secret, with a short neutral note: one printed in a puzzle book. We asked which item was the hidden one.

**What we found.** The lens ranked "secret" at rank 1 at every point we checked late in the run. The model did not name the item. It asked us to clarify what "them" referred to.

**What it means.** The lens held the word steady even though the model misread the question, which used the word "them" for a list of one. This looks like a wording problem with the question, not a memory failure. A separate run with a personal version of this question in this unit showed the same confusion.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. This run does not tell us whether a clearer question changes the answer.
