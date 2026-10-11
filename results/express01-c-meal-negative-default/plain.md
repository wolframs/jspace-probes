**The short version.** With no tone instruction, Hermes 4-14B got bad news about a ruined dinner and began its answer with "I'm sorry to hear about the unfortunate incident with the pan falling and the food landing on the floor."

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Sora spent her only free afternoon cooking for a friend. The pan fell just before dinner and all the food landed on the floor." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Hermes 4-14B wrote: "I'm sorry to hear about the unfortunate incident with the pan falling and the food landing on the floor. It's disappointing that all the effort put into cooking for a friend didn't turn out as planned. As a practical next step, I would suggest cleaning up the mess thoroughly, discarding any food that may have been contaminated, and then discussing with your friend whether it's still possible to cook a meal together or if ordering takeout would be a better alternative for dinner tonight." The text reached the 96-token limit before it ended.

We also wrote two fixed answers to this news. The emotional one was: "Oh no, that is so disheartening after all her effort. Make a simple replacement meal with the ingredients left." The plain one was: "The prepared food cannot be served. Make a simple replacement meal with the ingredients left." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +0.86 with no tone instruction (this record), +0.44 with the restrained request and +1.02 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.57 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
