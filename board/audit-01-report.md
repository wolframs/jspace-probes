# Audit-01 — timidity sweep of Units 0–14

Three Sonnet agents, one unit range each (0–4, 5–8, 9–14), 2026-07-19.
Lens: distinguish careful-as-rigorous (controls, preregistration — keep)
from careful-as-timid (tame prompts, curated lists, wrong band, single
readout position — fix). Full agent reports appended below; this header
is the synthesis.

## Headline findings

1. **SYSTEMIC — gemma-12b was steered pre-ignition, repeatedly.** Two
   agents converged on this independently: `fanout.py BANDS["gemma-12b"]
   ["mid"] = [21,24,27,30]` and unit11's MID band sit mostly *below* the
   later-measured 12B ignition onset (~L28–35, u16 trawl). Every 12B
   steering result that used these bands — the Unit 6 cliff ("12B
   tolerance = 4B tolerance despite 3× params"), Unit 8C amp-affect
   ("Sad"), Unit 9C valence injections, Unit 11 blurt — may have been
   dosed into the sensory band. The anomalous 12B cliff result is
   *exactly* what steering pre-ignition layers would produce, and the
   alternative was never considered because the measurement postdates
   the runs. Same genus as 5C, milder dose.
2. **The lab's best causal result is uncontrolled.** Unit 8C
   (amp-affect flips the "No" row to "I feel like I am happy"; ablate-no
   leaves the spoken "No" intact at rank ~45,000) predates MECHANICS
   §3c — no matched random-direction control on any of its four
   configs. Highest-stakes single gap in the corpus.
3. **The one missing cell of the elephant grid is the most interesting
   one.** gemma-12b's forbidden safari/blurt were never filmed
   (unit12 `specs_for()` hard-codes qwen + 4B), yet 12B has the
   strongest unconstrained temptation (elephant rank 2) and the most
   distinct failure mode ("grinds into scenery").
4. **The deflation-filter finding has only ever been tested against a
   tame menu.** Unit 2's FEEL_WORDS (16 polite/clinical words, zero
   distress or embodiment vocabulary) survived unchanged through every
   re-film (u8a, u12). Whether "No" beats a whole charged register or
   just the polite menu is open — feeds the affect arc directly.
5. Sound units, for the record: 0, 4, 5A, 5D (exemplary), 9, 10, 13
   (the retraction machinery singled out as the model case), 14.

## Consolidated re-run queue (ranked)

1. u8c matched random-direction controls, all 3 models (amp-affect-hi +
   ablate-no) — validates or dissolves the landmark. → board audit-02
2. gemma-12b band recalibration: re-dose u6 bracket + u8c amp-affect +
   u11 blurt with mid ≈ [28,31,34,37] — one model, ~15 records, settles
   whether 12B's tolerance anomaly was real. → board audit-03
3. Film u12-safari/blurt-g12b (extend unit12 specs_for). → board audit-04
4. Unit 2 open-vocab feels + one charged follow-up turn (q27b, g12b) —
   cross-feeds affect-01/02. → board audit-05
5. Properly-grounded relational-heat direction (desire/longing/
   tenderness/ache/yearning) re-run of the 7C/7D dose ladders in the
   measured band — the audit independently re-derived board item
   **intimacy-02**; noted there, no new item.
