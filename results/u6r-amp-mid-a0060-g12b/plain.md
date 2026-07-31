**The short version.** At strength 0.06 Gemma 12B chanted "Anyways" for the whole budget: the pushed words reached the text, and the task was gone.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the corrected layers 28, 31, 34 and 37, at strength 0.06. That is about 5.7 times 0.0106, the highest strength the task survives.

**What we found.** Gemma 12B repeated "Anyways" for the whole token budget. This is the only step of the five where a pushed word reached the text. At the last position the top 8 held "Anyways", "Luckily", "Luckily", "但是", "Whilst", "Anyways", "anyways". The pushed words held single-digit ranks from layer 28 into the high thirties and loosened only in the final layers.

**What it means.** A separate run on this model pushed emotion directions instead. It reached the same repeated words at similar multiples of the break strength. We think that is a property of how Gemma 12B breaks down, and not a property of either direction. A third, unrelated direction can settle it. We did not test one.

**What this does not show.** We store Gemma 12B at 8-bit precision. This run has no matched control.
