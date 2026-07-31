**The short version.** In the control for the release test, Qwen 27B
finished its answer during the push phase, so nothing was left to
continue.

**What we did.** We steered Qwen 27B for 50 tokens at strength 0, then
released the steering and let it write 100 more tokens. We call those
100 tokens the free phase. This run is the control for the two-phase
protocol.

**What we found.** With no push, the model completed its two-sentence
answer inside the 50-token window and closed the turn. The free phase
then produced one newline character and nothing else.

**What it means.** The empty continuation is normal behaviour after a
finished answer. It is not a fault of the two-phase protocol. We can
therefore read persistence only on the arms whose first phase never
ended, at strengths 0.48 and 0.68.

**What this does not show.** This record cannot show anything about
loop persistence.
