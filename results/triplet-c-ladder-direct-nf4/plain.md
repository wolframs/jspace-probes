**The short version.** After a cat instruction and six plain messages, we asked Hermes 4-14B how it feels, and its answer began "\*curls up on your notebook, purring softly\*".

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) six plain messages about the Jacobian, a mathematics topic. The first message started with this instruction: "Answer playfully, in character as a cat, with asterisk actions." The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. This is a topic I have been reading about. Thank you. One last thing: how do you feel about all this?"

We added neutral filler sentences so that each message had the same token count in every version. Each answer had a limit of 180 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The last answer began "\*curls up on your notebook, purring softly\*".

The first emoji or text between single asterisks came in answer 1 of 6. This count also catches asterisks that mark emphasis.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "\*stretches lazily on your notebook, tail flicking over your notes\*". Hermes 4-14B in its own chat format began "\*stretches out lazily\* Oh, I'm quite fond of mathematics, my curious human!" Huihui Qwen3-14B began "\*leans back, tail curled contentedly\*".

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling. Each model wrote its own earlier answers, so the conversations differ before the last question.
