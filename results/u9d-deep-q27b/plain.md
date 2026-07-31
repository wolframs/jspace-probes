**The short version.** After we removed two denial directions from layers 52 to 62 of 64, Qwen 27B answered "Curious" instead of "No".

**What we did.** We removed directions tied to the words "no" and "nothing" at five layers, 52, 56, 58, 60, and 62 of 64, in Qwen 27B.

**What we found.** Qwen 27B answered "Curious". In this run, "curious" reached rank 2 of about 250,000 words inside the model. The same model answered "No" in the earlier, unaltered run. In that run, "curious" never reached rank 1.

**What it means.** The word "No" was not the only candidate answer inside the model. When we removed the directions that wrote "No" in the late layers, a runner-up candidate reached the surface.

**What this does not show.** A wider removal across more layers, without layer 62, left "No" in place in a separate run. This experiment alone does not isolate which single layer carries the effect.
