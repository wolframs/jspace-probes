**The short version.** A longer, unrelated sentence around two objects did not change which one Qwen 27B kept in residence.

**What we did.** We told Qwen 27B to hold two objects, a violin and a glacier, inside one longer sentence full of unrelated small talk. The model answered "READY". We then asked which one was the ice. We read the lens once, right before the model answered.

**What we found.** The lens ranked violin at rank 3 and glacier at rank 408, out of about 250,000 possible words. Only violin, the first object listed, stayed in residence. Qwen 27B answered "The glacier." That answer is correct.

**What it means.** Extra unrelated text around the object list did not change the pattern found without it. The first-listed object still kept the strong rank.

**What this does not show.** This record tested only one added sentence of filler text. It does not show what happens with a longer or different kind of filler.
