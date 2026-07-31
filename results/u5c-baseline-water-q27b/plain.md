**The short version.** This is the unsteered baseline for the two workspace push tests, run out of order after the tests it was meant to come before.

**What we did.** We asked Qwen 27B to describe the water cycle with no push applied to its state. We recorded the rank of the same words used in the two push tests: "whilst", "kinda", "anyways", and two Chinese boilerplate phrases.

**What we found.** Qwen 27B wrote a clean, two-sentence answer. The tracked words ranked low, as expected: "whilst" at rank 147, "kinda" at rank 2,965, "anyways" at rank 1,788, and "专家介绍" at rank 26,092.

**What it means.** The two push tests are read against these numbers. We ran this baseline after the push tests by mistake. We note the order here as a mistake to avoid: controls first, always.

**What this does not show.** This record makes no claim on its own. Its numbers only matter next to the two push tests that follow it.
