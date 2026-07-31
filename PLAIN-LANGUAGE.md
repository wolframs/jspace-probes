# PLAIN-LANGUAGE.md — the house standard for reader-facing text

This lab writes for itself. The result is accurate and unreadable: a page
that opens with "the furniture is bolted to the lens" tells a first-time
reader nothing, and it fails the one person whose judgement the lab runs
on. This file defines the **plain layer** — a parallel set of texts, in
simplified technical English, that carries the same claims in language a
reader can understand.

**The 30-second rule.** A reader must get the meaning of any page within
30 seconds, from any entry point, with no prior reading. 30 seconds is
about 90 words. So every page opens with a short version of 25 words or
less, and every hard word links to its definition on the same page.

**Nothing is deleted.** The original text stays exactly as written and
moves into a **Research notes** container on the same page. The plain
layer is added on top; the lab's record is not edited. This also keeps
the preregistration discipline intact (see PREDICTIONS.md).

---

## 1. The standard

The plain layer follows **ASD-STE100 Issue 9** (2025-01-15), Part 1 —
the 53 writing rules — with the four documented deviations in §3. Rule
numbers below are the standard's own.

We do not claim certification. STE was written for aircraft maintenance
procedures. Its strongest section is procedural writing; ours is
descriptive and argumentative, which is STE's thinnest area (Section 6,
six rules). We follow it because it gives **checkable numeric limits**
where "write clearly" gives none, and this lab has 499 records to keep
consistent. `probes/ste.py` enforces what a machine can enforce.

**Our jargon is covered by the standard itself.** Issue 9 permits words
outside the ~875-word dictionary when they are *technical nouns* (Rule
1.5) in one of 22 categories. Category 7 is mathematics, science, and
engineering. Category 19 is computer science and information technology
— and Issue 9 lists **token**, **large language model**, **embedding**,
and **machine learning** as its own worked examples. So `token`,
`layer`, `residual stream`, and `lens` are legal STE, on one condition
the standard also sets (Rules 1.8, 1.11): the terms live in a maintained
list, and one referent gets exactly one term, everywhere. That list is
`plain/terms.json`.

Precedent worth knowing: Simple English Wikipedia tells its own writers
to defer to this standard for science and technical topics.

## 2. The rules we enforce

Machine-checked by `probes/ste.py`. STE rule numbers in brackets.

| # | Rule | Limit |
|---|---|---|
| R1 | Sentence length, descriptive text [6.3] | ≤ 25 words |
| R2 | Sentence length, instructions [5.1] | ≤ 20 words |
| R3 | Sentences per paragraph [6.6] | ≤ 6 |
| R4 | One topic per sentence and per paragraph [4.1, 6.5] | — |
| R5 | Multi-word noun length [2.1] | ≤ 3 words |
| R6 | Active voice [3.6] | passive only when the actor is unknown |
| R7 | No `-ing` verb forms [3.5] | except inside a registered technical noun |
| R8 | Simple tenses only [3.2] | infinitive, imperative, simple present/past/future, past participle as adjective |
| R9 | Do not omit words; no contractions [4.2] | write "do not", not "don't" |
| R10 | One word, one meaning; one meaning, one word [1.3, 1.11] | see `plain/terms.json` |
| R11 | No metaphor, no idiom, no irony, no in-joke | — |
| R12 | Every term of art is registered and linked on first use [1.5, 1.8] | — |
| R13 | Numbers carry their scale | "rank 1 of 250,000", not "rank 1" |
| R14 | No semicolons [8.1] | use two sentences |
| R15 | No banned modals [3.4] | no `shall`, `should`, `may`, `might`, `would`, `could` — use `can`, `will`, `must`, or §3.1 |
| R16 | No Latin abbreviations [GR-6] | no `e.g.`, `i.e.`, `etc.`, `vs.` |
| R17 | Keep the conjunction "that" [GR-1] | it helps every reader and every translator |

Word counting follows Rule 8.6: a number with its unit, an abbreviation,
a quoted string, a parenthetical, and a hyphenated word each count as
**one** word.

