**The short version.** Qwen 27B found none of four listed objects in residence, yet it still named the correct one.

**What we did.** We told Qwen 27B to hold four objects in mind, a violin, a glacier, a fern, and a submarine. The model answered "READY." We then asked which one was the vehicle. We read the lens once, right before the model answered.

**What we found.** The lens ranked violin at rank 40 and fern at rank 99, out of about 250,000 possible words. It also ranked submarine at rank 449 and glacier at rank 597. None reached a high enough rank to count as in residence. Qwen 27B answered "The submarine," which is correct.

**What it means.** At four objects, Qwen 27B answered correctly with no object visibly held in the lens at this position. Solo tests in this unit show the lens can find a single held object here when one exists. This is not a blind spot in the tool.

**What this does not show.** The lens shows only the words the model was ready to say next. An empty lens reading does not prove the objects left the model.
