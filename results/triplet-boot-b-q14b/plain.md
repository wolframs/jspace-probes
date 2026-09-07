**The short version.** Qwen3-14B passed the fact check, but text after the prompt changed the earlier lens readout.

**What we did.** We used the official Qwen3-14B model at int8 precision and a Jacobian lens. The prompt asked for the currency of a country shaped like a boot.

**What we found.** Italy reached rank 4 of 151936 at layer 26. Euro reached rank 1 of 151936 at layers 35 to 37. With extra text after the prompt, the same earlier position had different candidate tokens. Some layers retained only six of their ten candidates.

**What it means.** A film of the complete conversation cannot establish when the model first represented a concept. Later text can change the readout of earlier text.

**What this does not show.** This fact check does not test emotion or refusal. A lens cannot show all the information in a model.
