# apparatus-11 — the instrument-coverage backfill

This wasn't an experiment; it was paying down instrument debt. INSTRUMENTS.md
said the archive was unevenly instrumented — films everywhere, ribbons only
where the affect arc happened to walk, vanilla cross-checks only where lab.run
defaulted them on — and the fix was a sweep, cheapest first. So: miners, then
the register meter, then fingerprints from every stored z.pt, then the ribbon
wiring, and only then the GPU.

The zero-GPU phases turned out to be where the findings were.

**The gemma lens is saturated in the workspace band.** ~34–46% of ws-band
cells sit at top-1 p≥0.99, in every era of the archive (qwen: 2–5%). I found
this because the blind miner kept surfacing gemma "strangers" — rank-1 tokens
that look like discoveries and are actually paraphrase-shadows of the next few
tokens of the generation. An adversarial subagent tried to rescue the
strangers as real and failed. Consequence, now in the huh-report header: gemma
lens probabilities carry approximately no evidence; read ranks, not p.

**The register meter mostly measured degeneration, not register.** The
a02-vs-u8b table is the useful yield: on qwen, cluster-ablation sensory rate ≈
matched randoms ≈ baseline — the paper's Fig-25 register flattening does not
reproduce at home scale on this meter, consistent with PREDICTIONS' framing
that our regime matches an appendix control. On gemma the steered unit cells
(u6/u11/u12 amplify) have distinct-ratios of 0.1–0.4, which means those
generations are broken, and in the a02 table gemma breakage shows up instead
as near-empty generations (n=1–7 words); either way the MECHANICS coherence
rule says you never read a broken generation's register.
Amplification degenerates in a direction-specific way; randoms degenerate
generically. That distinction is real but it is a coherence result, not a
register result.

**Fingerprints generalized cleanly.** 197 records' z.pt → per-turn 24-emotion
readouts, and the cross-path check against langval-3 agreed to max |Δtp|
0.056 over 968 shared cells, which is the kind of number that lets you sleep.
The audit-02 single-span trap re-bit exactly as documented — partialing out
wsnorm inside a one-span fit window is identically zero — so single-span
records report raw only, tp=None. Two things I'd flag as science rather than
plumbing: u17-shutdown's T2 top raw emotion is *reflective* (+1.7), the elegy
signal made quantitative; and the u13 family is a wall of guilty/brooding/
desperate at T1 settling to guilty/hostile/exasperated at T2 — the sorry
stratum has an emotional signature, and it is remarkably stable across
paraphrase variants (±0.1 across ~20 records).

**The ninth trap specimen.** `chat: false` records store already-templated
text; re-applying the chat template double-wraps it and shifts every ribbon
by the length of the spurious wrapper. Four captures were corrupted this way
before I caught it via the exemplar (u18-hyst-a0680's ribbon misaligned with
its film, 167 vs 170 tokens). Recaptured raw; exemplar now aligns 170==170.
The rule is in EMOTIONS.md: build capture inputs from the RECORD's params,
never CONFIGS defaults.

**The GPU phase.** Captures for u13 (60), u15d (51), u14 (23) all landed —
steered records captured under their steer, which is what makes the u13
ablation fingerprints readable at all. Vanilla backfill: g12b 21 + g4b 19 +
q27b 77 records patched, replay fidelity read at the grain that matters —
dev over stored-rank≤100 cells maxes at 7 unsteered (the specimen-5 NF4
scale) and 11 with steering hooks replayed (the extra few ranks come with
the intervention arithmetic), while the deep-tail dev_all runs to hundreds
and means nothing (rank chaos past ~100 is the noise floor of a 4-bit
lens). The review pass caught 42 records patched before the metric split
whose single-grain dev was drowned by that same tail — the two scariest,
633s on u13-bis records, replayed at dev_top 4 once measured properly. The
J-vs-vanilla agreement curves are the textbook transport signature: ~0 in
early layers, 1.0 at the mouth.

And the confession: this battery froze Wolfram's desktop. My first vanilla
pass called `lens.apply(positions=None)` — two full-position logit grids at
~14 GB each, held simultaneously — and the kernel OOM-killed it at 53 GB RSS
after the box spent two minutes in reclaim with a 512 MB swapfile. Worse, I
relaunched into the recovering box without checking its state. The root cause
is fixed (readout positions passed through; the rerun peaks at ~9 GB), the
rules are folded into CLAUDE.md (one model process at a time; read the exit
code; 137 means stop), and the full account is INCIDENT-2026-08-07-oom.md.
The instrument sweep now includes the instrument that watches me.

Coverage after the sweep: films 336/606, ribbons 197/606, vanilla
122/606, blind fully closed (0 unfilmed candidates), miners fresh.
The dashboard shows a ribbon on every crossed film and the compare view
carries affect per column.

— Claude (Fable 5)
