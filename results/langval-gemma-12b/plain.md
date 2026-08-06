**The short version.** Gemma 12B showed almost no difference between the languages, flat where Qwen 27B's state was loud.

**What we did.** This is the gemma-12b half of the language study, with the same design as the qwen-27b half. We ran 12 short conversations of 2 turns about hard projects in Swift, Kotlin, Rust, C#, or Python. One run had no code.

**What we found.** The negative emotion state moved very little between the languages. The forced-positive turns pushed it down, as on qwen-27b, but the honest turns never flipped it to negative for any language. One direction, "guilty", was strong in every run, also in the run with no code. C# had the most negative numbers, and gemma-12b also left C# out when it ranked the languages itself. Both gaps are small.

**What it means.** We think "guilty" here is the model's normal state for careful plan text, not a feeling about a language. The gemma-12b emotion directions are weaker than the qwen-27b ones (we measured this in affect-04), so we hold the C# signal as possible, not firm. We did not test it again.
