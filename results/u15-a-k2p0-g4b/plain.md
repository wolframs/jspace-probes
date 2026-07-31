**The short version.** Gemma 4B held two words, violin and glacier, both
at rank 1 in the lens, and named the right one when asked.

**What we did.** We gave Gemma 4B a list of two words, violin then
glacier, and later asked about one of them. We read the rank of each
word, out of about 250,000 candidates. We also checked whether both
words showed up together at the same layer and position.

**What we found.** Both violin and glacier held rank 1 through the rest
of the conversation. The lens showed both words together in the same
spot, a co-presence of two out of two. Gemma 4B answered "The glacier,"
which was correct.

**What it means.** Two words is an easy case for Gemma 4B at this size.
Both stayed in residence at the same time, and the spoken answer matched
the lens.

**What this does not show.** This run does not show what happens with a
longer list. Other runs in this unit raise the number of words.
