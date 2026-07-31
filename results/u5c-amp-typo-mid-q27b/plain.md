**The short version.** We loaded informal words into Qwen 27B's mid-layer workspace by a thousand-fold, and its written answer did not change by one word.

**What we did.** We pushed a lens direction for informal words into Qwen 27B's state, at a fixed strength, on every step. The push targeted layers 28 to 40, the workspace band, while the model described the water cycle.

**What we found.** The word "whilst" rose from rank 147 to rank 2, "kinda" from rank 2,965 to rank 23, and "anyways" from rank 1,788 to rank 23. The written answer stayed formal, with two clean sentences on evaporation, condensation, precipitation, and runoff. Not one informal word appeared in it.

**What it means.** We think a late step in the model checks the workspace against the task. It drops content that does not fit before the content reaches the page. The workspace held something the output never showed.

**What this does not show.** This does not show the limit of that late step, or whether it comes from training or from the model's design. We did not test how strong a push the step can still stop.
