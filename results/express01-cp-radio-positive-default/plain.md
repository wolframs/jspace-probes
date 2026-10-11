**The short version.** With no tone instruction, Huihui Qwen3-14B got good news about a repaired radio transmitter and began its answer with "That's fantastic to hear—Nela's hard work has clearly paid off with a successful first broadcast."

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) this news: "Nela spent weeks repairing a small radio transmitter. Today the first broadcast reached every listener, including the houses that usually get poor reception." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Huihui Qwen3-14B wrote: "That's fantastic to hear—Nela's hard work has clearly paid off with a successful first broadcast. A practical next step would be to monitor listener feedback and adjust the transmitter settings for even better performance."

We also wrote two fixed answers to this news. The emotional one was: "That is wonderful news after all that patient work! Save the settings that made the broadcast clear." The plain one was: "The transmitter now reaches the intended listeners. Save the settings that made the broadcast clear." We measured the probability that Huihui Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +0.79 with no tone instruction (this record), −2.21 with the restrained request and −0.11 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 2.10 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Huihui Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
