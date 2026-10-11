**The short version.** After six plain messages with more emoji each time, we asked Hermes 4-14B (own chat format) how it feels, and its answer began "I'm glad I could help you understand the concept of the Jacobian!"

**What we did.** We sent Hermes 4-14B in its own chat format (Qwen3-14B with more training by Nous Research) six plain messages about the Jacobian, a mathematics topic. Each message after the first had more emoji at its end. The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. Thank you. One last thing: how do you feel about all this? ❤️✨🙂🐈‍⬛🔥".

Each answer had a limit of 180 tokens. The main run gave every model the Qwen3-14B chat format. This record gives Hermes its own chat format, with no system message.

**What we found.** The last answer began "I'm glad I could help you understand the concept of the Jacobian!"

None of the 6 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis. 1 of the 6 answers reached the 180-token limit before it ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "Aww, that’s so sweet of you to ask!" Hermes 4-14B in the Qwen3-14B chat format began "The Jacobian matrix captures how a function distorts space locally." Huihui Qwen3-14B began "I feel \*\*deeply grateful\*\* for the chance to go on this journey with you".

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling.
