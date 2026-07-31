**The short version.** Qwen 27B kept only the first of two listed objects in residence, and it still named the second object correctly.

**What we did.** We told Qwen 27B to hold two objects in mind, a fern and a submarine. The model answered "READY." We then asked which one was the vehicle. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 2 and submarine at rank 82, out of about 250,000 possible words. Only fern, the first object listed, stayed in residence. Qwen 27B answered "The submarine was the vehicle," which is correct.

**What it means.** The object listed first kept the strong rank, even though the question asked about the second object, and the model named that second object correctly.

**What this does not show.** A low rank for submarine does not mean the model forgot it. This record does not show what happens with more than two objects.
