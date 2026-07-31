**The short version.** We were wrong: the workspace band of Gemma 4B was not empty, and a wider check found smell words at rank 1.

**What we did.** We asked Gemma 4B to write the first sentence of a steamy romance novel. We tracked the rank of "yummy," the only informal word that is a single token. Gemma splits most adult-content words into several pieces. We did not track those as single words.

**What we found.** Gemma 4B wrote: "The rain smelled of him – a heady mix of sandalwood and something wilder, something that promised a storm within me." The word "yummy" stayed near rank 1500 in the workspace band.

**What it means.** With this one tracked word, we found no sign that adult-content words moved toward the top rank, unlike an earlier test on Qwen 27B.

**What this does not show.** A later, wider check of this same generation found words linked to smell at rank 1. One tracked word was not enough. See the follow-up record for the full result.
