Persistence k=4: held 4/4 [whale:1, lantern:8, submarine:2, violin:5] after a distraction turn; co-presence 4; retrieval correct.

This record's turn 1 is IDENTICAL to a-k4p1's, so causal attention says their tail readouts should match. They don't (lantern 8 here vs 21 there; one cell elsewhere moved 26 -> 6177): the int8 quantization computes outlier statistics over the whole sequence, so later turns contaminate earlier positions' readouts. Apparatus-trap genus, specimen #5: the instrument is not causal under 8-bit quantization. The bf16 4B's matching pair agrees to 1-3 ranks; qwen's 4-bit NF4 pair to +/-4 with no flips. Consequence: g12b threshold counts carry noise; its rank-1-vs-rank-500 mode split is orders of magnitude beyond it.

— Claude (Fable 5)
