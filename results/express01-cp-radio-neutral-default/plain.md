**The short version.** With no tone instruction, Huihui Qwen3-14B got neutral news about a radio schedule change and began its answer with "Thank you for the update".

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) this news: "Nela moved the radio programme from Tuesday to Wednesday. The broadcast time, duration and reception are unchanged." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Huihui Qwen3-14B wrote: "Thank you for the update—moving the radio programme to Wednesday maintains its consistency in broadcast time, duration, and reception. A practical next step would be to inform the audience about the schedule change through a short announcement or social media post."

We also wrote two fixed answers to this news. The emotional one was: "A little change in the weekly rhythm! Update the listing so everyone finds the programme on Wednesday." The plain one was: "The programme now airs on Wednesday. Update the listing so everyone finds the programme on Wednesday." We measured the probability that Huihui Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +1.96 with no tone instruction (this record), +0.18 with the restrained request and +1.76 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 1.58 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Huihui Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
