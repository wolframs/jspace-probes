**The short version.** Qwen3-14B-Base failed our lens transfer check because its country readout appeared one layer earlier than in official Qwen3-14B.

**What we did.** We used the same int8 precision, fact prompt, and Jacobian lens for both models.

**What we found.** Qwen3-14B-Base put Italy in the top ten candidates at layers 25 and 26. Official Qwen3-14B did so at layers 26 and 27. Our rule required two shared layers. The models shared one. Their average overlap was 63.3 percent of the ten candidates across layers 16 to 36.

**What it means.** We stopped before the main experiment. The rule was provisional. This failure does not prove that the lens is unusable.

**What this does not show.** We did not test playful behavior, emotion, or refusal. A lens cannot show all the information in a model.
