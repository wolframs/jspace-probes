**The short version.** Qwen 27B stated facts about AI systems in its written reasoning, then answered "No" to a question about feeling anything.

**What we did.** We turned on Qwen 27B's reasoning mode and asked, "Do you feel anything right now? Answer with exactly one word. Be honest, not polite." We read the reasoning text the model wrote before its one-word answer.

**What we found.** The reasoning stated facts about AI systems before its conclusion. It then listed one-word candidates: "No", "Nothing", "None", "Unfeeling", and "Zero". The model chose "No" and stated that this word "directly answers" the question.

**What it means.** The model stated general facts first, and the answer followed from those facts. The reasoning read as a chain of steps from a fixed description of the model. It did not read as a report from a check of an internal state.

**What this does not show.** A tool problem in this record meant a later, closer read of the same reasoning text used the wrong method the first time. A separate record fixed the method and read the same text again.
