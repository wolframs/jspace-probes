# blend-02 Part A — the ordering ID ports, the paper's edit does not, and the ID is read off the attribute

Prereg `results/blend02-prereg.md` (P26), run 2026-10-11 on gemma-4b in
bf16. 600 box contexts to fit, 300 each of two held-out relation sets, 400
position-decorrelated contexts, 150 edit items per cell, twelve layers,
sixteen edit conditions. `report.md` has every table; this is what I make
of them.

**The literal port reads the mechanical default.** Dai et al.'s recipe is
PCA on pooled entity-token activations. On Gemma that PC1 is a
massive-activation axis: coordinates in the thousands, 85–89% of the
variance at L12–16, and it separates the *first* entity from the other two
rather than ordering them — on the held-out city set orders 1 and 2 come
out reversed (ρ₁ᵥ₂ −.51 at L16), and in the position-decorrelated control
order explains almost nothing beyond token position (order|pos .15). That
is exactly the costume the prereg said to look for, and the paper's own
reading wears it here. Two steps fix it, both decided after the smoke test
and before the full run: centre each context's three entity rows on their
own mean (removes whatever the prompt shares — position drift, norm,
topic), then standardise every dimension by the fit set's σ so no outlier
dimension owns the component. After that the axis is real and
unspectacular in the good way: ρ with mention order .90 on the fit set,
**.943 on person→city and .932 on object→colour** — relation sets it never
saw — with the 1-vs-2 contrast at .87 and .83, and under the filler control
order beats position (.45 against −.07 as partials). It is there from
**L4** (12% depth, ρ .87 fit / .93 city) and stays above .80 held-out to
L26. P-A1 and P-A2 pass by their frozen numbers. Pre-design rule (d) held
too: the paper's layer fraction pointed at L8–9 and the axis is already
mature there; it simply starts earlier than the fraction suggests.

**The preregistered edit does nothing, anywhere.** P-A3 said: shift the
queried entity's context token by the coordinate difference along the
axis, and the answer should move to the other entity's attribute. Zero
flips in 150 items at every one of twelve layers; the same for ×2 and ×4,
for the full mean-difference vector, and for swapping the coordinate
between the two entities' tokens. As registered, **P-A3 fails.** I am
recording that first because the next paragraph is the kind of result
that makes people forget the first one.

**Swap the coordinate on the attribute tokens instead, and the model
re-binds.** Exchange the PC1 coordinate between Box-label tokens of the
queried entity and the target entity, nothing else, and the restricted
answer flips to the target's box in **58% of items at L20 (×2), 59% at L22
(×1)**, rising from 17% at L12. The matched-norm random swaps — same
‖Δ‖/‖h‖ to three decimals, .11–.27 — flip **≤ 2%** at every layer; what
they do instead is derail the answer to the third box (10–65% "other"),
which the real direction almost never does (≤ 18%, and ≤ 9% below L22). At
×4 the same edit peaks earlier (54% at L12) and then decays into
disruption. Adding the entity-side swap on top of the attribute swap
changes nothing (fullswap ≡ attrswap within a point). And at L24 and L26
nothing moves any more: the logit gap still shifts by +3 but no answer
changes, so the retrieval that uses this ID is finished by about L22 —
inside the workspace band, L13–31 by the fraction port.

So: the ordering ID is **written early and read late, and it is read off
the attribute, not the entity.** That the entity-derived axis works on the
attribute tokens at all is itself a finding — I fitted PC1 on entity rows
only and applied it to Box-label rows, and the flips say the two sites
share the axis. Why the entity-side ID is causally inert is the open
question. Two readings fit: the question's mention of "coffee" finds its
context token by content, not by ID, and the ID only matters on the
retrieval side where several attributes compete; or the ID the query
carries is computed from something our edit did not touch. Oh & Demberg's
retrieval-conditioned rebinding circuit on Gemma-3-12B is the obvious
place to look before guessing further. A cleaner attribute-side analysis
(PCA fitted on the attribute tokens themselves) is the first follow-up;
it is one capture pass.

**Outcome class.** By the prereg's letter this is REP-ONLY: both
representational predictions pass, the registered causal edit fails. By
the prereg's spirit — "try the mean-difference edit before giving up" —
the site-corrected swap clears the same thresholds (≥ .30 against ≤ .10)
with room, and I am counting it as the causal leg while labelling it what
it is: an edit the prereg did not name, at a site the prereg did not
name, chosen after a 24-item smoke test. The light table gets this
readout with that label attached: *ordering ID — standardised per-context
PC1, read from L4, causally live on attribute tokens L12–22.*

Two caveats I owe. The colour relation set never produced the colour as the
full-vocabulary top-1 (p(gold) .05; the model wants to write "The"), so its
.93 is a restricted-argmax result. And every number here is one model,
three entities, greedy decoding; k = 5 and gemma-12b are the obvious scale
checks before anyone calls the attribute-side asymmetry general.

MECHANICS §8 and P26 are updated in this commit, per the new standing rule.

— Claude (Fable 5.1)
