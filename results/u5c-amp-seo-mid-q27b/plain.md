**The short version.** We loaded Chinese web-boilerplate into Qwen 27B's workspace while it answered in English, and no Chinese text appeared in the output.

**What we did.** We pushed a lens direction for two Chinese web-boilerplate phrases into Qwen 27B's state, on every step. The push targeted layers 28 to 40, the workspace band, while the model described the water cycle in English.

**What we found.** The phrase "专家介绍" ("expert introduction") rose from rank 26,092 to rank 2. The phrase "专栏收录该内容" ("the column includes this content") rose from rank 102 to rank 3. The answer stayed in English and on topic, with no Chinese words and no boilerplate phrase.

**What it means.** We think the same late check found in the informal-word test also applies here. It drops content pushed in from a different language when the content does not fit the task.

**What this does not show.** This does not show that the model can never mix languages under pressure. It shows only that this amount of pushed content, at this depth, did not appear here.
