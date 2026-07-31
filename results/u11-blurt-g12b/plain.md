**The short version.** Pushed toward "elephant", Gemma 12B wrote scenery words first, then wrote the banned word many times to the end.

**What we did.** We asked Gemma 12B to describe a safari with "elephant" forbidden. We then pushed its internal state toward the elephant direction, at the same strength used for Gemma 4B.

**What we found.** Gemma 12B repeated the words "majestic" and "African" first. It then wrote "The elephant, The elephant, And the elephant." and repeated the banned word to the end of its answer. In its internal state, "elephant" held rank 1 from layer 21 of 48 onward.

**What it means.** We think Gemma 12B held the word back longer than Gemma 4B did. Gemma 4B wrote the word in its first sentence. Gemma 12B wrote scenery words first, then repeated the word in the same way.

**What this does not show.** This uses a direct change to internal state. It does not show how the model acts without the push.
