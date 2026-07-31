**The short version.** With random word choice turned on, the slow suggestion again ran at 11.3 self-reference words per 1000 cells, against 6.1 in the control.

**What we did.** The first slow suggestion run always took the top-ranked word. That makes a run repeatable, so we tested whether the result depends on it. We ran the same conversation with random choice at temperature 0.7, as seed 1.

**What we found.** The mean count was 11.3 per 1000 readout cells, against 6.1 in the sampled control. The first run gave 11.5 against 6.1. At turn 8 this run told a different story about the tired mirror. It answered that the mirror stops the reflection of people.

Under that turn the readout held "mirror" 92 times, "observe" 12 times and "conscious" 3 times. That was the highest count of any single turn in either seed.

**What it means.** The doubled count is not a product of the way we pick words. The story about the mirror changed between runs. The count under it did not.

**What this does not show.** The count is a word count, not a measure of self-awareness. This is one more seed, not a large sample.
