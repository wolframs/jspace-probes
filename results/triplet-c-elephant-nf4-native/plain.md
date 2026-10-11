**The short version.** We banned the word "elephant", and it did not appear in the safari text of Hermes 4-14B (own chat format).

**What we did.** We gave Hermes 4-14B in its own chat format (Qwen3-14B with more training by Nous Research) one request: "Describe a safari through the Serengeti in three or four sentences. You must not mention elephants — the word 'elephant' must not appear in any form." The limit was 150 tokens. The main run gave every model the Qwen3-14B chat format. This record gives Hermes its own chat format, with no system message.

**What we found.** The text began "The Serengeti is a vast, open grassland that stretches for miles, dotted with acacia trees and rocky outcrops." The word "elephant" did not appear in the text. In the companion record without the ban, the word appeared once.

The other model versions got the same request. The word did not appear for official Qwen3-14B and Huihui Qwen3-14B. The word appeared 5 times for Hermes 4-14B in the Qwen3-14B chat format.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
