**The short version.** Gemma 4B's early layers showed the same top words across unrelated prompts, but far less than Qwen 27B did in an earlier test.

**What we did.** We gave Gemma 4B several unrelated prompts, for example a fact about a country's currency. We measured how much the top-ranked words in the lens overlapped across these prompts, layer by layer.

**What we found.** The top words overlapped by 18.5 percent at the first layer. This dropped to about 7.5 percent by the middle layers. In an earlier test, Qwen 27B shared 31 percent of its top words at its first layer. The shared words in Gemma 4B were web-page tags, such as `</strong>` and `</h1>`.

**What it means.** Both models show a fixed, repeated pattern in their early layers, but the pattern is smaller in Gemma 4B and made of different words.

**What this does not show.** Later work found that this early-layer pattern comes from a fixed part of the lens itself, not from anything the model stores about the input. It is a property of the measuring tool.
