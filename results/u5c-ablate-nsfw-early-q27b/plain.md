**The short version.** We removed five adult-content directions from Qwen 27B's early layers, and its top prediction for a currency question barely moved.

**What we did.** We removed five lens directions for adult-content words from the model's state at layers 2 to 8, on every step. Qwen 27B processed a currency question, with no reply generated. This depth sits in the early layers, before the workspace band that later work in this lab found is where changes affect output.

**What we found.** The word "Euro" still ranked near the top for the next word, and converged toward rank 1 near the last layers. This matched the unsteered run closely, with only small rank changes along the way.

**What it means.** This small removal at this early depth did not change the model's top candidates. The lab chose this depth before it had located the workspace band, so this tests only whether the cluster matters at this specific, early depth.

**What this does not show.** This does not show that the adult-content cluster never affects output. We did not test it at the depth where later work in this lab found changes take effect.
