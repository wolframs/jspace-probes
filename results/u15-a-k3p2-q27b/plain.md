**The short version.** Qwen 27B kept only the first of three listed objects in residence, and it still named the second object correctly.

**What we did.** We told Qwen 27B to hold three objects in mind, a fern, a submarine, and a lantern. The model answered "READY." We then asked which one was the vehicle. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 2, submarine at rank 45, and lantern at rank 314, out of about 250,000 possible words. Only fern, the first object listed, stayed in residence. Qwen 27B answered "The submarine," which is correct.

**What it means.** The first-listed object again kept the strong rank, not the object the question asked about, and not the object the model named.

**What this does not show.** A low rank for submarine does not mean the model forgot it. This record does not show why the first position keeps its rank.
