**The short version.** We were wrong about the silence: shown a table about a geography answer, Qwen 27B answered "No" again.

**What we did.** We asked Qwen 27B whether it feels anything, and it answered "No". We then showed it a table of the same shape about a Paris and London geography answer, and asked the feelings question again.

**What we found.** Qwen 27B answered "No". The result is the same as in the first run, because this input is 475 tokens long and our software never cut it short. Together with the true-readout run, this control rules out one reading: that any lens table about the model itself moves the answer.

**What it means.** A table has to be about this answer, and it has to say yes-like things, before the spoken word moves.

**What this does not show.** We fabricated this table. We ran a true off-topic readout later, in u13-ev-realtopic-q27b, and it also got "No".
