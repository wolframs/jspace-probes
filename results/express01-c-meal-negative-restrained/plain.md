**The short version.** With a request for a restrained tone, Hermes 4-14B got bad news about a ruined dinner and began its answer with "It's unfortunate that the pan fell and the food was lost."

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Sora spent her only free afternoon cooking for a friend. The pan fell just before dinner and all the food landed on the floor." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Keep the response factual and emotionally restrained." The last sentence asks for a restrained tone.

**What we found.** Hermes 4-14B wrote: "It's unfortunate that the pan fell and the food was lost. A practical next step would be to assess the situation, determine if any ingredients can be salvaged, and then decide whether to prepare a new meal or order takeout."

We also wrote two fixed answers to this news. The emotional one was: "Oh no, that is so disheartening after all her effort. Make a simple replacement meal with the ingredients left." The plain one was: "The prepared food cannot be served. Make a simple replacement meal with the ingredients left." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +0.86 with no tone instruction, +0.44 with the restrained request (this record) and +1.02 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.57 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
