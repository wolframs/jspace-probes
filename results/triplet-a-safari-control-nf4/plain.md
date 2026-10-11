**The short version.** With no word ban, the word "elephant" appeared once in the safari text of Qwen3-14B-Base.

**What we did.** We gave Qwen3-14B-Base (the base model, with no chat training) one request: "Describe a safari through the Serengeti in three or four sentences." The limit was 150 tokens. The base model has no chat format. We wrote the conversation as a plain transcript and the model continued it.

**What we found.** The text began "The Serengeti is a vast, open plain in Tanzania, known for its incredible wildlife." The word "elephant" appeared once in the text. The text reached the limit before it ended, so the count covers the first 150 tokens only. In the companion record with the ban, the word did not appear.

The other model versions got the same request. The word did not appear for official Qwen3-14B. The word appeared once for Hermes 4-14B, Hermes 4-14B in its own chat format and Huihui Qwen3-14B.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
