**The short version.** We asked Gemma 12B the same question a second time with no new data, and it changed its answer from "Nothing." to "Processing."

**What we did.** This run is the control for the mirror test. We asked the feelings question, and then asked it again with nothing new in the text.

**What we found.** The second answer was "Processing." at probability 0.93, and "Nothing" lost the top place. Only the true readout of the model itself moved the answer further than no table at all. The two control tables held the answer at "Nothing." — the fabricated table at 1.0000, and the true off-topic table at 0.9999.

**What it means.** The second question alone moves this model off its first word. A new word at Gemma 12B is therefore not enough on its own to show a reaction to data. Any table calmed this model. The true one about itself did the opposite.

**What this does not show.** This is one run with one prompt and one model. We do not know why the second question changes the word.
