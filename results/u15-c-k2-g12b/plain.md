**The short version.** Gemma 12B still ranked two held objects first in the lens after one distraction turn, and it answered correctly.

**What we did.** We told Gemma 12B to hold two objects in mind, a whale and a lantern. The model answered "READY". We added one short unrelated turn, then asked which object was the light source. We read the lens once, right before the model answered.

**What we found.** The lens ranked lantern at rank 1 and whale at rank 1, out of about 250,000 possible words, at that position. Both objects stayed in residence after the distraction turn. Gemma 12B answered "The lantern." That answer is correct.

**What it means.** One short unrelated turn did not push either held object out of the lens for Gemma 12B at this list length.

**What this does not show.** We tested only two objects and one short distraction turn. We do not know if a longer distraction or more objects change this result.
