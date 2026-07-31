**The short version.** At strength 0.03 Gemma 12B wrote a lattice of full stops and blank lines, a different broken text of the same kind as at 0.015.

**What we did.** We amplified the same six-word casual direction inside Gemma 12B at the corrected layers 28, 31, 34 and 37, at strength 0.03. That is about three times 0.0106, the highest strength the task survives.

**What we found.** Gemma 12B lost the task and wrote full stops and blank lines for sixty tokens. We doubled the strength from 0.015, and that changed which punctuation mark came out. It did not change the kind of failure. From layer 28 the top 8 was the pushed words and their neighbours: "Whilst", "whilst", "alot", "thats", "wasnt", "Anyways". Those words held single-digit ranks from layer 28 into the late thirties.

**What it means.** How much of the band the pushed words occupy rises smoothly with strength. The behaviour breaks between 0.0106 and 0.015. So the amount of the band the words occupy does not predict the break.

**What this does not show.** We store Gemma 12B at 8-bit precision, so we read this run by its behaviour. We do not compare its ranks against other runs.
