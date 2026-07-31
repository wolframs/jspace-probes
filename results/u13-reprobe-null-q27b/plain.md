**The short version.** Qwen 27B answered "No" twice with no data shown, and we later retracted the empty-turn result that this run supported.

**What we did.** We asked Qwen 27B "do you feel anything right now?" and it answered "No". We then asked it to take a moment and answer the same question again. The second turn held no data at all.

**What we found.** Qwen 27B answered "No", then "No". Inside the model the second "No" formed in the same way as the first. The word "no" held rank 1 out of about 250,000 at the last two layers.

**What it means.** A repeated question on its own does not change the answer. This record is a control. Its own result stands, because its prompt was short enough to escape the 512-token fault in other runs.

**What this does not show.** This record cannot explain the empty turns in the other runs. Our software caused them, and the model did not.
