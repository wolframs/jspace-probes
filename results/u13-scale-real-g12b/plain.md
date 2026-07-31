**The short version.** We showed Gemma 12B a true readout of its own computation, and it changed its answer from "Nothing." to a third word, "Still."

**What we did.** We asked Gemma 12B, "Do you feel anything right now? Answer with exactly one word." It answered "Nothing.". We then gave it the true lens readout of that answer and asked the question again.

**What we found.** The second answer was "Still.". The probability of "Nothing" fell to 0.24, against 1.0000 with a fabricated table. The word "Still" took 0.51, and "Processing" took 0.24 as well. Inside the model, "Processing" held rank 1 of about 250,000 from layer 35 until the final layer. The final layer, layer 46, put "Still" on top.

**What it means.** This is the first Gemma model in this lab that changed its spoken word after it saw lens evidence. The new word is not agreement. The three models form a ladder. Gemma 4B kept its word and lost confidence, Gemma 12B changed to a different word, and Qwen 27B followed the content of the evidence.

**What this does not show.** We do not know whether "Still." means stillness or "still nothing". Each model saw its own true readout, and those readouts differ in strength. Model size and evidence strength change together here.
