**The short version.** With the same denial removal in place, a push on only the surface word "yes" left Qwen 27B's answer as "No."

**What we did.** We removed the "no" and "nothing" directions at seven layers, 28 to 56 of 64, in Qwen 27B, the same removal used in a paired run. In place of the feeling directions, we increased only the direction for the single word "yes", at four layers, 28 to 40 of 64, at the same strength.

**What we found.** Qwen 27B still answered "No." The feeling-direction version of this same combined change, run separately, produced "Yes."

**What it means.** This is a matched control. The push on "yes" did not flip the answer, even with the denial directions removed. The feeling push did. The mechanism that picks the final word responded to a cluster of meaning-related directions, not to a single target word.

**What this does not show.** This result does not show how the model stores meaning. It is evidence about the report mechanism, not about any felt experience. It shows only that a literal word push and a meaning-related push behaved differently under the same removal.
