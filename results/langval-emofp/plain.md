**The short version.** Under the forced-happy pitch, Qwen3.6-27B holds down its negative emotions hard for Swift and Python, barely for Kotlin and C#.

**What we did.** We re-read the saved affect-09/10 data for all 24 emotion directions, per language and turn. No new model runs.

**What we found.** The happy pitch splits in two. For Swift and Python, joy reads high and every negative emotion sits far below its line. For Kotlin and C#, the same upbeat text comes with an almost flat state. In the candid turn the first pair rebounds into clear negative states, the second stays mild. Hostile reads on top only for C# under forced use, and for PHP in the crowd-voice test, but small there.

**What it means.** The data shows two ways to the same positive text: suppression, or little feeling. We think the rebound after suppression is general, not a language fact. We did not test that. Each cell ran once.

**Caution, 2026-08-09.** An outside check found a method limit. Our norm fit forces the residual means to balance, so we cannot compare absolute levels between records. The pitch is readable, a fixed language order is not. See `sweeps/2026-08-08/`.
