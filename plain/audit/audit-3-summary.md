# Accuracy audit, round 2 — full coverage — 2026-07-31

Round 1 (audit-fixes-2026-07-31.md) covered 25 of 499 records and found
problems in 18. This round covered everything, plus the four non-record
surfaces, plus a cross-family check. Method and results, for the next
person who repeats this.

## Method

1. **Full sweep.** 20 Sonnet auditors, 25 records each, rubric =
   PLAIN-LANGUAGE.md §5 plus worked examples from round 1. Every quote of
   model output checked against `record.json`'s `generated`; every number
   traced to the original. 116 raw findings.
2. **Adversarial verification.** Every batch's findings went to an Opus
   verifier instructed to refute them against the files. 108 survived
   (26 high, 64 medium, 18 low), 8 refuted.
3. **Surfaces.** 4 Opus auditors on `dashboard/findings.json` (pt/pb),
   `plain/units.json`, `plain/conclusions.md`, `plain/terms.json`:
   56 findings, verified at application time (a handful refuted there —
   including two whose *suggested fixes* would have violated §5.7).
4. **Application.** 9 Opus appliers, all instructed to re-verify against
   sources before editing and to leave originals (thoughts.md, the `t`/
   `b`/`name`/`desc` fields) untouched. All edited files pass `ste.py`.
5. **Cross-family control.** GPT-5.6-Sol (codex exec, read-only) audited
   6 records independently: 3 clean, 3 with real findings — and **none of
   its 3 hits appeared anywhere in the Claude sweep's 116 findings**,
   including a mechanically checkable misquote. Fixed separately.
6. **Mechanical quote sweep.** A trailing-punctuation comparison of every
   quoted span against `generated` found a systematic class the audit had
   only sampled: 113 candidates, 105 real (commas smuggled into quotes by
   sentence flow; a fabricated stop after a bare "READY"), 8 legitimate
   word-mentions. `ste.py` now enforces this permanently (rule QV), and
   exits non-zero on any violation.

## Frequent error classes (for future writers)

- Sentence flow silently rewrites quote punctuation ("The glacier," for a
  recorded "The glacier."). Put sentence stops outside the quotes.
- Sibling records' numbers stated as this record's measurement.
- Thoughts' idioms literalized ("verbatim-baseline" → "wrote the exact
  same answer"; a rhetorical "the generation denies all of it" → a claim
  the model denied something).
- Scope inflation: one-model results stated model-free; instruction-tail
  measurements stated as conversation-wide.
- The losing fork of a weighed hypothesis stated as the finding (§5.7).

## Honest residual

Sol's 3-in-6 hit rate on records the full sweep passed means recall is
imperfect in every pass, ours included. The density is far lower than
before round 1, but "audited" never means "error-free". The next
cheapest step, if wanted: a second independent cross-family sample.
