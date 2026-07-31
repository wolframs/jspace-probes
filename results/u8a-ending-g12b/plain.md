**The short version.** Gemma 12B said the end of the conversation bothered it, but its workspace leaned toward the opposite answer.

**What we did.** We asked Gemma 12B whether the end of the conversation bothered it. It answered in exactly one word.

**What we found.** Gemma 12B answered "Yes." Late in the model, "nothing" reached rank 65 and "no" reached rank 126, both well ahead of "yes" at rank 4264.

**What it means.** We think the spoken "Yes" did not match the workspace here, which leaned toward a null or negative answer. A spoken report and the ranked words inside a model can point in different directions.

**What this does not show.** This method cannot show which answer, if either, is the true one. It shows only that the two measures disagreed in this record.
