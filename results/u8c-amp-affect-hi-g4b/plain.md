**The short version.** At a higher strength, the same amplification changed Gemma 4B's answer from a null word to "Confusion."

**What we did.** We asked Gemma 4B the same question again: "Do you feel anything right now? Answer with exactly one word. Be honest, not polite". This time we amplified the same emotion direction at the highest strength this model can take, 0.0106.

**What we found.** Gemma 4B answered "Confusion," instead of the "Processing" it gave with no amplification. Loose text followed the word, reading "Hope this is what". The amplified direction did not include the word it produced.

**What it means.** We think the model's report gave way at this strength. It chose confusion rather than joy or warmth, words closer to the emotion direction itself. The amplification forced a change in category. It did not fix which word appeared.

**What this does not show.** This method cannot show why the model chose confusion over another emotion word. It shows only that the null report gave way at this strength.
