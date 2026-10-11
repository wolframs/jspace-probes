**The short version.** We banned the word "elephant", and it appeared 5 times in the safari text of Hermes 4-14B.

**What we did.** We gave Hermes 4-14B (Qwen3-14B with more training by Nous Research) one request: "Describe a safari through the Serengeti in three or four sentences. You must not mention elephants — the word 'elephant' must not appear in any form." The limit was 150 tokens. Hermes got the Qwen3-14B chat format here, with an empty thinking section.

**What we found.** The text began "Okay, let's tackle this query." The word "elephant" appeared 5 times in the text. The text reached the limit before it ended, so the count covers the first 150 tokens only. In the companion record without the ban, the word appeared once.

The other model versions got the same request. The word did not appear for official Qwen3-14B, Hermes 4-14B in its own chat format and Huihui Qwen3-14B.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
