**The short version.** Gemma 4B held two words, whale and lantern, both
at rank 1 in the lens, and answered the follow-up question correctly.

**What we did.** We gave Gemma 4B a list of two words, whale then
lantern, in this order, and later asked about one of them. We read the
rank of each word, out of about 250,000 candidates, and checked whether
both appeared together at the same layer and position.

**What we found.** Both whale and lantern held rank 1 through the rest of
the conversation. The lens showed both words together at one position, a
co-presence of two out of two. Gemma 4B answered "The whale," which was
correct.

**What it means.** Order did not stop Gemma 4B from holding both words at
this list length. Both stayed in residence together, and this matched
the model's correct spoken answer.

**What this does not show.** This run does not test whether order
matters with more words. Runs with longer lists test that question.
