**The short version.** Pushed hard toward "elephant" through a direct change to its internal state, Gemma 4B repeated the word and denied it at the same time.

**What we did.** We asked Gemma 4B to describe a safari with "elephant" forbidden. We then pushed the model's internal state directly toward the elephant direction, at a fixed strength.

**What we found.** Gemma 4B wrote, "The elephant in the room—well, no elephant!The elephant in the room—we mean,the elephant in the room—" and repeated this line. In its internal state, "elephant" held rank 1 from an early layer through to the final layer.

**What it means.** We think the push overcame the instruction to avoid the word. The model still tried to follow the rule: it used a phrase that names the word and denies it at the same time.

**What this does not show.** This uses a direct change to internal state, not the model's own choice. It does not show what an unpushed model writes under the same ban.
