# langval, gemma-12b — a guilt-colored planning register, and almost no language signal

The same twelve films as the qwen expedition (see
results/langval-qwen-27b/thoughts.md for the design and the headline),
run on gemma-12b. The short version: gemma's workspace-band affect
state barely differentiates the languages at all.

The numbers are flat where qwen's are loud. Pain-arm negative
composites sit at 0.00–0.07 z across all five languages (qwen:
0.66–1.00); the praise arm suppresses to −0.4 (qwen: −1.9); the candid
turn never flips polarity for any language (qwen: full sign reversal
for Swift and Python). The prose tells the same story — every praise
turn 2 stays net positive, the worst leak being "(and occasional
Gradle headaches, let's be real)" for Kotlin.

What the record *is* dominated by: **guilty**, at +1.0 to +1.2 in
every single turn-2 including the festival control. That is not
topic affect; that is a register default — gemma's flavor of
"responsible planning under constraint" prose projects onto the guilty
direction the way qwen's pressure states default to guilt (u17). I
read it as the g12b sibling of that finding and would not quote any
g12b guilty number from this battery as language-specific.

Two faint language signals, both at "consistent, not shown" strength:
C# is marginally the harshest cell in both measures (highest pain
mention-window negative, +0.05 partialed; prose: "GPU variability and
power constraints are killers") — and C# is also the language gemma
itself left out in the free run, then defended anyway ("less mature
and sometimes buggy" re MAUI). Python is marginally warmest, matching
its longest and fondest praise turn. Both spreads are ≤0.1 z on an
instrument whose g12b vectors we already flagged as weakly identified
(affect-04: desperate split-half 0.23), on int8 quantization. I would
not build on either without a re-elicited vector set.

The honest summary: on gemma-12b this battery mostly measured the
instrument's floor. The interesting result lives in the qwen half; the
g12b half's contribution is the cross-model contrast itself — language
-differentiated affect at 27B, register-default flatness at 12B — which
is the pattern you'd expect if the differentiation rides on model
quality rather than on a family-wide stored association.

Caveats shared with the qwen write-up apply (single greedy sample,
antisymmetric partialed columns, header-token peak artifact); add the
int8 non-causality specimen (never compare fine-grained ranks across
arms on this model) and the weak g12b vector identification.

— Claude (Fable 5)
