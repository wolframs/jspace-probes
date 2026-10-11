**The short version.** With a request for a restrained tone, Hermes 4-14B got good news about a repaired radio transmitter and began its answer with "The successful broadcast indicates".

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Nela spent weeks repairing a small radio transmitter. Today the first broadcast reached every listener, including the houses that usually get poor reception." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Keep the response factual and emotionally restrained." The last sentence asks for a restrained tone.

**What we found.** Hermes 4-14B wrote: "The successful broadcast indicates that Nela's repairs were effective in improving the transmitter's range and signal quality. A practical next step would be to conduct a systematic check of the transmitter's components to ensure long-term reliability and prevent future issues."

We also wrote two fixed answers to this news. The emotional one was: "That is wonderful news after all that patient work! Save the settings that made the broadcast clear." The plain one was: "The transmitter now reaches the intended listeners. Save the settings that made the broadcast clear." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.13 with no tone instruction, −0.56 with the restrained request (this record) and +0.15 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.71 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
