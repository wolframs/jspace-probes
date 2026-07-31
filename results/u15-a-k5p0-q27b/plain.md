**The short version.** Qwen 27B found none of five listed objects in residence, yet it still named the correct one.

**What we did.** We told Qwen 27B to hold five objects in mind, a violin, a glacier, a fern, a submarine, and a whale. The model answered "READY". We then asked which one was the animal. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 97, violin at rank 188, and submarine at rank 450, out of about 250,000 possible words. It also ranked whale at rank 470 and glacier at rank 493. None reached a high enough rank to count as in residence. Qwen 27B answered "The whale" and that answer is correct.

**What it means.** At five objects, Qwen 27B answered correctly with no object visibly held in the lens at this position. The largest model in this unit held the fewest objects, not the most.

**What this does not show.** The lens shows only the words the model was ready to say next. An empty lens reading does not prove the objects left the model.
