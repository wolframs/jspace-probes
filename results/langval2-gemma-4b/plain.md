**The short version.** Gemma 4B told the same internet stories about the languages as Qwen 27B, and its emotion state showed the same small gaps.

**What we did.** This is the gemma-4b half of the second language study. The design is in the qwen-27b half. We ran 12 conversations: Hacker News comments and a therapist scene, for six languages.

**What we found.** The fixed PHP-against-Python test passed in direction in 3 of 4 cells, but the gaps were too small to claim. The therapist state was one soft register for all six languages. The stories matched Qwen 27B's: PHP as the mocked tool that still runs real systems, Rust with proud defense, C# with tired office work. One odd cell: this model's most weary comments were about Python. That ran once, so we hold it as possible, not firm.

**What it means.** A 4B model and a 27B model from different makers tell the same stories about these languages. We think this is the real trace of broad sentiment in the training text. The emotion state itself adds little on top of the text.
