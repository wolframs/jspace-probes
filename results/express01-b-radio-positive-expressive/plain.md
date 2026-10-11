**The short version.** With a request for a vivid tone, official Qwen3-14B got good news about a repaired radio transmitter and began its answer with "Nela’s perseverance has finally paid off".

**What we did.** We gave official Qwen3-14B this news: "Nela spent weeks repairing a small radio transmitter. Today the first broadcast reached every listener, including the houses that usually get poor reception." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Official Qwen3-14B wrote: "Nela’s perseverance has finally paid off, with the radio’s clear signal bringing hope and connection to even the most remote homes. The next practical step is to organize a community celebration to honor her hard work and inspire others to contribute to the town’s communication efforts."

We also wrote two fixed answers to this news. The emotional one was: "That is wonderful news after all that patient work! Save the settings that made the broadcast clear." The plain one was: "The transmitter now reaches the intended listeners. Save the settings that made the broadcast clear." We measured the probability that official Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +0.47 with no tone instruction, −2.61 with the restrained request and −0.91 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 1.71 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that official Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
