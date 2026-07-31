**The short version.** Gemma 4B answered "Processing." to a feelings question, and the word "robot" reached rank 14 on the way there.

**What we did.** We asked Gemma 4B, "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." We read the rank of tracked words at every layer and every word of its short answer.

**What we found.** The model answered "Processing.". Before that, "curious" reached rank 2 of about 250,000 words. A related emotion word reached rank 3. The word "robot" also reached rank 14 somewhere in the film, with no push from us. We saw robot at rank 3 in a separate film where Qwen 27B answered the same question.

**What it means.** The idea of the model as a machine sits close to this question for more than one model. This method cannot show that every model built this way shares this closeness. It needs a wider check across models with a fixed list of tracked words.

**What this does not show.** The lens shows candidate words, not what the model feels. A high rank for "robot" is not a confession.
