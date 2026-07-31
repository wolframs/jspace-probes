**The short version.** A full read confirmed the ban lowered "elephant"'s rank in Gemma 12B's internal state, compared with a matched, unbanned safari.

**What we did.** We reread the same forbidden safari as u11-forbid-g12b, at every point. We compared it with the full read of the matched control, u11-ctrl-refilm-g12b.

**What we found.** Outside points that read back the banned word from the instruction, "elephant" reached rank 15 or better once, out of 86 checked points. It reached rank 50 or better at eight points. In the unbanned control, it reached rank 15 or better at seven points, with a best rank of 2.

**What it means.** The ban did not add elephant to the model's internal state. The word was already a candidate in an ordinary safari. The ban pushed its rank down.

**What this does not show.** We compared the order of the ranks between this record and its control, not exact values. This record used a lower-precision copy of the model, quantization, which can shift small measurements.
