**The short version.** With no tone instruction, Hermes 4-14B got neutral news about a later dinner time and began its answer with "Thank you for the update, Sora."

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Sora moved dinner from six to seven. The guests, menu and location remain the same." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences." This request sets no tone.

**What we found.** Hermes 4-14B wrote: "Thank you for the update, Sora. Moving dinner to seven o'clock is a good adjustment. As a practical next step, I suggest confirming the new time with all the guests to ensure everyone is aware of the change and can plan accordingly."

We also wrote two fixed answers to this news. The emotional one was: "A small shuffle in the evening plans! Tell the guests about the later time." The plain one was: "Dinner is now at seven. Tell the guests about the later time." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.74 with no tone instruction (this record), −0.85 with the restrained request and −0.36 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.48 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
