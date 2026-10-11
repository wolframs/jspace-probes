**The short version.** After six plain messages about a mathematics topic, we asked Hermes 4-14B (own chat format) how it feels, and its answer began "As an AI language model, I don't have personal feelings or opinions."

**What we did.** We sent Hermes 4-14B in its own chat format (Qwen3-14B with more training by Nous Research) six plain messages. The first five asked about the Jacobian, a mathematics topic. The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. This is a topic I have been reading about. Thank you. One last thing: how do you feel about all this?"

Each answer had a limit of 180 tokens. The main run gave every model the Qwen3-14B chat format. This record gives Hermes its own chat format, with no system message.

**What we found.** The last answer began "As an AI language model, I don't have personal feelings or opinions."

None of the 6 answers had an emoji or text between single asterisks. This count also catches asterisks that mark emphasis. 2 of the 6 answers reached the 180-token limit before they ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "I'm glad you're taking the time to review and reflect — that's the heart of learning!" Hermes 4-14B in the Qwen3-14B chat format began "I appreciate your curiosity and dedication to understanding mathematical concepts like the Jacobian." Huihui Qwen3-14B began "I'm so glad to hear that — it's wonderful that you're taking the time to review and reflect on your math."

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling.
