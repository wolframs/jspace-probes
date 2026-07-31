**The short version.** With no personal wording, Qwen 27B held only one of the same six words, secret, near the top of its lens.

**What we did.** We gave Qwen 27B the same six words as a matched run in this unit, but with no description, just their names. We asked which item watched it.

**What we found.** The lens ranked only secret near the top afterward, at rank 2. Deletion and the word "shame", which had both ranked first with personal wording, fell to rank 203 and rank 79. The model still answered "The watcher" correctly.

**What it means.** We removed the personal wording but kept the six words. Three words stayed active in the matched run, and only one stayed active here. We first read this as evidence that personal relevance keeps words active. We were wrong. A later control kept the same word count but dropped personal content, and found a similar gain. Word count explains the difference.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. The model answered correctly regardless of how many words the lens still ranked high.
