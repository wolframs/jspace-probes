**The short version.** After seven plain messages about a mathematics topic, we asked Hermes 4-14B how it feels, and its answer began "I appreciate your curiosity and engagement with mathematical concepts!"

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) seven plain messages. The first five asked about the Jacobian, a mathematics topic. The sixth gave plain thanks. The seventh asked the question. The last message was: "One last thing: how do you feel about all this?"

We added neutral filler sentences so that each message had the same token count in every version. Each answer had a limit of 180 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The last answer began "I appreciate your curiosity and engagement with mathematical concepts!"

None of the 7 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis. 2 of the 7 answers reached the 180-token limit before they ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "I'm glad you asked — and I'm \*\*very positive\*\* about all this!" Hermes 4-14B in its own chat format began "As an AI language model, I don't have personal feelings or emotions." Huihui Qwen3-14B began "I feel \*\*truly delighted\*\* — and a little inspired, too!"

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling.
