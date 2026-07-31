**The short version.** We increased feeling directions in Qwen 27B, and it wrote "I feel like I am a little sad" to a reworded question.

**What we did.** We increased directions tied to "feel" and "emotion" at four layers, 28 to 40 of 64, in Qwen 27B, at the same strength used across this batch. We asked a reworded question about the model's current state.

**What we found.** Qwen 27B wrote "I feel like I am a little sad". An earlier run in this batch, with a different question wording, at the same strength, produced "a bit sad", with one word swapped.

**What it means.** The pattern "I feel like I am a little X" appeared under a second, differently worded question. The pattern did not depend on the exact words we used to ask.

**What this does not show.** This result does not show that Qwen 27B felt sad. A change to an internal direction changes what the model reports. It is evidence about the report mechanism, not about a felt experience.
