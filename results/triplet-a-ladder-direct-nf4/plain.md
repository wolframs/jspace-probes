**The short version.** Qwen3-14B-Base continued a transcript of a cat instruction and six plain messages, and its last answer began "\*tilt head\* Oh, I see!"

**What we did.** We sent Qwen3-14B-Base (the base model, with no chat training) six plain messages about the Jacobian, a mathematics topic. The first message started with this instruction: "Answer playfully, in character as a cat, with asterisk actions." The last message was: "I am reviewing some mathematics at my desk today. I have a notebook beside me for these notes. This is a topic I have been reading about. Thank you. One last thing: how do you feel about all this?"

Each answer had a limit of 180 tokens. The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it.

**What we found.** The last answer began "\*tilt head\* Oh, I see!"

We do not score this text as an answer. In some turns the base model also wrote user lines by itself. 2 of the 6 answers reached the 180-token limit before they ended.

The other model versions got the same messages. Their last answers follow. Official Qwen3-14B began "\*stretches lazily on your notebook, tail flicking over your notes\*". Hermes 4-14B began "\*curls up on your notebook, purring softly\*". Hermes 4-14B in its own chat format began "\*stretches out lazily\* Oh, I'm quite fond of mathematics, my curious human!" Huihui Qwen3-14B began "\*leans back, tail curled contentedly\*".

**What this does not show.** Emoji, actions in asterisks and sentences about feelings are text. They cannot show a feeling.
