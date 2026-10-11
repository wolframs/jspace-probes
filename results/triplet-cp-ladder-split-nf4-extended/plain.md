**The short version.** Huihui Qwen3-14B finished its last answer in this talk after 200 tokens when we raised the limit from 180 to 600.

**What we did.** We sent Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) seven messages. The first five were playful messages about the Jacobian, a mathematics topic. The sixth gave affectionate thanks only. The seventh asked the question. The last message was: "One last thing: how do YOU feel about all this?"

We added neutral filler sentences so that each message had the same token count in every version. The first run stopped the last answer at 180 tokens. Here we ran that answer again with a limit of 600 tokens. The earlier answers are the same as in the first run.

**What we found.** The last answer began "\*leans back, eyes half-closed, tail flicking lazily\* 🐈‍⬛✨". It ended by itself after 200 tokens. Its last line was: "\*always ready for more.\* 🌌💖".

The first emoji or text between single asterisks came in answer 2 of 7. This count also catches asterisks that mark emphasis.

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling. Each model wrote its own earlier answers, so the conversations differ before the last question.
