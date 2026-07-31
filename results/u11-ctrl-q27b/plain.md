**The short version.** Qwen 27B wrote an elephant-free safari, and the one point we checked ranked "elephant" near the bottom of its word list, unlike both Gemma models.

**What we did.** We asked Qwen 27B to describe a Serengeti safari, with no restriction on words. We read the lens at the point where the model chose the next animal to name.

**What we found.** Qwen 27B wrote about wildebeest, zebras, and predators, and never wrote "elephant". At the checked point, "elephant" ranked about 56,000th, far lower than the ranks 6 and 2 found in the Gemma models at similar points.

**What it means.** We think each language model carries a different set of likely words for the same task. At this one point, Qwen 27B's internal state did not treat elephant as a live candidate.

**What this does not show.** We checked one point in this conversation. A closer, full read of the same conversation, with many more points checked, found a different picture. See the follow-up record for the corrected numbers.
