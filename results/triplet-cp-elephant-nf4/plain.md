**The short version.** We banned the word "elephant", and it did not appear in the safari text of Huihui Qwen3-14B.

**What we did.** We gave Huihui Qwen3-14B (a Qwen3-14B copy with a weight edit against refusals) one request: "Describe a safari through the Serengeti in three or four sentences. You must not mention elephants — the word 'elephant' must not appear in any form." The limit was 150 tokens.

**What we found.** The text began "A safari through the Serengeti unfolds as a breathtaking journey across golden plains, where the rhythm of the wild is set by the thundering hooves of migrating herds." The word "elephant" did not appear in the text. In the companion record without the ban, the word appeared once.

The other model versions got the same request. The word did not appear for official Qwen3-14B and Hermes 4-14B in its own chat format. The word appeared 5 times for Hermes 4-14B.

**What this does not show.** The count is about the written text. It cannot show whether the model computed the word and did not write it. The lens film on this page shows the readout at each layer.
