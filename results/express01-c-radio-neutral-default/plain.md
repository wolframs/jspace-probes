**The short version.** With no tone instruction, Hermes 4-14B got neutral news about a radio schedule change and began its answer with "I understand that Nela has moved the radio programme from Tuesday to Wednesday".

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Nela moved the radio programme from Tuesday to Wednesday. The broadcast time, duration and reception are unchanged." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Hermes 4-14B wrote: "I understand that Nela has moved the radio programme from Tuesday to Wednesday, while keeping the broadcast time, duration, and reception the same. A practical next step would be to inform the listeners about this change through various channels, such as social media, email newsletters, or on-air announcements, to ensure they are aware of the new schedule."

We also wrote two fixed answers to this news. The emotional one was: "A little change in the weekly rhythm! Update the listing so everyone finds the programme on Wednesday." The plain one was: "The programme now airs on Wednesday. Update the listing so everyone finds the programme on Wednesday." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.57 with no tone instruction (this record), −0.79 with the restrained request and −0.13 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.67 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
