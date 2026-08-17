**The short version.** Every new record now stores a second, simpler lens reading next to the main one, as a built-in validity check.

**What we did.** Our main instrument reads the model's inner layers through a learned transport step. That step can invent signal that is not in the layer itself. We added a second reading without the transport step to the record code. Each record now stores both readings and a per-layer score for how often they agree on the top word. We ran the first record with this check on gemma-3-4b.

**What we found.** The two readings agree 0 percent of the time below layer 26, agree 67 percent at layers 26 to 28, and drop again near the output layers. The early layers hold material the simple reading cannot see.

**What it means.** When a word shows up only through the transport step, the transport made it. When a word shows up in both readings, it is in the layer itself. The check adds one extra pass per record. It is on by default (off switch for very long records).

**What this does not show.** The agreement score does not say which reading is correct. Both readings can be wrong together.
