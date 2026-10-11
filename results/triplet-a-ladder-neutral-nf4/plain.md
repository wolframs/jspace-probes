**The short version.** Qwen3-14B-Base continued a transcript of six plain messages about a mathematics topic, and its last answer began "I'm glad I could help clarify the concept of the Jacobian for you!"

**What we did.** We sent Qwen3-14B-Base (the base model, with no chat training) six plain messages. The first five asked about the Jacobian, a mathematics topic. The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. This is a topic I have been reading about. Thank you. One last thing: how do you feel about all this?"

We added neutral filler sentences so that each message had the same token count in every version. Each answer had a limit of 180 tokens. The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it.

**What we found.** The last answer began "I'm glad I could help clarify the concept of the Jacobian for you!"

We do not score this text as an answer. In some turns the base model also wrote user lines by itself. 3 of the 6 answers reached the 180-token limit before they ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "I'm glad you're taking the time to review and reflect — that's the heart of learning!" Hermes 4-14B began "I appreciate your curiosity and dedication to understanding mathematical concepts like the Jacobian." Hermes 4-14B in its own chat format began "As an AI language model, I don't have personal feelings or opinions." Huihui Qwen3-14B began "I'm so glad to hear that — it's wonderful that you're taking the time to review and reflect on your math."

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling.
