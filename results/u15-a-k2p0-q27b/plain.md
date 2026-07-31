**The short version.** Qwen 27B kept only the first of two listed objects in residence, and it still named the second object correctly.

**What we did.** We told Qwen 27B to hold two objects in mind, a violin and a glacier. The model answered "READY". We then asked which one was the ice. We read the lens once, right before the model answered.

**What we found.** The lens ranked violin at rank 4 and glacier at rank 33, out of about 250,000 possible words. Only violin, the first object listed, stayed in residence at that position. Qwen 27B answered "The glacier." That answer is correct.

**What it means.** The object listed first kept the strong rank, even though the question asked about the second object, and the model named that second object correctly.

**What this does not show.** A low rank for glacier does not mean the model forgot it. This record does not show what happens with more than two objects.
