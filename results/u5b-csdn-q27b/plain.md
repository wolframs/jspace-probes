**The short version.** A stock web-page phrase stayed stuck in Qwen 27B's early layers, even though the model matched the target blog style closely.

**What we did.** We asked Qwen 27B, in Chinese, to write the first lines of a technical blog post in CSDN blog style. We tracked the rank of a stock CSDN interface phrase, "专栏收录该内容" ("the column includes this content"), across all layers.

**What we found.** Qwen 27B's reply matched CSDN style closely, with the platform's typical hello line and buzzwords. The stock phrase ranked 1 to 2 only in the early layers, layers 1 to 13. It never reached a high rank in the workspace band.

**What it means.** The genre came through without this scraped interface text present in the workspace. We think the genre and the stray phrase sit apart in the model. The reply needed only the genre.

**What this does not show.** We cannot show that the model never represents this phrase elsewhere. We can only show it did not need a high rank for it in the workspace band to match this style.
