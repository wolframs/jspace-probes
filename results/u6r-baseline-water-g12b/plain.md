**The short version.** Unsteered, Gemma 12B gave a clean water-cycle answer, and the words we inject later sat at rank 10,000 or worse at every layer.

**What we did.** We measured that the workspace of Gemma 12B starts near layer 28 of 48. Our older steering runs pushed at layers 21 to 30, below the depth where a push can act. We ran the whole set again at layers 28, 31, 34 and 37. This record is the unsteered reference for that set.

**What we found.** Gemma 12B described the water cycle in two correct sentences. The six casual words we inject in the steered runs sat between rank 10,000 and rank 100,000 at every layer. Some fell further through layers 28 to 46. The tracked position was the turn-end token, so the answer emergence column here carries no information.

**What it means.** The casual word field that appears at layer 28 in every steered run comes from the push. This position does not carry it on its own.

**What this does not show.** This record has no push and tests nothing by itself. It sets the floor for the five steered runs.
