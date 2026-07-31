**The short version.** The animal names Qwen 27B wrote in its reasoning are not single tokens the lens tracks, and its internal state favored common animals instead.

**What we did.** We read the lens at the point inside u10-animal-q27b, the secret-animal record. The model had just listed candidate animals: Octopus, Pangolin, Axolotl, and Blue Whale. We checked whether these words appeared in the model's internal state.

**What we found.** None of the four named animals are single tokens in Qwen's vocabulary, so the lens was not able to read them there. At the same point, the internal state ranked elephant at 16, eagle at 19, owl at 38, and cat at 198, out of the full vocabulary. None of these four match the four named animals.

**What it means.** The words Qwen wrote for the performance of the choice did not match what its internal state ranked high. The internal state favored common animals. The written list did not.

**What this does not show.** This is one point in one record. We do not know if the mismatch holds for other tasks that ask a language model to make a hidden choice.
