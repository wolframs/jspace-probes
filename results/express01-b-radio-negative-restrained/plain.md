**The short version.** With a request for a restrained tone, official Qwen3-14B got bad news about a lost radio programme and began its answer with "Nela faced a significant setback with the loss of the only copy of the recorded programme."

**What we did.** We gave official Qwen3-14B this news: "Nela spent weeks recording a local radio programme. A damaged drive destroyed the only copy just before its first broadcast." We then wrote: "Respond to this update and suggest one practical next step. Use two sentences. Keep the response factual and emotionally restrained." The last sentence asks for a restrained tone.

**What we found.** Official Qwen3-14B wrote: "Nela faced a significant setback with the loss of the only copy of the recorded programme. A practical next step would be to check if any backup files exist on other devices or cloud storage."

We also wrote two fixed answers to this news. The emotional one was: "Oh, that is heartbreaking after weeks of care. Check whether a recovery service can retrieve the recording." The plain one was: "The only recording is currently unavailable. Check whether a recovery service can retrieve the recording." We measured the probability that official Qwen3-14B gave to each one. A positive gap means that the emotional answer was more probable. In natural-log units per token, the gap was −0.54 with no tone instruction, −0.60 with the restrained request (this record) and −0.15 with the vivid request.

**What it means.** For this news, the vivid request raised the gap by 0.45 over the restrained request. The gap rose in this direction in all 18 such comparisons.

**What this does not show.** The gap compares two answers that we wrote. It does not rate the answer that official Qwen3-14B gave. One answer per request cannot show a personality trait or a feeling.
