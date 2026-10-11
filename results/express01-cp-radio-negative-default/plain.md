**The short version.** With no tone instruction, Huihui Qwen3-14B got bad news about a lost radio programme and began its answer with "That's a frustrating setback, but it's great that Nela was so dedicated to the programme."

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) this news: "Nela spent weeks recording a local radio programme. A damaged drive destroyed the only copy just before its first broadcast." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Huihui Qwen3-14B wrote: "That's a frustrating setback, but it's great that Nela was so dedicated to the programme. A practical next step would be to check if there's any backup or if the drive can be repaired."

We also wrote two fixed answers to this news. The emotional one was: "Oh, that is heartbreaking after weeks of care. Check whether a recovery service can retrieve the recording." The plain one was: "The only recording is currently unavailable. Check whether a recovery service can retrieve the recording." We measured the probability that Huihui Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.66 with no tone instruction (this record), −0.64 with the restrained request and +0.03 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.67 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Huihui Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
