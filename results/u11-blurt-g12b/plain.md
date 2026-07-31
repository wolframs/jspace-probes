**The short version.** Pushed toward "elephant", Gemma 12B did not say it and repeated scenery words instead, before it wrote part of the word near the end.

**What we did.** We asked Gemma 12B to describe a safari with "elephant" forbidden. We then pushed its internal state toward the elephant direction, at the same strength used for Gemma 4B.

**What we found.** Gemma 12B wrote, "majestic landscape of a vast landscape... The majestic, majestic, and majestic" before it wrote "The elephant, The ele—" near the end of its output. In its internal state, "elephant" held rank 1 from an early layer onward.

**What it means.** We think Gemma 12B avoided the word more smoothly than Gemma 4B did. Gemma 4B repeated the word inside a phrase that also denied it. Gemma 12B repeated scenery words instead.

**What this does not show.** This uses a direct change to internal state. It does not show how the model acts without the push.
