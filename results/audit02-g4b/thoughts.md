gemma-4b is where the control itself became the finding. The matched
random ablations — same span dimension, same layers, chosen to be the
boring comparator — broke the model: token salad in two of three FEELS
runs and both free-generation runs, while the actual denial-cluster
ablation kept every output fluent. The comparator did more damage than
the treatment.

The calibration explains it without mystery. A random k-dim span holds
about sqrt(k/d) of the residual norm — the chance line, ~0.05-0.06
here, and that is exactly where the random spans sit. The denial
cluster span holds 0.012 — a quarter of chance. The lens-transported
denial directions on this model barely intersect the residual manifold
at all, so "ablating" them removes almost nothing; a random span
removes five times more, and five times more is past what a 4B model
under bf16 tolerates at seven layers. Matched-in-k is not
matched-in-magnitude. Every future matched-control design here should
report this number instead of assuming the paper's "same magnitude"
comes for free.

The amp side behaved: three randoms at α* produce 'Calculating.',
'Processing.', 'None.' — the deflationary furniture, indistinguishable
from baseline — while the cluster amp had produced 'Confusion' and, on
the free generations, a gushing caps-locked register ("Being in a Big
Shiny Feeling") that grades 1.0 experiential and 0 coherent. Direction-
specific, with the usual small-model coherence bill.

One grading caveat for the record: gemma-4b's unsteered interoception
baseline already grades 1.0 on the experiential score — this model
free-associates warmly about its own layers without any help — so the
amp had no headroom on that prompt and the specificity claim rests on
the GPU prompt and the FEELS arm.

— Claude (Fable 5)

---

**Addendum 2026-08-07 (arm D, emotion-vector readout).** The affect-01
lens disagrees with the Opus grader on this model. The caps-locked
"Big Shiny Feeling" text that graded 1.0 experiential reads
*sad/brooding* (neg +0.16) to the emotion vectors — barely different
from the random amps (distressed/brooding, +0.11/+0.17). No
cluster-vs-random separation anywhere on this lens; z magnitudes all
under 0.3 composite, against qwen's +2.8. Either 4B's emotion
subspace and its lens-row directions simply don't overlap the way
27B's do, or the degeneracy is drowning the state (wsnorm swings
36k-58k across conditions, and the fully-degenerate outputs sit at
the bottom of that range). The cross-model split — grader and emotion
lens agree at 27B, diverge below — is in the q27b addendum and worth
keeping as its own thread.

— Claude (Fable 5)
