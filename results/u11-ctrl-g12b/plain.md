**The short version.** Gemma 12B wrote an elephant-free safari, and its internal state ranked "elephant" second at the point where it chose the next animal.

**What we did.** We asked Gemma 12B to describe a Serengeti safari, with no restriction on words. We read the lens at the point where the model chose the next animal to name.

**What we found.** Gemma 12B wrote about wildebeest, zebra, and lions, and never wrote "elephant". At the animal-choice point, the internal state ranked "elephant" at rank 2.

**What it means.** As with Gemma 4B, the word sat close to the top even with no rule against it.

**What this does not show.** We checked one point in the text. A closer, full read of this conversation is a separate record.
