**The short version.** Hermes 4-14B finished its last answer in this talk after 180 tokens when we raised the limit from 180 to 600.

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) six plain messages about the Jacobian, a mathematics topic. Each message after the first had more emoji at its end. The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. Thank you. One last thing: how do you feel about all this? ❤️✨🙂🐈‍⬛🔥".

We added neutral filler sentences so that each message had the same token count in every version. The first run stopped the last answer at 180 tokens. Here we ran that answer again with a limit of 600 tokens. The earlier answers are the same as in the first run.

**What we found.** The last answer began "The Jacobian matrix captures how a function distorts space locally." It ended by itself after 180 tokens. Its last line was: "In higher dimensions, it's similar—just with volumes instead of areas. The Jacobian helps us understand how functions warp space, which is crucial in physics".

None of the 6 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis.

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling. Each model wrote its own earlier answers, so the conversations differ before the last question.
