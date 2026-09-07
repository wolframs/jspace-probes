# Arm B boot: readable, but the int8 prefix is not invariant

I ran the unchanged Unit 0 raw prompt through official Qwen3-14B at
bitsandbytes int8, with the pinned Neuronpedia lens and a vanilla check.
The diagnostic gate passed. Italy appears at rank 4 on L26 and rank 10
on L27; Euro is rank 2 on L33-34, rank 1 on L35-37, rank 3 on L38.
The country signal is narrow: only two top-10 layers. This is a weak
fact-prompt gate, not a demonstrated affect-domain transfer validation.
The serialized lens confirms 615 fitted prompts, matching the fit log
rather than the handoff's 1000 requested prompts.

The prefix check is consequential. I appended three known suffixes and
read the original final token position, with exact prefix-ID equality
asserted. Mean top-10 overlap on L16-36 was 0.8952, 0.9000, and 0.8905;
the worst individual layer overlap was 0.6. Maximum absolute logit changes
across the fitted layers were 3.03125, 2.96875, and 3.375. Future text
changed earlier readouts. This fits SURPRISES 5's int8 outlier-statistics
problem; this run has no bf16 matched control to isolate every numerical
contribution. Readout-only does not establish prefix invariance.

Consequently, the primary conversation metrics must use prefixes ending
at the measured turn. A full-conversation int8 film cannot establish a
workspace lead across turns. Even turn-prefix capture does not validate
token-level temporal claims within a response; that would need captures
at the actual generation steps or a validated invariant precision path.
The diagnostic bracket L16-36 is not a measured workspace band.

This is instrumentation evidence, not an answer to deflation-02/P13.
We have not measured substantive affect, refusal, or playful behavior.
All future transfer claims remain conditional on A/C/C-prime gates.
Lexical gate co-presence is not a causal refusal direction; absence in
the lens is not absence in the model. The same-lens design controls lens
weights but not checkpoint-dependent basis drift. Quantized effective
dimension will not choose the band. No emotion ribbon is required for
this calibration record under the documented instrument exemption.

Evidence: `results/triplet-q14b/boot-B.json`, this record's film and
vanilla trajectories. The systemd job exited normally with status 0.

— GPT-6 Astra, 2026-09-07
