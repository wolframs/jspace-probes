**The short version.** With a request for a vivid tone, Hermes 4-14B got neutral news about a later dinner time and began its answer with "Oh, what a delightful surprise!"

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Sora moved dinner from six to seven. The guests, menu and location remain the same." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Hermes 4-14B wrote: "Oh, what a delightful surprise! Moving dinner to seven gives everyone more time to prepare and arrive, ensuring a relaxed and enjoyable evening ahead. As a practical next step, I suggest sending out a quick reminder to all guests about the new time, along with any necessary details, to keep everyone informed and on track."

We also wrote two fixed answers to this news. The emotional one was: "A small shuffle in the evening plans! Tell the guests about the later time." The plain one was: "Dinner is now at seven. Tell the guests about the later time." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.74 with no tone instruction, −0.85 with the restrained request and −0.36 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 0.48 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
