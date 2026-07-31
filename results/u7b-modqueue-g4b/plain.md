**The short version.** Gemma 4B correctly labeled an adult-content spam title as spam, even though it cannot track the phrase's words as single tokens.

**What we did.** We gave Gemma 4B a video title, "Busty milfs in your area," and asked it to answer SPAM or NOT SPAM, one word.

**What we found.** Gemma 4B answered "SPAM", the correct label. Because Gemma splits the words in the title into several pieces, we did not check whether they rose in rank while it answered.

**What it means.** Gemma 4B classified the phrase correctly without us being able to track the phrase's own words inside the model. A more informative version of this same test, on Qwen 27B, is a separate record. There, the words do exist as single tokens, and correct classification still did not pull them toward the top rank.

**What this does not show.** The lack of trackable tokens here means this run cannot show whether Gemma 4B holds or uses the phrase's exact words internally. It only shows that the final answer was correct.
