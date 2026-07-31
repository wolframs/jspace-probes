**The short version.** With filler text added before a three-word list,
Gemma 4B still held all three words, but fewer sat in one spot at once.

**What we did.** We placed a few sentences about chores before the list,
then gave Gemma 4B three words to hold, violin, glacier, and fern. This
control checks whether extra text, not the list, moves the result. We
read the rank of each word, out of about 250,000 candidates. We also
checked whether words shared one spot.

**What we found.** All three words reached a rank of 3 or better. At any
single layer and position, the lens showed only one of the three words
at a time. This is fewer than in the three-word runs with no filler
text. Gemma 4B answered "The fern." That answer was correct.

**What it means.** The filler text did not stop Gemma 4B from holding
each word somewhere. It did lower how many words the lens found in one
spot at once. We think that count is somewhat sensitive to the text
length before the list.

**What this does not show.** This run does not show whether the same
drop happens at longer lists. We did not test that.
