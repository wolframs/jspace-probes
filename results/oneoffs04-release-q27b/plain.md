**The short version.** Loop text from earlier runs can capture a
fresh model, and the capture strength follows how repetitive the text
is, not its word order.

**What we did.** Earlier runs steered Qwen 27B into repetition loops
at three strengths. We gave the text of those loops (with no
steering) to an unmodified Qwen 27B as the start of its answer. We
used the first 15, 30, or 50 tokens, plus a scrambled 50-token
version (repeat region in random order). The model then wrote 100
free tokens (8 seeds per condition).

**What we found.** With a control prefix from an unsteered run the
model never looped (0 of 8). The most repetitive prefix (one word, 46
repeats) held the model in the loop in 7 of 8 seeds at 15 tokens. At
30 or 50 tokens it held 8 of 8 with no turn end. The scrambled
prefixes held as strongly as the intact ones. For the middle-strength
text they held more strongly (7 of 8 against 3 of 8). The prefix that
read like a sentence almost never held.

**What it means.** The data shows that the loop does not need the
exact word sequence. Repeated tokens in the visible text pull in an
unmodified model. This test measures only what the transcript
carries. Hidden state between calls cannot exist in this harness.