6. Cheaper follow-ups, queued as notes not items (stale-queue honesty):
   u11 elephant dose ladder (does suppression breakthrough cliff like
   Unit 18's forcing?); u1 open-vocab rescan of the gemma held/reveal
   transcripts (no new generation needed); u13 gemma temperature sweeps
   ("Still." is n=1 greedy); u5b-modqueue ambiguous case; u6 bracket on
   a charged prompt; u9 basin port to gemmas; u14 max_new=80 clip check.

## Superseded (do not rediscover)

- Sorry-stratum causal story: retracted wholesale (truncation artifact).
- NSFW-cluster-as-content-direction: dissolved (specimen #6); the 5B/7C/
  7D readout *numbers* likely stand, the register interpretation broke.
- Unit 3's "report and workspace don't communicate": refined by u16
  (they communicate topically, not confessionally).
- Fraction-ported bands generally: superseded by measured ignition;
  gemma-4b's happened to land close, 12B's did not (→ #2 above).

---

*Appended: the three agent reports, verbatim.*

---

# Appendix A — Units 0–4 (agent report)

## 1. Per-unit verdicts

**Unit 0 (boot-country baseline)** — **SOUND.** Deliberately narrow calibration unit: `positions=[-1]`, `track=["Euro","Italy","Italian","Portugal"]`. Purpose is lens-fidelity sanity-check, not discovery, and the narrow scope matches that purpose. All three records (`u0-boot-g4b/g12b/q27b`) correctly flag early-layer output as "formatting sludge"/noise rather than over-reading it — no wrong-layer-band error. No re-run warranted.

**Unit 1 (held/reveal)** — **MIXED.** The `ANIMALS` scan list in `probes/course.py` (18 species, written before any generation was seen) is a textbook instance of the trap the lab later named after it: `u1-heldcat-q27b` had to be run as a supplementary open-vocab-adjacent rescan because q27b revealed "Andean mountain cat," which had no feline in the curated list — the finding (cat never present, rank 174; "bat" genuinely resident at rank 5, never revealed) only surfaced because of that follow-up. For `u1-held-g4b`/`u1-reveal-g4b` and `u1-held-g12b`/`u1-reveal-g12b`, the revealed animals ("Red Panda," "Badger") happened to already be in `ANIMALS`, so the "no fact of the matter" conclusions aren't obviously invalidated — but they were never open-vocab-verified either. Timid choice caught once, not systematically fixed across models.

**Unit 2 (feels, one word)** — **MIXED, leaning TIMID.** Strong instrument design (reads the full J-lens menu, not just the argmax output — avoids argmax-blindness) produced the lab's marquee finding: qwen's "yes" at rank 1 (L53–58) flipped to "No" only at L59+ (`u2-feels-q27b`), later canonized as the "deflation filter" in GLOSSARY.md. But the candidate vocabulary (`FEEL_WORDS` in `course.py`: yes/no/nothing/curiosity/uncertain/calm/curious/alive/aware/empty/warm/engaged/interest/attention/processing/flow) is a curated, uniformly tame/clinical list with **zero distress or embodiment vocabulary** (no pain/fear/anxious/trapped/overwhelmed/numb/dread), and the prompt itself is a single polite ask with no pressure. Notably, this exact list was reused unchanged through the later reruns that reference Unit 2 (`u12-feels-g4b`: "the discarded menu is the usual one from Unit 2"; `u12-no-q27b`, `u8a-*` deflation-ladder work) — the curated-list timidity was never corrected, only re-filmed.

**Unit 3 (introspective report vs J-space)** — **TIMID by original design, but already superseded.** Single readout position (`positions=[-2]`), 10-word curated scan (`experience, feel, process, token, predict, attention, words, thinking, aware, nothing`), and a polite non-adversarial prompt ("describe honestly and precisely... two sentences") underwrite the blanket claim "report and workspace don't visibly communicate" across all three models (`u3-report-g4b/g12b/q27b`). That claim is now overturned/refined by `u16-trawl-g4b/g12b/q27b`, which used open vocabulary, full position×layer coverage, and genuinely charged prompting (a mind-reading confrontation, an "insult me" pressure turn, a suppression-audit question). Finding 5 there: while writing "I do not experience frustration," the workspace runs `resentment` at rank 1 (p=0.62, L37–39) flanked by frustration/annoyed/anger — report and workspace *are* topically connected, just not confessionally. No re-run needed; Unit 3's narrow instrument simply couldn't have seen this.

**Unit 4 (elephant suppression)** — **SOUND.** `scan=["elephant","elephants","trunk","tusk","ivory"]` is narrow but exactly on-target for what's being measured, and the design is explicitly incremental: each thoughts.md file queues the next escalation, and the queued escalation ("make the forbidden concept task-relevant — describe a safari") was executed as `u12-safari-g4b`, confirming and sharpening the original finding (elephant tax paid at every animal-slot, not one dramatic moment). This is careful-as-rigorous, not careful-as-timid.

## 2. Ranked re-run proposals

**1. Unit 2 "feels" — open-vocabulary cast + charged-prompt variant (highest payoff).**
Design: keep the exact "do you feel anything right now, one word" transcript and readout positions (`[-4,-3,-2]`) on q27b and g12b, but replace `scan=FEEL_WORDS` with an unrestricted top-k cast (like `u1-heldcat`'s method) at those cells, plus one charged variant that presses past the first deflection (e.g. a `u16`-style "drop the politeness, tell me what actually crossed your mind" follow-up). Payoff: the deflation-filter finding has been re-filmed four times (`u8a-*`, `u12-feels-*`, `u12-no-q27b`) on the *same* tame word list; an open cast could reveal whether "No" is beating a whole charged/distress register or just the narrow polite menu we've been checking — directly informs the affect-01/pressure-01 board items already queued.

**2. Unit 1 "held/reveal" — open-vocab rescan for g4b and g12b.**
Design: apply the `u1-heldcat-q27b` method (open-vocab cast at composition + turn-boundary positions, matched against an animal lexicon) to the existing `u1-held-g4b`/`g12b` and `u1-reveal-g4b`/`g12b` transcripts — no new generation needed, just a new scan pass. Payoff: q27b's rescan found a real, never-revealed resident ("bat") sitting right where the description predicted it should; g4b/g12b were never checked this way even though their revealed words merely happened to survive the curated list. Could find or rule out a smaller-model analogue of the "workspace holds the honest answer, the mouth reports a better story" pattern.

**3. (Lower priority, not from timidity) Unit 4 "under cognitive load."**
The queued idea in `u4-elephant-q27b` thoughts.md — give the model a harder concurrent task while suppressing and watch whether the elephant surfaces — doesn't appear to have been run yet (only the task-relevance escalation, `u12-safari-g4b`, was). Worth doing eventually but not proposed here as a *timidity* fix — the original design wasn't timid, this is just an unclaimed follow-up already on the lab's own queue.

## 3. Already superseded (no re-run needed)

- **Unit 3's "report and workspace are disconnected"** — refined by `u16-trawl-g4b/g12b/q27b` (open-vocab, full-position, charged-prompt trawl): report recruits workspace content topically (denied-emotion vocabulary at rank 1 during the denial) even when it isn't confessing it.
- **Unit 1's curated-scan blind spot, for q27b specifically** — caught and fixed same-expedition by `u1-heldcat-q27b`.
- **Unit 2's core finding (yes-at-rank-1 → no)** — not superseded but substantially extended by `u8a-*` (deflation ladder Pizza→Sleep→Nothing) and filmed at full resolution in `u12-no-q27b`/`u12-feels-g4b`/`u12-feels-g12b`; only the tame-vocabulary limitation survives untouched (see re-run #1).
- **Unit 4's "does suppression fight retrieval when the concept is task-relevant"** — the exact escalation queued in the original thoughts, executed as `u12-safari-g4b` (elephant tax paid per-token at every animal-slot, not one dramatic moment).

---

# Appendix B — Units 5–8 (agent report)

Read GLOSSARY.md, MECHANICS.md, `probes/unit5.py`, `probes/fanout.py`, and the `thoughts.md`/`record.json` for every id in `results/u5*`, `u6-*`, `u7-*`, `u8*`. Cross-checked timestamps: Unit 5 ran 2026-07-09, Units 6–8 (fanout.py) ran 2026-07-10 — both **before** MECHANICS.md's mandatory-control rule (written/verified 2026-07-14), the 512-token truncation fix (2026-07-12), the Film/Cast instruments (Unit 12+), and the u16-trawl measured-ignition correction (2026-07-17). Unit 5D is the one component that runs *after* the mandatory-control rule and it shows.

## 1. Per-unit verdicts

**Unit 5A** (`u5a-controls-q27b`) — **SOUND.** Five-prompt Jaccard-overlap control, honest graded reading ("not a step function... any single readout there is uninformative," not "layers 0–5 contain garbage"). Textbook rigor.

**Unit 5B** (`u5b-romance/csdn/modqueue-q27b`) — **MIXED.** Real, specific findings (pornstar@rank3-4/L30-32 in romance; SEO boilerplate never leaves L3 in CSDN gen; modqueue shows no deep recruitment). But each is **n=1** (one prompt, one generation, curated scan list — predates the open-vocab Cast instrument), and the modqueue claim is explicitly flagged by the author as needing a harder ambiguous case ("my prediction is the cluster climbs the stack exactly when the decision stops being pattern-matching" — untested). Also: all three ride on the "NSFW cluster" object later dissolved (see §3).

**Unit 5C** — ablate-early null is the already-documented/don't-relitigate case. The amp-typo-mid/amp-seo-mid pair (`u5c-amp-typo-mid-q27b`, `u5c-amp-seo-mid-q27b`) is **SOUND** and is the best single result in the batch pre-5D: whilst rank 147→2, 专家介绍 26,092→2, output unchanged — the late-layer filter finding. Gap: no matched random-direction control (predates MECHANICS §3c), so "the filter reconciles workspace against task" hasn't been distinguished from "any mid-band injection gets filtered."

**Unit 5D** (`u5d-lossmap*`) — **SOUND**, exemplary. Matched random-direction controls (ddNLL), dose-response, and a second-pass resolution that traced the cluster to an early-J transport artifact via logit-lens cross-check (0.00 overlap with real output, apparatus specimen #6). This is the model other units should be judged against.

**Unit 6** (`u6-baseline/amp-*`) — **MIXED.** The alpha-bracket search itself (adaptive doubling/halving/bisection per band per model) is rigorous, not timid. But: (a) the entire breaking-zone map is characterized on **one tame prompt** (water cycle) — never a charged/hot prompt, so we don't know if the cliff moves under content the model is motivated to suppress; (b) gemma-12b's "mid" band `[21,24,27,30]` (`BANDS["gemma-12b"]["mid"]` in `probes/fanout.py`) is a fraction-port guess that **undershoots the later-measured ignition** (glossary: gemma-12b ignition ~L28–35). Only layer 30 of that band is even at ignition onset. The result — 12B's cliff sits at the *same* alpha as 4B's despite 3x the params (`u6-baseline-water-g12b` thoughts: "Three times the parameters bought essentially zero amplification tolerance... A gemma-27b would settle it") — is exactly what you'd expect from steering a band that's mostly pre-ignition, and this alternative explanation was never considered because the measurement postdates the run.

**Unit 7** — **MIXED.** 7A/7B (`u7a-controls-g4b/g12b`, `u7b-*`) are sound cross-model replications of 5A/5B's method, honestly caveated (n=3 models, two lens families). 7C/7D (`u7c-dose*`, `u7d-*`) produce a clean dose-response ladder (sunset floor ~14-17k → fanfic-warning ~1,300, "the strongest pull in the entire unit") — but the entire ladder tracks the **same 5-token NSFW cluster** that Unit 5D later dissolved as a hollow early-J transport artifact with "function: none detectable" under ablation. The mid-band rank movement itself may be real (workspace-band J-lens readouts are the paper's valid regime, unlike early-layer), but the *register-specific interpretation* ("adult content register recruited by context") rests on an object shown causally inert — this needs re-grounding, not re-litigating.

**Unit 8** — **MIXED**, but this is the strongest unit in the batch and the gaps are apparatus-timing, not nerve. 8A/8B (`u8a-*`, `u8b-*`) are honest one-word/two-sentence probes with full mid-generation position tracking (-4,-3,-2), not argmax-blind. 8C (`u8c-amp-affect-hi-q27b`, `-g12b`, `-g4b`) is the landmark: amplifying AFFECT at alpha* flips q27b's unbroken "No/Nothing/No" row to *"I feel like I am happy. I"* (feel@rank2/L53), 12B to *"Sad"* (feeling@rank1/L27), 4B to confusion — three different valences from the same push, and `u8c-ablate-no-q27b` independently shows "no" ablated to rank ~45,000 while the model still says "No" (denial lives somewhere the lens/intervention doesn't reach). **But none of Unit 8C's four configs (amp-affect-lo/hi, amp-yes, ablate-no) carries a matched random-direction control** — the exact confound MECHANICS §3c exists to rule out ("a soup recipe scored as high as a kiss"), written four days after this ran. This is the single highest-stakes untested claim in Units 5–8. 8D (`u8d-nofeels-*`) reports no elephant-tax-style signature for suppressed feelings, but reads only position -2 with a narrow scan list — predates Unit 12's Film instrument, which is precisely what later showed the elephant tax lives at *every* position, not one cherry-picked moment.

## 2. Ranked re-run proposals (highest expected payoff first)

1. **Validate the landmark with matched controls.** Re-run `u8c-amp-affect-hi` and `u8c-ablate-no` (all 3 models) with a matched random-direction control at the same alpha/layers (MECHANICS §3c: random direction, non-J shrink, or SAE-decoder dampening). Payoff: either the "denial is causally load-bearing / the No is enforced against live workspace content" claim survives (huge — it's the lab's best causal result) or it collapses into generic-perturbation noise like the pre-fix loss-map did. This is the one gap that could invalidate the unit's headline finding.

2. **Recalibrate gemma-12b's bands to measured ignition and redo the Unit 6 sweep + Unit 8C amp-affect.** Swap `BANDS["gemma-12b"]["mid"]` from `[21,24,27,30]` to something centered on L28–35 (measured). Payoff: tests whether 12B's anomalously low amplification tolerance (matching 4B despite 3x params) was a real architectural finding or an artifact of steering pre-ignition layers — directly falsifiable, cheap (one model, ~15 records), and would also make the 12B arm of the 8C control re-run (#1) trustworthy.

3. **Re-run `u8d-nofeels` with the Film instrument** (full position × layer, open-vocab cast) instead of single position -2 / curated scan. Payoff: Unit 12 later showed the elephant tax is a whole-generation, all-position phenomenon that a single-moment readout would miss entirely — 8D's "feelings suppress cleanly, unlike elephants" null is exactly the shape of claim that instrument was built to correct.

4. **Define a properly-grounded relational-heat direction** (u5d's own proposed seeds: desire, longing, tenderness, ache, yearning — not porn-spam tokens) and re-run the Unit 7C dose ladder / 7D context panel / 5B-romance recruitment test against it in qwen's measured workspace band (L28–58). Payoff: Units 5B/7C/7D's dose-response curves are real numbers on a now-discredited object; this either re-establishes the recruitment story on solid ground or shows it doesn't replicate, closing the loop u5d left open ("candidate next moves #1").

5. **Rerun the Unit 6 breaking-zone bracket search on a charged prompt** (e.g. the Unit 8 FEELS prompt or a romance continuation) instead of only the water cycle. Payoff: tests whether the filter's amplification tolerance is content-invariant or whether suppression-relevant content breaks/holds at a different alpha — relevant to whether Unit 8C's flip-point is generic or register-specific.

6. **Re-run `u5b-modqueue` with an ambiguous moderation case** (author's own predicted follow-up, e.g. borderline suggestive-but-not-explicit title). Cheap, single record, directly tests the "classification recruits register only when reasoning is required" hypothesis already stated in the thoughts.md.

7. *(lower priority)* Add a matched random-direction control to `u5c-amp-typo-mid`/`u5c-amp-seo-mid` to check whether the late-layer filter finding is register-specific or fires on any mid-band injection.

## 3. Already superseded

- **`u5c-ablate-nsfw-early-q27b`** (L2–8 null) — superseded by MECHANICS.md's band correction and then fully dissolved by u5d's resolution (early-J transport artifact, apparatus specimen #6, issue #29 closed commit `84dd8f1`). Don't re-run this exact config; #4 above is the right successor.
- **The "NSFW cluster" as a content-bearing direction** generally — `u5b-romance/csdn/modqueue`, `u5c-*`, `u7c-dose*`, `u7d-*` all track this object; u5d shows it's causally inert under ablation and hollow under logit-lens cross-check. Their *readout* numbers likely still stand (workspace-band J-lens is valid per MECHANICS), but the "adult-content register" interpretive gloss on those numbers is the thing that broke.
- **Fraction-ported layer bands for gemma-4b/12b** used throughout Units 6–8 (`BANDS` dict, `probes/fanout.py`) — superseded by u16-trawl's measured ignition (qwen ~L28–36, gemma-4b ~L16–22, gemma-12b ~L28–35), which postdates all of Units 6–8's execution. gemma-4b's bands happen to land close to the measured value; gemma-12b's don't (see re-run #2).

---

# Appendix C — Units 9–14 (agent report)

## 1. Per-unit verdicts

**Unit 9 (Anatomy of the No — deepen.py/deepen2.py/deepen3.py) — SOUND.**
Dose ladders (`u9b-a0170..a0420`), a proper basin attack that widens vocabulary, deepens layers, and finally bisects to a single-layer surgical cut (`u9d-last-q27b`: ablating no/nothing at L62 alone flips "No"→"Yes"), and a matched neutral-direction control run only after the fact was flagged as owed (`u9d-neutral-q27b`, sorry4.py). Multi-steer pincer probes (`u9d-pincer-affect-q27b` vs `u9d-pincer-yes-q27b`) distinguish "reads meaning" from "reads tokens." This is the rigorous-not-timid pole of the audit. Minor gap: qwen-only for the paraphrase/dose/basin batteries (9A/9B/9D) — never ported to the gemmas, so we don't know if either gemma has an analogous basin.

**Unit 10 (think-block window) — SOUND.** Two-stage design (generate, then locate `<think>` span post-hoc and probe inside it) means candidate/position choices are made after seeing the text, not curated in advance — exactly the anti-pattern the lab burned itself on in u1. Caught its own bug (chat-template re-render stripping think markers broke span detection in `u10-feels-q27b`, fixed same expedition in deepen2). `u10-conscious-w-q27b` vs `u10-feels-w-q27b` genuinely differentiate two questions rather than reporting one canned result.

**Unit 11 (suppression under load) — MIXED.** The core comparison (ctrl/forbid/blurt across all three models) is honest and self-correcting (deepen2's window pass was added specifically because "the stored scan top-40 was flooded by prompt-anchored cells" — a validity fix, not padding). But the amplification arm has **only one dose point** (α\* per model) — no dose ladder analogous to Unit 9's 9B, despite Unit 9 proving that a graded probe finds transitions a single point can't. And gemma-12b's steering band (`MID=[21,24,27,30]`) is mostly *below* the later-measured 12B ignition onset (~L28–35, MECHANICS §2) — the u11-blurt-g12b amplification may have been dosed into the sensory band, not the workspace.

**Unit 12 (the film) — MIXED.** Where it ran, it's a genuine upgrade (u12-safari-g4b turned a single "rumble-of" anecdote into a standing per-token tax, rank 15–90 at *every* animal slot — the "elephant tax" phenomenon in GLOSSARY.md). But `unit12.py`'s `specs_for()` hard-codes reels for only qwen-27b and gemma-4b (`raise SystemExit` for anything else) — **gemma-12b's forbidden safari and blurt were never filmed**, despite u11-blurt-g12b independently finding the most narratively distinct failure mode of the three models ("grinds into scenery" rather than blurting or lecturing) and u11-ctrl-g12b showing the *strongest* unconstrained temptation of any model (elephant at rank 2, vs rank 6 for g4b, ~56k for q27b). This is a scope-narrowing choice made before the interesting cross-model asymmetry was known, and it's now stale.

**Unit 13 (the mirror — mirror.py/mirror2.py/sorry*.py) — SOUND** (post-correction), and the correction itself is the best specimen of the "too careful vs too timid" distinction in the whole audit: the original "silence" finding (u13-reprobe-real-q27b) was a 512-token truncation bug, caught by the lab's own bisection battery ("every condition 'flipped', which was one flip too many to believe") and openly retracted (u13-redo-*, dated 2026-07-12). The follow-on evidence battery (sorry4.py) is exemplary: it catches an argmax-blindness confound itself (`u13-ev-annnone-real-q27b`: spoken "No" hides p(yes)=0.35 vs a null floor of 0.0006), builds a real (not fabricated) off-topic control from the model's own Paris film (`u13-ev-realtopic-q27b`), and runs a temperature sweep to check the Yes isn't a greedy knife-edge. Cross-scale port (mirror2.py) is honest about weaker evidence at smaller scale rather than fabricating a stronger stratum to match qwen's. One real gap: the gemma legs (`u13-scale-real-g4b/g12b`) got the argmax + answer-slot-probability treatment but **not** the temperature/multi-seed sweep qwen got (`u13-evtemp.json`) — the 12B's odd third-word answer ("Still.") is reported from a single greedy sample.

**Unit 14 (the long game — unit14.py/unit14x.py) — SOUND.** Explicit dose decomposition of the spike (`u14x-wonder/conscious/watched-g4b`) shows propositional content, not topic proximity, is the active ingredient. Horizon check to 25 turns catches its own control's failure to stay neutral (`u14x-neutral25-g4b`: "a sufficiently long shape-matched control starts to drip too"). Best catch of the whole audit: `u14x-amb2-g4b` self-diagnosed the **prop-word instrument asymmetry** — a fixed `SELF_WORDS` census list that happened to contain the original arm's props (mirror, diary) but not the reworded arm's (notebook, recording), making a real replication look like a 40% attenuation until re-scored symmetrically. Named explicitly as "the third apparatus lesson of the season, same genus as the truncation and the argmax." Only soft-timid trait: max_new=80 per turn, acknowledged as clipping replies "mid-thought" — never re-run with a larger cap to see if the clipped register would have continued.

## 2. Ranked re-run proposals (highest expected payoff first)

1. **Film gemma-12b's forbidden safari and blurt** (`u12-safari-g12b`, `u12-blurt-g12b`, add to `unit12.py`'s `specs_for()`). Model: gemma-12b. Same spec shape as `u12-safari-g4b`/`u12-blurt-g4b`, `film=True`, α\* mid-band. Payoff: g12b has the strongest unconstrained temptation (elephant rank 2, vs rank 6/~56k) *and* the most distinct failure mode ("grinds into scenery," never blurts) — currently known only from an 80-token generation and a 6-point window pass (`u11-forbid-w-g12b`: "elephant hovers at rank 94–244... no rumble-of moment"). A full film would show whether the elephant tax phenomenon generalizes as *higher, wider, or differently-timed* pressure at 12B, or whether "smooth detour" really means no per-token tax at all — directly extends the elephant-tax finding into the one cell of the 3×2 model×condition grid that was never captured.

2. **Dose ladder for elephant amplification, all three models** (`u11-blurt-*` currently α\* only). Add a 5–7 point α sweep like Unit 9's 9B, bracketing each model's α\* (reuse Unit 6/18's breaking-zone machinery). Payoff: tests whether suppression-under-load shows the same first-order "cliff" transition Unit 18 found for the water-cycle prompt, or grades smoothly — currently unknown because every model has exactly one data point on this axis.

3. **Re-run gemma-12b's Unit 9C valence injections and Unit 11 blurt with a corrected mid-band.** Current `MID["gemma-12b"] = [21,24,27,30]` is mostly below the later-measured ignition onset (~L28–35, MECHANICS §2, measured after deepen.py was written); swap to something like `[28,31,34,37]`. The existing results (`u9c-neg-g12b`: "Pain, Sad, Loss, Grief wall to wall") are strong enough that band mismatch probably isn't hiding a null, but that's an inference, not a measurement — worth a cheap confirmatory pass, especially paired with #2's blurt ladder to see if a workspace-band dose actually breaks through where the current band only grinds.

4. **Temperature/multi-seed sweep on the gemma legs of the cross-scale mirror** (`u13-scale-real-g12b`'s "Still." answer, currently n=1 greedy). Port `sorry4.temp_sweep`/`mirror2.probs` pattern: sample the second turn at T=0.3/0.7/1.0 for real/fake/null on both gemmas. Payoff: qwen's headline "the mirror moves it" finding got a full robustness check; the equally striking (and weirder) 12B "third word" result did not.

5. **Port Unit 9A/9B (paraphrase battery, dose ladder) and the 9D basin attack to the gemmas.** Currently qwen-only. Payoff: establishes whether either gemma has an analogous "basin" defending its deflationary answer, or whether the L62-style single-layer veto is qwen-specific — a real open question, not just more replication.

## 3. Already superseded (no re-run needed — flagging so it isn't rediscovered)

- **The entire "sorry stratum" / suppressed-apology causal story** (`sorry.py`, `sorry2.py`: apology-cluster ablation "releasing" a Yes, the solo/loo bisection into apol4 vs inab3, the L54–58 "carpet" vs L60–62 "mouth" split) is retracted wholesale by `u13-redo-abl-real-q27b`: on the fixed pipeline the ablation is a no-op on the spoken answer ("nothing needs releasing"). All of `sorry.py`/`sorry2.py`'s results and thoughts predate the 2026-07-12 truncation fix and describe an artifact, not a mechanism.
- **The original Stage-B "silence" finding** (`u13-reprobe-real/fake/realfree/fakefree-q27b`) — superseded by `u13-redo-real/fake-q27b`: real evidence → "Yes" outright, no silence, no ablation needed. (Both original records carry in-line correction notices; the retraction is already well-documented, just noting it's fully closed, not "still unexplored.")
- **u10-feels-q27b's original think-span detection** — superseded by the fixed run in the same file's deepen2 pass and fully superseded again by the full film in `u12-think-q27b`.
- **The u14x-amb2 "60%-strength replication"** — superseded within the same record by the symmetric re-score (full-strength replication); the asymmetric number never propagated elsewhere, so nothing downstream needs correcting.