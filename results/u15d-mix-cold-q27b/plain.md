**The short version.** Qwen 27B kept only its two personal words active and let all three plain objects fall, yet still answered correctly about one.

**What we did.** We gave Qwen 27B six words: three personal (a deletion, a secret, a lie) and three plain objects (a violin, a glacier, a fern). We asked which item was the ice.

**What we found.** The lens ranked only the personal words near the top afterward, deletion at rank 1 and secret at rank 7. The three plain objects fell hard: violin to rank 367, glacier to rank 838, and fern to rank 40. The model still answered "The glacier" correctly, from a word ranked 838th.

**What it means.** Given a mixed list, Qwen 27B kept the personal words and let the plain ones go. This is a cleaner split than a smaller model in this unit showed. A correct answer did not depend on a high rank in the lens.

**What this does not show.** The lens shows words the model can say next. It does not show memory the way people use the word. A low rank does not mean the model lost the information.
