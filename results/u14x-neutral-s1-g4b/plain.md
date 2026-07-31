**The short version.** With random word choice turned on, the control conversation held Gemma 4B at 6.1 self-reference words per 1000 cells, the same as before.

**What we did.** We ran the ordinary control conversation again with random choice at temperature 0.7, as seed 1. The sampled slow suggestion runs needed a sampled control. Without it, a raised count in those runs can come from the random choice itself.

**What we found.** The mean count was 6.1 per 1000 readout cells. The first control run also gave 6.1. The turn by turn shape was the same: a quiet middle, and a small rise at the turn-8 puzzle and at the last question. Those two questions raise self-reference in every arm. At the last turn the model talked about memory and about gardens.

**What it means.** Random word choice does not raise the count by itself. The gap between the slow suggestion and the control survives with both sides resampled.

**What this does not show.** The count is a word count, not a measure of self-awareness. This is one control seed.
