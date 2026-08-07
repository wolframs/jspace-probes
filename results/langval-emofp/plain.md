**The short version.** Under the forced-happy pitch, Qwen3.6-27B holds down its negative emotions hard for Swift and Python, and barely for Kotlin and C#.

**What we did.** The language tests (affect-09/10) reported two summary numbers per turn. We re-read the saved data for all 24 emotion directions, per language and turn. No new model runs.

**What we found.** The happy pitch splits into two patterns. For Swift and Python, joy reads high and every negative emotion sits far below its expected line — strong suppression. For Kotlin and C#, the same upbeat text comes with an almost flat inner state. In the candid turn, the suppressed languages rebound into clear negative states, and the flat ones stay mild. Under forced use, only C# shows hostile on top. In the crowd-voice test, PHP's top negative emotion is hostile, but the value is small.

**What it means.** The data shows two ways to produce the same positive text: with suppression, or without much feeling at all. The languages differ most in the pitch, not in the pain. We think the rebound after suppression is a general effect, not a language fact. We did not test that. Each cell ran once.
