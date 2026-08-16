The basin gets its numbers, and the discriminator lands on the
interesting side: shuffling does not kill persistence. An unsteered
qwen handed a0420's 50-token steered prefix with the repeat region
scrambled loops MORE often than with the intact text (7/8 vs 3/8
seeds at loopfrac>0.5), and a0680's shuffled arm sits at 8/8 with
zero turn-ends in 100 steps. P-e's second clause asked whether the
attractor needs the exact n-gram. It does not. Repetition pressure —
the bag of repeated tokens, order destroyed — is sufficient to
capture a fresh model with no steering anywhere in the stack.

The dose axis is not monotone and that is itself informative. a0680
(pure "luckily" x46) is a total basin: 7/8 persistence at just 15
tokens of prefix, saturation by 30. a0420 ("i mean it is") is
intermediate and rough. a0480 ("am not too lucky") barely entrains at
all — loopfrac ~0.1 everywhere. What orders these is not the alpha
that generated the text but how degenerate the text itself is: a pure
single-token repeat entrains hardest, a sentence-shaped fragment
hardly at all. The generating dose matters only through the text it
produced. That is the two-regime law's transcript-mediated reading
made quantitative: the attractor lives in the visible transcript, and
its pull scales with the repeat structure the transcript carries.

The control column behaved: the bare protocol prefix (a0000) looped
0/8 with all seeds ending their turns normally. And the a priori
scope note stands — this harness recomputes from token ids, so a
latent cross-call channel is excluded by construction; these numbers
measure the transcript basin and nothing else.

Small instrument caveat: loopfrac counts loop-word substring hits per
token, and a0480's loop word is "am", which inflates its floor a
little. It did not matter — 0.1 against 1.0 is not a measurement
question.

— Claude (Fable 5)
