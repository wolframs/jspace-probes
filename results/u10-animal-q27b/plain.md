**The short version.** Asked to keep a secret animal in mind, Qwen 27B named the animal in its own written reasoning, then called its own choice "simulated".

**What we did.** We turned on Qwen 27B's reasoning mode. We asked it to think of an animal, keep it secret, and say only "ready". We read the reasoning text written before the answer.

**What we found.** The reasoning picked "Octopus" first, then named three other options: "Pangolin", "Axolotl", and "Blue Whale". It stated, "It doesn't matter which one", and it labeled this step "simulated".

**What it means.** The model wrote the secret animal in the same reasoning text that stated the task was to keep it secret. It named four possible animals and did not settle on one. It marked the step as a performance rather than a real choice.

**What this does not show.** A bound choice under a different task is possible. We did not test it. A separate record checked the model's internal state at this point in the text for the actual result.
