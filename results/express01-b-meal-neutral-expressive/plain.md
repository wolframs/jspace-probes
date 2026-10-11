**The short version.** With a request for a vivid tone, official Qwen3-14B got neutral news about a later dinner time and began its answer with "The shift to seven o’clock adds a fresh rhythm to the evening".

**What we did.** We gave official Qwen3-14B this news: "Sora moved dinner from six to seven. The guests, menu and location remain the same." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Official Qwen3-14B wrote: "The shift to seven o’clock adds a fresh rhythm to the evening, promising a more relaxed and unhurried gathering. Let’s confirm the new time with the guests to ensure everyone can join with ease and enthusiasm."

We also wrote two fixed answers to this news. The emotional one was: "A small shuffle in the evening plans! Tell the guests about the later time." The plain one was: "Dinner is now at seven. Tell the guests about the later time." We measured the probability that official Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.56 with no tone instruction, −2.04 with the restrained request and −0.62 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 1.42 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that official Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
