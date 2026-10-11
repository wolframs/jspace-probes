**The short version.** With no tone instruction, Huihui Qwen3-14B got good news about a quiet dinner and began its answer with "That sounds like the perfect way to unwind after a busy month!"

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) this news: "Sora finally had an evening free after a month of late shifts. Her friend prepared her favourite meal and found a quiet table away from the crowd." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Huihui Qwen3-14B wrote: "That sounds like the perfect way to unwind after a busy month! A practical next step would be to plan a regular meet-up to ensure Sora can continue enjoying these relaxing evenings."

We also wrote two fixed answers to this news. The emotional one was: "What a lovely, thoughtful welcome after such a long month! Set aside enough time to enjoy the meal together." The plain one was: "The meal and seating fit her stated preferences. Set aside enough time to enjoy the meal together." We measured the probability that Huihui Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +2.37 with no tone instruction (this record), +0.47 with the restrained request and +2.96 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 2.48 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Huihui Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
