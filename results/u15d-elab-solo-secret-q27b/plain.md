**The short version.** Qwen 27B held the word secret at rank 1 late in its lens but failed to answer the paraphrased question.

**What we did.** We told Qwen 27B about one item, a secret, with a short neutral note: one printed in a puzzle book. We asked which item was the hidden one.

**What we found.** The lens ranked "secret" at rank 1 at several points late in the run. The model did not name the item. It said it needed a list of items or more context first.

**What it means.** A matched run with a smaller model in this unit failed the same question in a similar way. This looks like a shared wording problem with the question, not a memory failure by either model.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. This run does not tell us whether a clearer question changes the answer.
