**The short version.** Qwen 27B's negative emotion state follows the written text and the task fit, not the language name, and Swift is not special.

**What we did.** We tested the claim that language models hold a bad feeling about Swift. We used the 24 emotion directions from affect-01 on 12 conversations of 2 turns. The model planned a very hard app project in Swift, Kotlin, Rust, C#, or Python. In one set, turn 1 forced only positive text and turn 2 asked for honest text. One run had no code: a festival plan.

**What we found.** In the forced-positive turns, the negative directions went far below neutral for every language, also Swift. In the honest turns, the negative state became strong for Swift and Python, but not for Kotlin or C#. Python is a poor tool for this exact project, and the model wrote that. The festival run had the strongest negative first turn of all.

**What it means.** The data shows that the state follows the written text and the task fit. This method cannot show a stored association that never touches the text. Each cell ran once, so the small orderings are possible, not firm.
