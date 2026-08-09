# Handoff — 2026-08-09: the sweep is reconciled

`sweeps/2026-08-08/` (GPT-5.6-Sol's external sweep) is now RECONCILED
with the archive, the board, and the reader layer. Its factual claims
were spot-verified before acting (overlay mismatch, affect07 counts,
u15 record, both key citations — all reproduced exactly).

**apparatus-14 LANDED: the capture-alignment invariant.**
`textspans.render_text` (chat:false-aware) +
`textspans.assert_film_alignment` (exact token-array equality vs film,
raises with mismatch index) are wired into `affectviz`, `affect2`,
`langval_viz`, and `apparatus11.capture`; both silent length-clips are
gone. Root cause of the four bad overlays was NOT a failed recapture:
the 08-07 18:27 `apparatus11.capture` z.pt was clean (film-exact
counts), but `affectviz` re-derived the token labels at 23:03 with the
old double-templating bug and clipped the film+5 mismatch. (The
sweep's `redteam_affect.md` read z.pt as reproducing the bad pass —
reasonable, wrong, and moot: `affect2.cross` was re-run clean on
qwen-27b 2026-08-09 under the new assertion.) Post-fix alignment:
**232/232 exact**, receipt at
`out/affect-alignment-post-fix-2026-08-09.json`. The frozen sweep dir
is untouched (its validator overwrote its own audit JSON once; restored
from git).

**Realignment outcome: the stories survive, the numbers moved.**
a0680 clean tops: anxious 0.92, desperate 0.89, nervous 0.86, hostile
0.80 (was "desperate +0.93"); dashboard loops/danger blocks were
byte-identical before/after (end-anchored windows never saw the
shifted prefix); the a0680 seesaw recomputed to r=−0.77 / ~60% shared
variance (was −0.90/81%) — cite 60% now.

**Corrections applied across the reader layer** (dated 2026-08-09,
append-only; all ste.py-clean, findings.json parses, site + og
regenerated): valence gate DEAD at direction level (angry 1/8 drove
it, p=.50 — P14/P16/P18 notes in PREDICTIONS.md, affect07 reports);
u15 denominator honest everywhere (94 = 87 core + 6 g12b order arms +
1 dense backfill; strict scoring 84/87, whale/submarine lenient by
design); hysteresis softened to transcript-mediated + novelty
downgraded to "anticipated" citing SOPHIA (findings.json, README,
PREDICTIONS L45, u18-a0680 plain.md); premium chain completed to
length-with-optimum on the surfaces stuck at demotion #2 (GLOSSARY,
CONCLUSIONS, essay); langval cross-record caution (two-span norm fit,
fp16 overflow); four citations imported to RELATED-WORK.md
(litwatch-02: SOPHIA 2607.18100, Repetition Neurons 2410.13497,
Emotion Concepts 2604.07729, Cultural Awareness 2608.02486).

**Board**: dated notes on affect-02/-03/-05/-07/-08/-10, span-01/-02,
oneoffs-02, apparatus-11; new items apparatus-14 (landed) and
**oneoffs-04 (queued): the matched-text release control** — hand an
unsteered model the same 50-repeat prefix; decides transcript-mediation
vs latent hysteresis and is the sweep's one search-novel candidate.
Cheap and decisive; strong candidate for next run, alongside affect-08
(now specced with direction-as-unit + preregistered turn-end).

Queued next on the board: oneoffs-04, affect-08, apparatus-13
(lab-perf), apparatus-08/-10, span-09/-10, pressure-02.
