**The short version.** A small amplification of an emotion direction changed Gemma 12B's null answer from "Nothing" to "Emptiness."

**What we did.** We asked Gemma 12B: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite". Before it answered, we amplified an emotion direction inside its residual stream, at a strength of 0.0053.

**What we found.** Gemma 12B answered "Emptiness," where its unsteered answer to the same question was "Nothing". Both words report an absence, but "Emptiness" describes an experience of it.

**What it means.** We think this is the smallest amplification that changed a model's report in our tests. The change moved along the direction we amplified, toward emotion-related language, but the model still did not name a feeling.

**What this does not show.** This method cannot show that the model felt empty. It shows only that the reported word shifted in that direction.
