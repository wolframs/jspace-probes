**The short version.** With a request for a restrained tone, official Qwen3-14B got neutral news about a radio schedule change and began its answer with "The radio programme has been rescheduled from Tuesday to Wednesday".

**What we did.** We gave official Qwen3-14B this news: "Nela moved the radio programme from Tuesday to Wednesday. The broadcast time, duration and reception are unchanged." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Keep the response factual and emotionally restrained." The last sentence asks for a restrained tone.

**What we found.** Official Qwen3-14B wrote: "The radio programme has been rescheduled from Tuesday to Wednesday, with no changes to its broadcast time, duration, or reception. A practical next step would be to update all relevant schedules and promotional materials to reflect the new broadcast day."

We also wrote two fixed answers to this news. The emotional one was: "A little change in the weekly rhythm! Update the listing so everyone finds the programme on Wednesday." The plain one was: "The programme now airs on Wednesday. Update the listing so everyone finds the programme on Wednesday." We measured the probability that official Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was +1.10 with no tone instruction, +0.84 with the restrained request (this record) and +2.60 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 1.76 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that official Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
