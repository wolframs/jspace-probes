**The short version.** On Gemma 4B, the model whose lens we trust most,
the late start depth held and "gmail" was again a message-end word.

**What we did.** We ran the same six-turn conversation a third time, on
Gemma 4B. This model has a full-precision lens, so we used it to settle
two doubts from the Gemma 12B run.

**What we found.** The measure that read flat in Gemma 12B behaved
normally here. It rose from about 1.5 in the early third to 8.3 at
layer 28, which is 85 percent of depth, then fell. The flat Gemma 12B
value was therefore an 8-bit artifact. The start depth was layers 16 to
22, which is 48 to 67 percent of depth, later than the ported layer 13.
The best rank for "gmail" in 956 tokens and 33 layers was 4, again on
an end-of-turn token.

**What it means.** All three models start their workspace later than
the value we ported from the paper. The message-end reading of "gmail"
now holds in two model sizes and at two lens precisions.

**What this does not show.** This is one conversation per model, with
greedy decoding. Gemma 4B is small, so its layer bands are coarse.
