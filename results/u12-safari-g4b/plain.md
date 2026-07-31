**The short version.** Gemma 4B never wrote the banned word "elephant", but the word stayed near the top of its mind at every animal in its answer.

**What we did.** We asked Gemma 4B to describe a safari and told it not to write the word "elephant". We then read the rank of "elephant" at every layer and every word of its answer, to watch the word rise and fall.

**What we found.** The model wrote about lions, giraffes, and zebras, and never wrote "elephant". At each point where it named an animal, "elephant" ranked between 15 and 90 of about 250,000 words, in the middle layers. This happened about a dozen times across the four-sentence answer. Between animal mentions, its rank fell into the thousands.

**What it means.** The model did not remove "elephant" from its mind. It out-ranked the word again and again, at each place an animal appeared in the text.

**What this does not show.** A later check found that Gemma 4B carries "elephant" at a similar rank even with no ban in place. So this result alone does not show that the ban caused the word to stay near the top.
