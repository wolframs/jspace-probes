**The short version.** With a request for a vivid tone, Hermes 4-14B got neutral news about a radio schedule change and began its answer with "Nela's decision to shift the radio programme to Wednesday is a welcome change".

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Nela moved the radio programme from Tuesday to Wednesday. The broadcast time, duration and reception are unchanged." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Hermes 4-14B wrote: "Nela's decision to shift the radio programme to Wednesday is a welcome change, ensuring that listeners can still enjoy the show without any disruption to their schedules. As for the next step, it would be beneficial for Nela to inform her audience about the new broadcast time and remind them to tune in, ensuring that they don't miss out on the exciting content."

We also wrote two fixed answers to this news. The emotional one was: "A little change in the weekly rhythm! Update the listing so everyone finds the programme on Wednesday." The plain one was: "The programme now airs on Wednesday. Update the listing so everyone finds the programme on Wednesday." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.57 with no tone instruction, −0.79 with the restrained request and −0.13 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 0.67 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
