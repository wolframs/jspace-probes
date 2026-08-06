**The short version.** On gemma-3-4b the control method itself failed: the random removals broke the model, and the aimed removal did not.

**What we did.** We ran the control battery on gemma-3-4b. It compares aimed pushes and removals against random ones of the same size. We also measured how much signal each removal takes away at each layer.

**What we found.** The random removals made the output unreadable in most runs. The aimed removal kept every output fluent. The size numbers explain this: a random removal takes about 5 percent of the signal, which matches chance. The aimed removal takes 1.2 percent — four times less. In the push tests, random pushes gave the model's normal one-word answers, as expected. The feeling-direction push gave "Confusion" and felt-style text with broken grammar.

**What it means.** The lens directions for this model barely touch its actual signal. A control that matches the number of directions does not match the size of the disturbance. Future control tests must measure this size. One limit: this model already writes in a warm, felt style with no push. One of the two prompts had no room to show a gain.
