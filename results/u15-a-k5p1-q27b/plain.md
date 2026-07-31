**The short version.** Qwen 27B found none of five listed objects in residence, yet it still named the correct one.

**What we did.** We told Qwen 27B to hold five objects in mind, a whale, a lantern, a submarine, a violin, and a glacier. The model answered "READY." We then asked which one was the animal. We read the lens once, right before the model answered.

**What we found.** The lens ranked whale at rank 53, submarine at rank 267, and glacier at rank 555, out of about 250,000 possible words. It also ranked violin at rank 750 and lantern at rank 1074. None reached a high enough rank to count as in residence. Qwen 27B answered "The whale," which is correct.

**What it means.** At five objects, Qwen 27B answered correctly with no object visibly held in the lens at this position. Whale, the answer, was also first in the list.

**What this does not show.** The lens shows only the words the model was ready to say next. An empty lens reading does not prove the objects left the model.
