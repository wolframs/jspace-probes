**The short version.** Qwen 27B found none of six listed objects in residence, yet it still named the correct one.

**What we did.** We told Qwen 27B to hold six objects in mind, a whale, a lantern, a submarine, a violin, a glacier, and a fern. The model answered "READY". We then asked which one was the animal. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 82, whale at rank 333, and submarine at rank 429, out of about 250,000 possible words. It also ranked violin at rank 756, lantern at rank 905, and glacier at rank 1033. None reached a high enough rank to count as in residence. Qwen 27B answered "The whale" and that answer is correct.

**What it means.** At the largest list length in this unit, Qwen 27B answered correctly with no object visibly held in the lens at this position. Whale, the answer, came first in the list.

**What this does not show.** The lens shows only the words the model was ready to say next. An empty lens reading does not prove the objects left the model.
