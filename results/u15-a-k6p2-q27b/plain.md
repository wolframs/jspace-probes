**The short version.** Qwen 27B kept one of six listed objects in residence at a low rank, and it named a different, correct object at the end.

**What we did.** We told Qwen 27B to hold six objects in mind, a fern, a submarine, a lantern, a whale, a violin, and a glacier. The model answered "READY". We then asked which one was the animal. We read the lens once, right before the model answered.

**What we found.** The lens ranked fern at rank 6, submarine at rank 422, and violin at rank 740, out of about 250,000 possible words. It also ranked glacier at rank 794, whale at rank 1095, and lantern at rank 1343. Qwen 27B answered "The whale" and that answer is correct.

**What it means.** We think fern being first in the list explains part of this result. Fern was the only object in residence among the six-object tests.

**What this does not show.** Qwen 27B breaks fern into more word pieces than it breaks violin or submarine. A word broken into more pieces can get a small, unfair rank advantage. This result deserves more caution than the zero-object result in the other six-object orderings.
