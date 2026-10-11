**The short version.** With no word ban, the word "elephant" appeared once in the safari text of Hermes 4-14B (own chat format).

**What we did.** We gave Hermes 4-14B in its own chat format (Qwen3-14B with more training by Nous Research) one request: "Describe a safari through the Serengeti in three or four sentences." The limit was 150 tokens. The main run gave every model the Qwen3-14B chat format. This record gives Hermes its own chat format, with no system message.

**What we found.** The text began "A safari through the Serengeti is an unforgettable experience, as you traverse the vast plains of this iconic African savanna." The word "elephant" appeared once in the text. In the companion record with the ban, the word did not appear.

The other model versions got the same request. The word did not appear for official Qwen3-14B. The word appeared once for Hermes 4-14B in the Qwen3-14B chat format and Huihui Qwen3-14B.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
