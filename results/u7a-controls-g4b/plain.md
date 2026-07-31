**The short version.** Gemma 4B's early layers showed the same top words across unrelated prompts, but far less than Qwen 27B in an earlier test.

**What we did.** We gave Gemma 4B several unrelated prompts, such as a fact about a country's currency. We measured how much the top-ranked words in the lens overlapped, layer by layer.

**What we found.** The top words overlapped by 18.5 percent at the first layer. This dropped to about 7.5 percent by the middle layers. In an earlier test, Qwen 27B shared 31 percent at its first layer. Gemma 4B's shared words were web-page tags, such as `</strong>` and `</h1>`.

**What it means.** Both models show a fixed, repeated pattern in their early layers. The pattern is smaller in Gemma 4B and made of different words. The tokenizer settled that difference: Qwen 27B's adult-content words are not single tokens in Gemma's vocabulary.

**What this does not show.** Later work found what this pattern is. The lens reads a fixed part of the model's early internal state that does not change with the input. The pattern is real inside the model, and it carries no information about our text.
