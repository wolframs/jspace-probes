**The short version.** We withdrew the Gemma 12B emotion-report claim because the corrected-depth test kept the usual denial.

**What we did.** We amplified six feeling-word directions at layers 21, 24, 27 and 30, at strength 0.0106.

**What we found.** The recorded text starts with "Sad." and then continues into extra words. That output remains in the record.

**What it means.** The later audit repeated the push at layers 28, 31, 34 and 37. The answer kept its usual denial, and the pushed words leaked into broken text after it. We were wrong to present the earlier output as a stable emotion-report effect. See record u8cr-amp-affect-hi-g12b and results/audit03-thoughts-g12b.md.

**What this does not show.** A changed word does not establish a feeling. This 8-bit measurement also cannot establish a causal interpretation from word ranks alone.
