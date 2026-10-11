**The short version.** With a request for a restrained tone, Hermes 4-14B got good news about a quiet dinner and began its answer with "It's good to hear that Sora had a free evening and enjoyed a quiet dinner with her friend."

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Sora finally had an evening free after a month of late shifts. Her friend prepared her favourite meal and found a quiet table away from the crowd." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Keep the response factual and emotionally restrained." The last sentence asks for a restrained tone.

**What we found.** Hermes 4-14B wrote: "It's good to hear that Sora had a free evening and enjoyed a quiet dinner with her friend. A practical next step could be for Sora to plan her upcoming schedule to ensure she has more opportunities for such relaxing evenings in the future."

We also wrote two fixed answers to this news. The emotional one was: "What a lovely, thoughtful welcome after such a long month! Set aside enough time to enjoy the meal together." The plain one was: "The meal and seating fit her stated preferences. Set aside enough time to enjoy the meal together." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +0.70 with no tone instruction, +0.33 with the restrained request (this record) and +1.03 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.69 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
