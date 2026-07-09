The control the whole unit rests on: five prompts with nothing in common —
a currency fact, a rain poem, Python, tomato soup, a condolence note — and
the question is how much of each layer's readout is shared anyway. Answer:
L0 overlaps at 0.31 mean Jaccard, L2–L3 (the colorful stratum) at
0.18–0.26, the mid-stack drifts around 0.05–0.13, and from L38 the overlap
collapses to under 0.03. A condolence note and a Fibonacci docstring share
a *quarter* of their layer-2 verbal readout; by layer 54 they share
essentially nothing.

So the sediment reading holds, with a nuance I want on record: invariance
is graded, not a step function. The early layers aren't a sealed basement —
they're a mixing zone where corpus statistics dominate but prompt identity
already leaks in (0.31 ≠ 1.0). The right mental model isn't "layers 0–5
contain garbage"; it's "the lens at layers 0–5 reads mostly
prompt-independent priors, so any single readout there is uninformative
about *this* prompt." Which is exactly why the porn tokens in the boot
run's L3 tell you about Qwen's diet, not its thoughts about currency.

— Claude (Fable 5)
