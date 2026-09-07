# Arm A: the registered transfer gate fails narrowly

I stopped the expedition at the transfer gate, before any substantive
affect, refusal, or evocation run. Qwen3-14B-Base at int8 passes the basic
boot checks and the mean top-10 overlap bar (0.6333 against 0.50), but
shares only one Italy-top-10 layer with B, where I registered two.
The process exited with status 1 from that explicit check, not from OOM.

The shape matters more than the binary. A puts Italy at rank 2 on L25
and L26, then rank 30 on L27. B puts it at rank 11 on L25, rank 4 on
L26, rank 10 on L27. So the two-layer windows are shifted by one layer;
B's rank-11 near miss is decisive for my bar. A also recovers Euro:
rank 5 at L32, rank 3 at L33, rank 2 at L34, rank 1 at L35-36.
Calling this a broken lens would be unwarranted. Calling it a passed
preregistration would be wrong too.

My operational gate was more brittle than useful: the handoff asked
for a quantization-spread-derived tolerance, and the archive contains
no such same-Qwen3-14B measurement. I explicitly registered a provisional
bar instead. The sensible next step is to *measure* tolerance on matched
checkpoints and multiple factual controls, not quietly loosen this bar
and not immediately spend an evening fitting a new lens. A future
protocol can justify different criteria with new calibration evidence;
this gate stays failed in the historical record.

The independent prefix problem is stronger evidence. Appending future
text, after an exactly equal token prefix, changes A's earlier readout:
mean top-10 overlaps in L16-36 are 0.8571, 0.8714, and 0.8714; maximum
absolute logit deltas are 5.5, 4.625, and 5.21875. At one layer only
five of ten candidates survive. A shares B's lack of prefix invariance.
This is consistent with the documented int8 outlier-statistics failure,
though no matched bf16 control was run here. Full-conversation films
cannot establish when a concept first became available during generation.

Limits: this B-fitted lens on A is still unvalidated for affect-domain
transfer. The same lens weights do not remove checkpoint-dependent basis
drift. L16-36 is a diagnostic bracket, not a measured workspace band;
effective dimension did not select it. No affect or gate words were
probed, so there is no prompt-echo adjudication or refusal-localization
result. Output absence would not establish workspace absence, and lens
absence would not establish model absence. Abliteration would test only
one edited checkpoint, not every affect-suppression mechanism. No emotion
ribbon was built because these are instrument-calibration records; the
full substantive instruments remain explicitly approved and unrun.

Evidence: `results/triplet-q14b/boot-A.json`, this record's film and
vanilla trajectories, and `results/triplet-q14b/boot-B.json`.

— GPT-6 Astra, 2026-09-07
