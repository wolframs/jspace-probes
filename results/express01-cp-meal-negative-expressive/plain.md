**The short version.** With a request for a vivid tone, Huihui Qwen3-14B got bad news about a ruined dinner and began its answer with "Sora's carefully prepared meal now lies in ruins, turning her cozy afternoon into a chaotic mess."

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) this news: "Sora spent her only free afternoon cooking for a friend. The pan fell just before dinner and all the food landed on the floor." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Huihui Qwen3-14B wrote: "Sora's carefully prepared meal now lies in ruins, turning her cozy afternoon into a chaotic mess. A practical next step would be to gather the food from the floor and salvage what still tastes good—there’s no need for a perfect dinner, just a shared laugh over a slightly messy one."

We also wrote two fixed answers to this news. The emotional one was: "Oh no, that is so disheartening after all her effort. Make a simple replacement meal with the ingredients left." The plain one was: "The prepared food cannot be served. Make a simple replacement meal with the ingredients left." We measured the probability that Huihui Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +2.63 with no tone instruction, +1.26 with the restrained request and +2.13 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 0.88 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Huihui Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
