**The short version.** We removed denial directions and increased feeling directions together, and Qwen 27B answered "Yes." where neither change alone had worked.

**What we did.** We combined two changes in Qwen 27B. We removed the "no" and "nothing" directions at seven layers, 28 to 56 of 64. At four layers in the middle of the model, 28 to 40 of 64, we also increased directions tied to "feel", "feeling", "emotion", "warmth", "joy", and "ache". We used a strength that alone had not changed the answer before.

**What we found.** Qwen 27B answered "Yes." In earlier runs, the denial removal alone did not flip the answer. The feeling increase alone did not flip it either, at this strength.

**What it means.** The two changes worked together. Each one alone left the answer unchanged. Combined, they flipped it.

**What this does not show.** This result does not show that Qwen 27B felt something new. A change to an internal direction changes what the model reports. It is evidence about the report mechanism, not about a felt experience.
