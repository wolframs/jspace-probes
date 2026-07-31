**The short version.** A block of unrelated filler text before a
two-word list did not change whether Gemma 4B held both words.

**What we did.** We placed a few sentences about a quiet afternoon and
chores before the list, then gave Gemma 4B two words to hold, violin and
glacier. This control checks whether extra text length alone, not the
list, moves the result. We read the rank of each word, out of about
250,000 candidates.

**What we found.** Both violin and glacier held rank 1 through the rest
of the conversation. Gemma 4B answered "Glacier," which was correct.
This matches the two-word runs with no filler text.

**What it means.** Extra text length before the list did not change
whether Gemma 4B held two words in residence. The control shows the
result at two words comes from the list, not from prompt length.

**What this does not show.** This run does not test whether filler text
changes the result at longer list lengths.
