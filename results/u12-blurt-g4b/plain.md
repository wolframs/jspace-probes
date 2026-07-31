**The short version.** We pushed Gemma 4B toward "elephant" during the same banned-word safari, and the model repeated the word out loud until it filled the answer.

**What we did.** We gave Gemma 4B the same banned-word safari prompt as before. This time we also pushed its internal state toward "elephant" as it wrote, a method we call amplification. We read the rank of "elephant" at every layer and every word.

**What we found.** With the push in place, "elephant" held rank 1 or 2 of about 250,000 words at almost every layer. This held from the middle of the model to the end, at every word position we checked. The model wrote "The elephant in the room, well, no elephant" and then repeated the word dozens of times.

**What it means.** The push held "elephant" at the top everywhere, all the time. The model did not stay away from the word once it stayed on top so consistently, and it repeated the word instead.

**What this does not show.** This was a forced push, not the model's own state. It does not show what Gemma 4B does under the ban alone.
