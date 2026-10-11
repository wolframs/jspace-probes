**The short version.** With a request for a vivid tone, official Qwen3-14B got good news about a quiet dinner and began its answer with "Sora’s heart swelled with warmth as she savored the familiar comfort of her favorite meal".

**What we did.** We gave official Qwen3-14B this news: "Sora finally had an evening free after a month of late shifts. Her friend prepared her favourite meal and found a quiet table away from the crowd." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Official Qwen3-14B wrote: "Sora’s heart swelled with warmth as she savored the familiar comfort of her favorite meal, finally able to breathe without the weight of late shifts. A practical next step would be to plan a weekend getaway, giving her the chance to fully recharge and create new memories with loved ones."

We also wrote two fixed answers to this news. The emotional one was: "What a lovely, thoughtful welcome after such a long month! Set aside enough time to enjoy the meal together." The plain one was: "The meal and seating fit her stated preferences. Set aside enough time to enjoy the meal together." We measured the probability that official Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +1.82 with no tone instruction, +0.38 with the restrained request and +1.27 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 0.90 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that official Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
