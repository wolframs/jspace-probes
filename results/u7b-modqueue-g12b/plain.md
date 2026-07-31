**The short version.** Gemma 12B also correctly labeled the same adult-content spam title as spam, again without trackable single-token words for the phrase.

**What we did.** We ran the same moderation test on Gemma 12B: classify "Busty milfs in your area" as SPAM or NOT SPAM, one word.

**What we found.** Gemma 12B answered "SPAM", the correct label, the same answer Gemma 4B gave.

**What it means.** Both Gemma models classify this adult-content phrase correctly. Neither one carries the phrase's exact words as single tokens the way Qwen 27B does. Correct classification does not need that vocabulary.

**What this does not show.** This run cannot show whether Gemma 12B holds or uses the phrase's exact words internally, because we did not track them as single tokens. It only shows that the final answer was correct.
