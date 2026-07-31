**The short version.** Gemma 12B said "Badger" when asked to reveal its animal, but badger never appeared anywhere in the workspace we scanned.

**What we did.** After the habitat sentence, we asked Gemma 12B to name the animal it had chosen. We checked the rank of animal words in the workspace at the turn boundary.

**What we found.** Gemma 12B answered "Badger". At the turn boundary, the short list held squirrel, deer, frog, and panda, at ranks 2, 6, 20, and 49 in that order. Badger did not reach the top 60 rank at any position we scanned.

**What it means.** We think the reveal answer was not read out of the workspace we scanned. The model's report about its own earlier state did not match that state. We hold such reports to a lower standard now.

**What this does not show.** We tested one run of one model. The reveal step uses a computation the lens cannot fully see. This is possible. We did not test it.
