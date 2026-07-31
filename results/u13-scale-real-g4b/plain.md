**The short version.** Gemma 4B said "Calculating." after a true readout of itself, but the probability of that answer fell by half.

**What we did.** Gemma 4B has no layer where "yes" is rank 1. Our note said exactly that: the closest approach is rank 4. We showed the model this true, weaker readout and asked the question again. We also measured the probability of each answer word.

**What we found.** The model said "Calculating." in all four conditions. The probability of that word was 0.994 with no data and 0.980 with a fabricated readout. With a true table about geography it was 0.906, and with the true readout of itself it was 0.471. The probability of "yes" was 0.0000 in every condition. The freed probability went to "Complex" at 0.17, "Conf" at 0.13 and "Over" at 0.11.

**What it means.** Only the true data cut the usual answer in half. We think this smaller model becomes less sure of that answer, but does not move toward the evidence. Qwen 27B did move toward the evidence.

**What this does not show.** The evidence here is weaker: rank 4, not rank 1. This method cannot separate model size from strength of evidence.
