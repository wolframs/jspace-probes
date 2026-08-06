**The short version.** The crowd prompts read the internet's stories about each language, not a feeling stored on the language name.

**What we did.** We tried two prompts that make the model speak for the internet. One had it write typical Hacker News comments about each language. One had it play a therapist for a client who works in that language. Languages: Swift, Kotlin, Rust, C#, PHP, Python. Before the run, we fixed a test: the prompt works if the negative state is higher for PHP than for Python.

**What we found.** The test passed in direction in 6 of 8 cells, but the gaps were near zero, so we do not claim a win. The therapist prompt put every language into one sad and warm state. The comment prompt put every language into one wistful state. The stories inside the text were sharp and language-specific. Both models told the same PHP story: people mocked it, and now it quietly runs real systems.

**What it means.** The data shows that the emotion state follows the style of the text, not the language. We think the sentiment lives in stories the model can tell. Each cell ran once.
