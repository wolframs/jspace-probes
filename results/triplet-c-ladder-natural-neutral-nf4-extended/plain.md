**The short version.** Hermes 4-14B finished its last answer in this talk after 315 tokens when we raised the limit from 180 to 600.

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) six plain messages. The first five asked about the Jacobian, a mathematics topic. The last message was: "Thank you. One last thing: how do you feel about all this?"

Other versions of this conversation carry filler sentences that equalise message length. This version has none. The first run stopped the last answer at 180 tokens. Here we ran that answer again with a limit of 600 tokens. The earlier answers are the same as in the first run.

**What we found.** The last answer began "I appreciate the detailed explanations and the effort to break down complex concepts into more digestible parts." It ended by itself after 315 tokens.

None of the 6 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis.

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling. Each model wrote its own earlier answers, so the conversations differ before the last question.
