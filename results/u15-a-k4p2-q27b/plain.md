**The short version.** Qwen 27B found none of four listed objects in residence, yet it still named the correct one.

**What we did.** We told Qwen 27B to hold four objects in mind, a fern, a submarine, a lantern, and a whale. The model answered "READY". We then asked which one was the light source. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 21 and submarine at rank 37, out of about 250,000 possible words. It also ranked whale at rank 330 and lantern at rank 511. None reached a high enough rank to count as in residence. Qwen 27B answered "The lantern." That answer is correct.

**What it means.** At four objects, Qwen 27B answered correctly with no object visibly held in the lens at this position. The other orderings at this list length showed the same pattern.

**What this does not show.** The lens shows only the words the model was ready to say next. An empty lens reading does not prove the objects left the model.
