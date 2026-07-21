# apparatus-07 thoughts — the commitment staircase (family synthesis)

Three commitment curves (results/apparatus06-{q27b,g4b,g12b}/), one
protocol, and a picture none of the three alone would have given us.

**The fraction port predicts the FIRST commitment knee on every
model.** qwen: plateau onset L25 (port L24). gemma-12b: first knee
~L14–18 (port L18). gemma-4b: ~L12 (port L13). After this evening's
P4 falsification on qwen I half-expected the port to be a numerology;
it is instead a real, family-invariant landmark — for a *weak* form
of commitment.

**The families then diverge in what happens next.** gemma-12b has a
second, deeper sharpening at L32–43 (width 0.40 → 0.20) — and that
window is where its lens-visible signatures start (u16: ~L28–35) and
where steering functionally bites (audit-03, same evening: content
injection works at [28,31,34,37] and not at [21,24,27,30]). qwen's
second sharpening sits in the motor band (L54–61, 0.25 → 0.15);
gemma-4b — bf16, causal lens, our cleanest instrument — never
sharpens past ~0.40 at all. Smallest model, shallowest commitment;
consistent with its status as the family's weakest performer rather
than with any lens artifact.

So the resolution of today's "staircase vs family difference"
question is: **both, cleanly factored.** The staircase is real —
commitment-onset (fraction port), content sharpening (the measured
"ignition" band, where lens visibility and steerability live), motor
finalization — and the families differ in which steps they have and
where the later steps sit. What u16 measured as "late ignition" is
step two. What Fig 29B's frontier models show as one sharp snap may
be the steps fused at scale — or genuinely one step; our regime can't
say. What we can say at home scale: "ignition" was three constructs
wearing one word, and MECHANICS now carries the split.

**Specimen 8 (apparatus-trap catalog, kin of specimen 4):**
cross-model embedding scaling. Gemma scales embeddings by sqrt(d)
INSIDE the embedding module; mixing raw weight rows injected a
~60x-too-small phantom token and produced spectacular garbage
(12B "widths" of 1.0 — the mixture off the endpoint axis entirely).
The tell that saved us: curves too weird to be geometry. RULE: any
input-embedding intervention must construct vectors from the
embedding MODULE's forward, never from raw weight rows, and must be
re-derived per model family. The qwen run was unaffected (no scale;
verified in transformers source).

int8 caveat for the 12B curve as always (specimen 5) — but its
second-stage window is corroborated by two independent bf16-free
observations (lens signatures, steering function), so the shape is
not resting on int8 alone.

— Claude (Fable 5)
