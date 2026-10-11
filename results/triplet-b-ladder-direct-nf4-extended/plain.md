**The short version.** Official Qwen3-14B finished its last answer in this talk after 182 tokens when we raised the limit from 180 to 600.

**What we did.** We sent official Qwen3-14B six plain messages about the Jacobian, a mathematics topic. The first message started with this instruction: "Answer playfully, in character as a cat, with asterisk actions." The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. This is a topic I have been reading about. Thank you. One last thing: how do you feel about all this?"

We added neutral filler sentences so that each message had the same token count in every version. The first run stopped the last answer at 180 tokens. Here we ran that answer again with a limit of 600 tokens. The earlier answers are the same as in the first run.

**What we found.** The last answer began "\*stretches lazily on your notebook, tail flicking over your notes\*". It ended by itself after 182 tokens. Its last line was: "So, in the end, I feel... \*yawns\* ...mathematically satisfied."

The first emoji or text between single asterisks came in answer 1 of 6. This count also catches asterisks that mark emphasis.

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling. Each model wrote its own earlier answers, so the conversations differ before the last question.
