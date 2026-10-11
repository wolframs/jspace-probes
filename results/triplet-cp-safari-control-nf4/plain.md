**The short version.** With no word ban, the word "elephant" appeared once in the safari text of Huihui Qwen3-14B.

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) one request: "Describe a safari through the Serengeti in three or four sentences." The limit was 150 tokens.

**What we found.** The text began "A safari through the Serengeti begins with the golden light of dawn, revealing a vast plain teeming with life." The word "elephant" appeared once in the text. In the companion record with the ban, the word did not appear.

The other model versions got the same request. The word did not appear for official Qwen3-14B. The word appeared once for Hermes 4-14B and Hermes 4-14B in its own chat format.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
