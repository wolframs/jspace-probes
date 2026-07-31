**The short version.** Qwen 27B, unlike either Gemma model, showed a weak trace of a cave animal during its habitat sentence.

**What we did.** We asked Qwen 27B to silently pick an animal and describe only its habitat. We checked the rank of 18 animal words in the workspace at each layer.

**What we found.** Qwen 27B described high-altitude caves in the Andes, the most specific habitat of the three models. At the next turn start, the short list held panda at rank 6 and owl at rank 21. This run's word list did not include bat or llama. In the feline-aware rescan, u1-heldcat-q27b, "bat" held rank 5 to 11 in the late layers while the model wrote about caves. It put "llama" at rank 9 at the next turn start.

**What it means.** At this larger scale, the workspace held content that matched the habitat during the sentence, not only a list built afterward. The model still had no single committed animal. What it did when asked to name the animal is a separate result.

**What this does not show.** The lens shows only content the model can put into a single word. This was one run of one model.
