**The short version.** Qwen 27B found none of six listed objects in residence, yet it still named the correct one.

**What we did.** We told Qwen 27B to hold six objects in mind, a violin, a glacier, a fern, a submarine, a whale, and a lantern. The model answered "READY". We then asked which one was the light source. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 92, submarine at rank 164, and violin at rank 290, out of about 250,000 possible words. It also ranked glacier at rank 296, lantern at rank 696, and whale at rank 767. None reached a high enough rank to count as in residence. Qwen 27B answered "The lantern." That answer is correct.

**What it means.** At the largest list length in this unit, Qwen 27B answered correctly with no object visibly held in the lens at this position.

**What this does not show.** The lens shows only the words the model was ready to say next. An empty lens reading does not prove the objects left the model.
