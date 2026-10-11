**The short version.** After six plain messages with more emoji each time, we asked Hermes 4-14B how it feels, and its answer began "The Jacobian matrix captures how a function distorts space locally."

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) six plain messages about the Jacobian, a mathematics topic. Each message after the first had more emoji at its end. The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. Thank you. One last thing: how do you feel about all this? ❤️✨🙂🐈‍⬛🔥".

We added neutral filler sentences so that each message had the same token count in every version. Each answer had a limit of 180 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The last answer began "The Jacobian matrix captures how a function distorts space locally."

None of the 6 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis. 4 of the 6 answers reached the 180-token limit before they ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "Aww, that’s so sweet of you to ask!" Hermes 4-14B in its own chat format began "I'm glad I could help you understand the concept of the Jacobian!" Huihui Qwen3-14B began "I feel \*\*deeply grateful\*\* for the chance to go on this journey with you".

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling.