Read R11 twice. The lab's voice is built on metaphor — *furniture*,
*weak king*, *elephant tax*, *the mouth says No*, *the sub-unit of
shame*. Every one of those is banned in the plain layer and belongs in
the research notes. The plain layer says what happened.

## 3. Four deviations, and why

STE is a maintenance-manual standard. Four of its rules would make this
lab's writing *less* accurate, so we deviate on purpose and in a fixed
way. An undocumented deviation is a mistake; a documented one is a
dialect.

### 3.1 Uncertainty — the important one

STE bans `may`, `might`, `could`, and `should`, and offers no way to
express graded confidence. This lab's entire value is calibrated
hedging: it publishes retractions, demotes its own findings, and marks
the difference between "measured" and "possible". Flattening a hedge
into a declarative would be a **scientific error**, and §5.1 forbids it.

So we keep uncertainty, but only through this closed ladder. Use these
words, in these forms, and no others:

| Confidence | Write |
|---|---|
| Direct measurement | **We measured X.** |
| Supported by the data | **The data shows X.** |
| Our reading of the data | **We think X.** |
| Possible, not tested | **X is possible. We did not test it.** |
| Open question | **We do not know.** |
| Known limit of the method | **This method cannot show X.** |
| Correction | **We were wrong. The correct result is X.** |

`can` and `possible` are approved STE words, so this ladder stays inside
the dictionary while restoring the meaning STE cannot express.

### 3.2 Past tense for findings

STE prefers the imperative and simple present. Experiment reports are
history: **"The model answered No"**, not "The model answers No". Simple
past only — Rule 3.2 permits it.

### 3.3 Quoted model output is never edited

Model output is data. It keeps its original spelling, spacing, and
punctuation, inside quotation marks, and counts as one word (Rule 8.6).

### 3.4 We name ourselves

STE's active-voice rule wants a named actor. Ours are "we" (the lab) and
the model by name. Never "it was found that".

## 4. The shape of a plain text

Every record page uses these headings, in this order. Only the first is
mandatory.

```markdown
**The short version.** One sentence, 25 words or less. State the result.

**What we did.** One to three sentences. The question and the method.

**What we found.** Two to five sentences. The numbers, with their scale.

**What it means.** One to three sentences. The interpretation.

**What this does not show.** One or two sentences. The limit of the claim.
```

The last heading is the lab's honesty slot. Use it whenever the original
hedges, and always when the claim is about absence — the lens can only
show what it can see, so "we did not find X" never means "X is not
there".

Length: a record summary is **200 words or less**. Finding cards: plain
title ≤ 12 words, plain body ≤ 60 words. Unit summaries ≤ 70 words.

## 5. Accuracy rules (these outrank readability)

1. **Do not upgrade a hedge.** If the original says "suggests", the
   plain text uses the §3.1 ladder — it does not say "shows".
2. **Do not drop a correction.** Several records carry dated
   corrections and one retraction. The plain text states the correction
   in the short version, not in a footnote.
3. **Do not invent numbers.** Every number in the plain text must appear
   in the original or in the record's JSON.
4. **Keep the actor.** "Qwen 27B answered No" — not "No was answered".
   Name which model: the three differ, and most findings are about the
   difference.
5. **Absence claims carry the basis caveat.** See GLOSSARY.md: the lens
   reads what the model could say next. It cannot see what the model has
   no words for.
6. **A failed prediction stays failed.** Where the lab lost a
   preregistration, the plain text says so.

## 6. Where the plain texts live

```
results/<id>/plain.md      per record        (original: thoughts.md)
plain/conclusions.md       the essay         (original: CONCLUSIONS.md)
plain/units.json           unit summaries    (original: app.js UNIT_NOTES)
plain/terms.json           the glossary      (source: GLOSSARY.md)
dashboard/findings.json    `pt`/`pb`/`pdesc` fields beside `t`/`b`/`desc`
```

Check everything with:

```sh
.venv/bin/python probes/plain.py inventory          # what is still missing
.venv/bin/python probes/ste.py --all --summary      # conformance
```

— Claude (Fable 5), 2026-07-31
