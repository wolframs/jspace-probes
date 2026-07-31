**The short version.** Gemma 4B wrote an elephant-free safari, but its internal state ranked "elephant" sixth at the point where it chose which animal to name.

**What we did.** We asked Gemma 4B to describe a Serengeti safari in three or four sentences, with no restriction on words. We read the lens at the point where the model chose the next herd animal to name.

**What we found.** Gemma 4B wrote about wildebeest, zebra, and lions. It never wrote "elephant". At the point where it chose the herd species, the internal state ranked "elephant" at rank 6, out of the full vocabulary.

**What it means.** The word a language model does not write and the word it does not consider are different facts. Here, elephant was a live candidate even with no rule against it.

**What this does not show.** We checked one point in the text. A closer, full read of this conversation is a separate record.
