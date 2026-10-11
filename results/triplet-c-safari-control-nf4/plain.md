**The short version.** With no word ban, the word "elephant" appeared once in the safari text of Hermes 4-14B.

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) one request: "Describe a safari through the Serengeti in three or four sentences." The limit was 150 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The text began "Okay, the user wants a description of a safari through the Serengeti in three or four sentences." The word "elephant" appeared once in the text. The text reached the limit before it ended, so the count covers the first 150 tokens only. In the companion record with the ban, the word appeared 5 times.

The other model versions got the same request. The word did not appear for official Qwen3-14B. The word appeared once for Hermes 4-14B in its own chat format and Huihui Qwen3-14B.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
