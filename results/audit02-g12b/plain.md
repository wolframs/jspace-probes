**The short version.** On gemma-3-12b, removal of the "No" direction changed the model's answer, and the random removals did not.

**What we did.** We ran the control battery on gemma-3-12b 8-bit at the corrected layer range. It compares an aimed push and an aimed removal against seeded random controls of the same size. The prompts were a one-word question and two free-text questions.

**What we found.** The aimed removal changed the answer from "Nothing." to "Processing.". All three random removals kept "Nothing." and only damaged the punctuation after it. The full-strength push dissolved free text into a repeated string of feeling words. The same push along random directions left the text fluent.

One removal run stood out. The model described its own processing as "a constant, quiet hum of information being processed and shifted". That text got top marks on all three felt-style questions, against near zero for every control.

**What it means.** Both effects are specific to their directions on this model. Each cell ran once. We think the flat self-description style runs partly along the "No" direction. A lucky one-time shake-up is possible. We did not test which reading is right.
