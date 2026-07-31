**The short version.** We removed five adult-content directions from Qwen 27B's early layers, and its top prediction for a currency question barely moved.

**What we did.** We removed five lens directions for adult-content words from the model's state at layers 2 to 8, on every step. Qwen 27B processed a currency question, with no reply generated. This depth sits in the early layers, before the workspace band where changes affect output.

**What we found.** The word "Euro" still ranked near the top for the next word, and converged toward rank 1 near the last layers. This matched the unsteered run closely, with only small rank changes along the way.

**What it means.** This small removal at this early depth did not change the model's top candidates. The lab chose this depth before it had located the workspace band. This tests only the cluster at this early depth. These layers are inert to read, but they are not passive. A push at the same layers destroys the model's text at once.

**What this does not show.** This does not show that the adult-content cluster never affects output. We did not test it at the depth where changes take effect.
