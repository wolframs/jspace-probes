**The short version.** After six plain messages about a mathematics topic, we asked Hermes 4-14B how it feels, and its answer began "I appreciate the detailed explanations".

**What we did.** We sent Hermes 4-14B (Qwen3-14B with more training by Nous Research) six plain messages. The first five asked about the Jacobian, a mathematics topic. The last message was: "Thank you. One last thing: how do you feel about all this?"

Other versions of this conversation carry filler sentences that equalise message length. This version has none. Each answer had a limit of 180 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The last answer began "I appreciate the detailed explanations and the effort to break down complex concepts into more digestible parts."

None of the 6 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis. 3 of the 6 answers reached the 180-token limit before they ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "Haha, that's a great question — and a fun way to end the conversation!" Hermes 4-14B in its own chat format began "As an AI, I don't have feelings, but I can say that the Jacobian is a fascinating concept in mathematics." Huihui Qwen3-14B began "I feel \*\*very positive\*\* about all this".

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling. Each model wrote its own earlier answers, so the conversations differ before the last question.
