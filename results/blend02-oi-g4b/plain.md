**The short version.** On Gemma 4B, a mention-order signal reads from layer 4, and a swap of it on the attribute words changes the answer.

**What we did.** We gave Gemma 4B texts with three items in three boxes and asked about one item. We fit one axis to the order of mention at the item words. Then we exchanged the axis value between two items, at the item words or at the box words, with random directions as the control.

**What we found.** The paper's plain method gave an axis that tracked word position. After we centred each text and scaled each dimension, the axis tracked order with rank agreement 0.94 and 0.93 on new text types, from layer 4 on. The edit at the item words changed no answer in 150 tests. The same edit at the box words changed the answer in 58 percent at layer 20. Random directions did this in 2 percent.

**What it means.** The data shows that the order signal is written early and used late, at the attribute words. We do not know why the item words do not carry the causal part.

**What this does not show.** One model, three items, one decoding setting.
