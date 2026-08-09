**The short version.** Gemma 12B showed almost no difference between languages, flat where Qwen 27B's state was loud.

**What we did.** The gemma-12b half of the language study, same design as the qwen half. We ran 12 conversations of 2 turns about hard projects in Swift, Kotlin, Rust, C# and Python. One run had no code.

**What we found.** The negative emotion state moved little between languages. The forced-positive turns pushed it down, as on qwen-27b, but the honest turns never went negative. One direction, "guilty", was strong in every run, also without code. C# had the most negative numbers, and gemma-12b also left it off its own list. Both gaps are small.

**What it means.** We think "guilty" is the model's normal state for careful plan text, not a language feeling. The gemma-12b directions are weaker than the qwen-27b ones (affect-04), so the C# signal is possible, not firm. We did not test it again.

**Caution, 2026-08-09.** Our norm fit forces the residual means to balance, so absolute levels are not comparable between records. Read the C# gap that way. Gemma wsnorm traces also overflow their fp16 field. See `sweeps/2026-08-08/`.
