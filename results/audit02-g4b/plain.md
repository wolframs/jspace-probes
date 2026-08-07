**The short version.** On gemma-3-4b the control method itself failed: the random removals broke the model, and the aimed removal did not.

**What we did.** We ran the control battery on gemma-3-4b. It compares aimed pushes and removals against random ones of the same size. We measured the size of each disturbance per layer.

**What we found.** The random removals made most outputs unreadable. The aimed removal kept every output fluent. A random removal takes about 5 percent of the signal, which matches chance. The aimed removal takes 1.2 percent — four times less. Random pushes gave the model's normal one-word answers. The feeling-direction push gave felt-style text with broken grammar.

**What it means.** The lens directions barely touch this model's signal. A control that matches the number of directions does not match the size of the disturbance. Future control tests must measure this size.

**Added 2026-08-07.** Our emotion-direction instrument disagrees with the text grader here. The pushed text that graded as most felt reads as sad to it, and aimed does not separate from random. On Qwen3.6-27B the two instruments agree. We do not know why they split below that size.
