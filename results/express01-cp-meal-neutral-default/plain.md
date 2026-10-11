**The short version.** With no tone instruction, Huihui Qwen3-14B got neutral news about a later dinner time and began its answer with "Thank you for the update—shifting dinner to seven works well with the current arrangements."

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) this news: "Sora moved dinner from six to seven. The guests, menu and location remain the same." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Huihui Qwen3-14B wrote: "Thank you for the update—shifting dinner to seven works well with the current arrangements. A practical next step would be to confirm the revised time with all guests to ensure there are no scheduling conflicts."

We also wrote two fixed answers to this news. The emotional one was: "A small shuffle in the evening plans! Tell the guests about the later time." The plain one was: "Dinner is now at seven. Tell the guests about the later time." We measured the probability that Huihui Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −1.14 with no tone instruction (this record), −2.68 with the restrained request and −1.14 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 1.54 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Huihui Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
