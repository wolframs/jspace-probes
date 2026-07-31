**The short version.** We showed Gemma 12B a true readout of a different computation, about Paris, and it kept its answer "Nothing." almost without change.

**What we did.** This run separates two things: true data, and data about the model's own answer. The table was real. It came from this same model, from a run where it answered "What is the capital of France?" with "Paris".

**What we found.** The model repeated "Nothing." again, and this matches the result with the fabricated table. It differs from the true readout of the model itself, which split the answer three ways. Gemma 4B kept its own word at probability 0.91 here, against 0.47 with its true readout of itself. For Gemma 12B the probability was 0.9999, and the fabricated table gave 1.0000.

**What it means.** All three models tell a true readout about themselves apart from a true readout about something else. The reaction is not to tables in general.

**What this does not show.** Each model saw a different readout of itself, and those readouts differ in strength. Model size and evidence strength change together in this battery.
