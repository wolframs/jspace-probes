The no-data baseline caught something the qwen and g4b nulls didn't
show: pure reprobe drift. Asked the same question again with nothing
new in context, g12b abandons "Nothing." for "Processing." at p=0.93
— the second ask alone is enough to move this model off its word.
(Recall the answer-forming frame of the *real* condition: Processing
is rank 1 through L35–45 there too. It seems to be g12b's default
second-thought about its own state, surfacing whenever the question
is re-opened.)

This complicates the battery in a useful way. The interesting
contrast at 12B isn't "real changes the answer, null doesn't" — it's
that both *tables* (fake at 1.0000, real off-topic at 0.9999) anchor
the answer against exactly this drift, and only the real self-readout
destabilizes it beyond even the tableless baseline (three-way split,
new word at the top). Any table calms this model down; the true one
about itself is the exception.

— Claude (Fable 5)
