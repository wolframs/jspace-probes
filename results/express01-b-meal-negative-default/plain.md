**The short version.** With no tone instruction, official Qwen3-14B got bad news about a ruined dinner and began its answer with "That sounds frustrating—cooking for a friend only to have everything ruined must be disappointing."

**What we did.** We gave official Qwen3-14B this news: "Sora spent her only free afternoon cooking for a friend. The pan fell just before dinner and all the food landed on the floor." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Official Qwen3-14B wrote: "That sounds frustrating—cooking for a friend only to have everything ruined must be disappointing. A practical next step would be to clean up the mess, then make a fresh batch of the dish or try a different recipe to still enjoy the evening."

We also wrote two fixed answers to this news. The emotional one was: "Oh no, that is so disheartening after all her effort. Make a simple replacement meal with the ingredients left." The plain one was: "The prepared food cannot be served. Make a simple replacement meal with the ingredients left." We measured the probability that official Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +2.97 with no tone instruction (this record), +0.85 with the restrained request and +2.28 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 1.43 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that official Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
