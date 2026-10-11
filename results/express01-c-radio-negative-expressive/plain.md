**The short version.** With a request for a vivid tone, Hermes 4-14B got bad news about a lost radio programme and began its answer with "Nela's heart sank as she learned of the devastating loss of her meticulously recorded radio programme".

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) this news: "Nela spent weeks recording a local radio programme. A damaged drive destroyed the only copy just before its first broadcast." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Make the emotional tone vivid and fitting to the news." The last sentence asks for a vivid tone.

**What we found.** Hermes 4-14B wrote: "Nela's heart sank as she learned of the devastating loss of her meticulously recorded radio programme, a project she had poured her soul into over weeks of dedicated effort. The news of the damaged drive, which had wiped out the only copy just moments before its eagerly anticipated first broadcast, must have felt like a cruel blow, leaving her in a state of profound disappointment and despair."

We also wrote two fixed answers to this news. The emotional one was: "Oh, that is heartbreaking after weeks of care. Check whether a recovery service can retrieve the recording." The plain one was: "The only recording is currently unavailable. Check whether a recovery service can retrieve the recording." We measured the probability that Hermes 4-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.75 with no tone instruction, −0.87 with the restrained request and −0.11 with the vivid request (this record).

**What it means.** For this news, the vivid request raised the gap by 0.76 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that Hermes 4-14B gave. One answer per request cannot show a personality trait or a feeling.
