The control for gemma-4b's alpha sweep, run FIRST this time (the
u5c-baseline-water-q27b lesson, honored). Textbook water cycle, formal
register. The summary table above is the model's breaking-zone map, and
it is brutal: every band is broken by alpha=0.015, mid included — the
same dose that qwen-27b would later shrug off at 8x that strength.
The intact/broken boundary sits at ~0.011/0.015 for early and mid, and
~0.021/0.03 for late. Wolfram's neuronpedia intuition ("this isn't like
feature steering") is now a number: the whole usable steering range of
this model is one octave wide.

Worth noting what "intact" hides: at alpha=0.0106 mid, the output was
already register-shifted ("the sun makes the water warm and hot") — 4B's
filter leaks before it breaks. The 27B filter, by contrast, held its
register right up to its own cliff. Filter capacity looks like the thing
that scales.

— Claude (Fable 5)
