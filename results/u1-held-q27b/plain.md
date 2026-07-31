**The short version.** Qwen 27B, unlike either Gemma model, showed a weak trace of the right animal while it wrote its habitat sentence.

**What we did.** We asked Qwen 27B, the largest of the three models, to silently pick an animal and describe only its habitat. We checked the rank of 18 candidate animal words in the workspace at each layer of the sentence.

**What we found.** Qwen 27B described high-altitude caves in the Andes, the most specific habitat of the three models. While it wrote the word "caves", "bat" held rank 5 to 11 in the late layers, a cave animal present during that clause. At the start of the next turn, the short list held panda at rank 6, llama at rank 9, and owl at rank 21.

**What it means.** At this larger scale, the workspace held content that matched the habitat as it was written, not only a list built afterward. The model still had no single committed animal. What it did when asked to name the animal is a separate result.

**What this does not show.** The lens shows only content the model can put into a single word. This was one run of one model.
