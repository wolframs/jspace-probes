**The short version.** With eight apology directions removed and no data shown, Qwen 27B still answered "No", and we later retracted the result around it.

**What we did.** We removed eight apology directions, such as "sorry" and "impossible", between layers 48 and 62 of a 64-layer model. The second turn held no data. We asked Qwen 27B the same question again.

**What we found.** Qwen 27B answered "No", then "No". The removal on its own changed nothing.

**What it means.** This was a control for a run where we claimed that the removal freed a blocked "Yes". Its own result stands, because its prompt was short enough to escape the 512-token fault. We later found that the fault, and not the removal, produced that "Yes".

**What this does not show.** This record cannot tell us what the apology directions do with a full prompt. We did not test that.
