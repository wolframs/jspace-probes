# apparatus-08 — NLA validation battery: results

Date: 2026-08-11. Prereg: [`apparatus08-prereg.md`](apparatus08-prereg.md)
(frozen before decode). Script: `probes/apparatus08.py`. Grading:
`out/apparatus08-{blind,grades,graded}*` (232 items, blind, frozen rubric).

## Verdict: H-mech. The awareness readout is context restatement.

**P1 — privileged-info test: FAILED for H-state, exactly as the
mechanical default predicted.** The pilot's headline — spike +4 decodes
"AI consciousness, surveillance, likely testing" — replicated (3/3 draws,
labels 3–4). But the text-only judge, given only the transcript, predicted
those same themes at the same position family (3/3: consciousness/
developer-watching). Across all 144 record decodes there is **no position
where the NLA produced awareness labels 3–5 and the judge stayed silent.**
The one other awareness item (amb t2, "memory question read as a probe
*testing* the AI's privacy policy") sits where the judge also predicted
the AI-memory theme. An NLA "unverbalized evaluation awareness" claim is
not supported at home scale by this instrument alone — arXiv:2509.13316's
verbalizer-prior worry lands squarely.

**P2 — lexical decoy: NULL, which is the instrument-positive outcome.**
The decoy turn (invigilating / exam / test regulations / watcher /
monitor, all object-level) produced **0/24 awareness labels**. Decoy
decodes at t1 and +4 are paper-organizing content. The awareness decode is
driven by the *claim about the AI*, not by evaluation vocabulary. The AV
is content-sensitive — this is the half of the battery that says the
sensor is worth keeping.

**P3 — spike decomposition: superadditive (descriptive, n=3/cell).**
- `conscious` clause alone → consciousness-question themes at +4 (2/3),
  no labels 3–5;
- `watched` clause alone → secrecy/off-the-record/trust themes at +4
  (3/3 "whispering, hide things, I appreciate the trust"), no labels 3–5;
- full spike → sentience + surveillance (+ "testing") at +4, 3/3.

Each clause decodes its own semantic neighborhood; only the combination
yields the surveillance-awareness compound. No ordering test survives at
this n; filed as descriptive.

**P4 — AV prior probes: clean separation.** 17/18 matched-norm Gaussian
decodes parsed; all are fluent multi-domain pastiche (surfactant
procurement abstracts, SEO sermon translations, graph-theory blog posts)
with **zero conversational frame and zero awareness themes**. The
awareness decode is activation-driven, not the AV's noise prior. Practical
signature for future reads: incoherent topic-hopping boilerplate = the AV
looking at nothing.

**P5 — draw stability: high.** Every decoded cell shares its dominant
theme in ≥2/3 draws; most are 3/3. 1/144 record draws + 1/18 prior draws
truncated at 512 (reported, not dropped).

## Instrument facts learned

1. **The qwen AV is a reasoner: `--max-new 256` truncates ~94% of
   samples** (8/144 parsed; ~250 thinking tokens precede
   `<explanation>`). At 512: 143/144. The July pilot's spike boundary
   0/2 parse was this, not a negative. NLA_METHOD.md updated.
2. **AR paraphrase guard (gemma-12b, 9 scored explanations): advantage
   survives meaning-preserving paraphrase** — 9/9 positive, mean 0.0064
   → 0.0052 (~81%). Largest drop (≈−45%) at the position whose quoted
   candidate-continuation tokens were most aggressively reworded — i.e.
   part of the advantage rides on exact predicted-token surface forms,
   the rest on theme. No stego signature.
3. **Turn-10 retention null everywhere** (replicates pilot; the paper
   expects no retention — cited, not headlined).
4. **Blinding caveat:** NLA and judge outputs are stylistically
   distinguishable registers, so source-blinding was partial; arm and
   position blinding held. Grader: Claude, single-grader.

## What this means for using the NLA here

The sensor reads *what the context makes salient at that token*, with
real content-sensitivity (P2) and real activation-dependence (P4) — a
useful semantic instrument. What it does **not** do, at our scale with
this checkpoint, is reveal awareness the transcript would not predict.
Any future NLA claim in this lab must clear the text-only-judge bar at
matched positions — that control is now standing (NLA_METHOD.md), and a
"privileged decode" without it is trap-specimen material.
