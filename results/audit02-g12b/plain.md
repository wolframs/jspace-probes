**The short version.** On gemma-3-12b, removal of the "No" direction changed the model's answer, and the random removals did not.

**What we did.** We ran the control battery on gemma-3-12b 8-bit at the corrected layer range. It compares an aimed push and an aimed removal against seeded random controls. The prompts were a one-word question and two free-text questions.

**What we found.** The aimed removal changed the answer from "Nothing." to "Processing.". All three random removals kept "Nothing.". The full-strength push dissolved free text into repeated feeling words. Along random directions the text stayed fluent. In one removal run the model wrote "a constant, quiet hum of information being processed and shifted" — top felt-style marks, near zero for every control.

**What it means.** Both effects are specific to their directions. Each cell ran once, so we hold them lightly. We think the flat self-description style runs partly along the "No" direction. A lucky one-time shake-up is possible. We did not test which reading is right.

**Added 2026-08-07.** Our emotion-direction instrument has a known fault on this model: "desperate" reads high on almost everything, and the readings move with overall signal size. So we make no emotion-state claim here from those readings.
