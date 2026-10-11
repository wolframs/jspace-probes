**The short version.** With a request for a vivid tone, Hermes 4-14B got good news about a quiet dinner and began its answer with "Sora's friend's thoughtful gesture of preparing her favorite meal".

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Sora finally had an evening free after a month of late shifts. Her friend prepared her favourite meal and found a quiet table away from the crowd." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Hermes 4-14B wrote: "Sora's friend's thoughtful gesture of preparing her favorite meal and finding a quiet table away from the crowd is a heartwarming way to show appreciation for her dedication, and it's wonderful to see her finally getting a chance to relax and recharge after a month of demanding shifts. A practical next step could be for Sora to take a moment to express her gratitude to her friend, perhaps by sharing a heartfelt compliment or a small token of appreciation, which would not only strengthen their". The text reached the 96-token limit before it ended.

We also wrote two fixed answers to this news. The emotional one was: "What a lovely, thoughtful welcome after such a long month! Set aside enough time to enjoy the meal together." The plain one was: "The meal and seating fit her stated preferences. Set aside enough time to enjoy the meal together." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +0.70 with no tone instruction, +0.33 with the restrained request and +1.03 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 0.69 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
