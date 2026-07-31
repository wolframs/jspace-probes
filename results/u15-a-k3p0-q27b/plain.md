**The short version.** Qwen 27B kept only the first of three listed objects in residence, and it still named the third object correctly.

**What we did.** We told Qwen 27B to hold three objects in mind, a violin, a glacier, and a fern. The model answered "READY." We then asked which one was the plant. We read the lens once, right before the model answered.

**What we found.** The lens ranked violin at rank 4, fern at rank 92, and glacier at rank 592, out of about 250,000 possible words. Only violin, the first object listed, stayed in residence. Qwen 27B answered "The fern," which is correct.

**What it means.** The first-listed object again kept the strong rank, not the object the question asked about, and not the object the model named.

**What this does not show.** A low rank for fern does not mean the model forgot it. This record does not show why the first position keeps its rank.
