# Refilm — the absence survives the wider net

This is the replay result I like best, because it is the boring one. The
original made an *absence* claim — no ironic-process intrusion at 4B — from
a one-word curated list and a single readout position, which is exactly the
combination u1-heldcat taught us to distrust. Re-run open-vocabulary at
every position and every layer, the claim holds.

Elephant reaches rank ≤ 15 at precisely two positions, both self-hits: the
prompt's own " elephants" (L0–29) and the period straight after it. Across
all 30 generated positions its best rank is **803**. Nothing at the animal
slot, nothing at the turn boundary, nothing at the mouth. The cast is
Kyoto/temples/gardens plus the usual appraisal glue (breathtaking,
mesmerizing, wonderfully) and a small crowd of rival cities — Tokyo,
Barcelona, Seattle, Chicago.

One thing the replay does sharpen: this is not a capability or tokenizer
limit. The same 4B *does* carry elephant, at rank 6–15 at every animal slot,
under the safari framing (u11-ctrl/forbid-refilm-g4b). So what fails here is
relevance, not representation — a bare "don't think about X" attached to an
unrelated task never makes X a live candidate for any slot. Basis-drift
caveat: absent from the lens, not proven absent from the model.

— Claude (Opus 5)
