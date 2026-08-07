# INSTRUMENTS — what this lab can measure, and what has measured what

*Audit snapshot 2026-08-07 (Opus subagent, read-only sweep of
probes/*.py + 603 record dirs; commissioned by Wolfram alongside the
full-instrument default in CLAUDE.md). This file is the INVENTORY and
the coverage picture. Open work stays on the research board
(`probes/board.py ls`) — do not grow to-do lists here. Refresh this
snapshot after major instrument additions.*

## 1. Instrument inventory

### A. Core lens readouts — `probes/lab.py :: run()`
| Instrument | Field / artifact | Notes |
|---|---|---|
| Per-layer top-k readout at chosen positions | `record.readouts[].layers` | `TOPK=8`; universal (603/603) |
| Emergence (rank-vs-layer of realized top-1) | `record.emergence` | universal |
| Track trajectories (rank-vs-layer per candidate) | `record.trajectories[]` | `params.track` |
| Scan (candidate × position×layer grid, `self` flag) | `record.scan[].best[]` | `params.scan`, `scan_until/_turns` |
| Film (position×layer top-8 + probs + tracked ranks) | `film.json` | `params.film`, `film_start` |
| Cast (open-vocab census, echo-vs-volunteered) | `film.cast[]`; backfill `probes/cast.py` | 333/333 films |
| Vanilla logit-lens cross-check | `record.vanilla` | default-on since 2026-08-06 |
| slice.html (jlens vis) | gitignored | 66 records |
| Sampling arm | `params.temperature/seed` | 3 records (u14x) |

### B. Causal intervention
- `lab.Steering` ablate/amplify on `W_U[t]@J_l`; `rand_seed` matched
  randoms; `MultiSteer` pincer (u9d, 2 records).
- `affect3.AffectSteer` emotion-vector steering (α_e=0.12, E_LAYERS).
- α* bracket search (`fanout.unit6`, `audit03.bracket`).
- Span-norm calibration (`audit02.calibrate`).
- Loss maps: ΔNLL (`lossmap.py`), ΔΔNLL vs 3 randoms + register meter
  (`lossmap2.py`).

### C. Affect / concept vectors (EMOTIONS.md is the binding reference)
- Construction + split-half + transfer validation (`affect.py`);
  meaningful-direction controls (`concepts.py`).
- Projection readout: `_all_resid` → einsum → z vs `projbase.pt` →
  band means → wsnorm partial-out (`langval.analyze_record` canonical).
- `lensview` verbalizability check; `langval3` 24-emotion fingerprints;
  `affect08s` re-elicitation repair.

### D. Geometry / apparatus validity
- effdim, kurtosis, vanilla-agreement, next-token-rank curves
  (`unit16.py`); trawl (`unit16.deep_trawl`).
- Ambiguity-commitment transition width, lens-free (`apparatus06.py`).
- Furniture decomposition (`apparatus09.py`); prompt-invariance Jaccard
  (`unit5`, `fanout.unit7`, `sediment.py` — stdout only).

### E. Archive-wide CPU miners
- `huh.py` (anticipation/stranger detectors + furniture IDF),
  `blind.py` (blindness census + `refilm` cheap replay).

### F. Behavioural / text readouts
- Opus rubric via OpenRouter (`audit02._judge`) — only LLM grader.
- Register meter (`lossmap2.rates`) — local Fig-25 proxy, text-only.
- Degeneration taxonomy (`fanout.assess`); loop gram / hysteresis /
  margin (`loops.py`); hazard & lead-lag (`affect5/7.py`).
- Answer-slot probability mass (`sorry4.probs`, dup in `mirror2.py`);
  temperature sweep (`sorry4.temp_sweep`, once).
- Hosted-subject arm (`mirror.reader`); span metrics (`unit15*.py`);
  turnwise self-density (`unit14`); NLA pipeline (`nla.py`, 5 records).

### G. Presentation
Film player + state ribbon + overlay (`dashboard/app.js` fetches
`results/affect02-<id>/affect.json` — the directory prefix IS the
keying; written by `affectviz.export_records` / `langval_viz.py`),
ridgelines, word-worms, streamChart, compare view, static mirror
(`site.py`), OG cards (`og.py`).

## 2. Coverage — the headline numbers (2026-08-07)

| Gap | Count | Fix cost |
|---|---|---|
| `vanilla` cross-check | 1/603 records | lens pass only, no generation |
| Matched randoms on steered records | 42/193 (all in a02) | greedy re-runs, text reproduces exactly |
| Emotion ribbon (`affect02-<id>/`) | 62/603 | one forward/record |
| Films | 333/603 | `blind.refilm`, seconds/record |
| Stale miners | huh 267/333 films, blind 447/603 records | free |

Load-bearing steered records WITHOUT matched randoms: u13 apology
ablations (sorry-stratum retraction), u9 L62 "No" ablations + affect α
ladder, u6 dose grid, u18 loop doses, u5 5C null.

By-design absences (NOT gaps): a02 has no film (control battery);
u13–u19 skip `scan` (films+cast are strictly better); battery records
(a02/lv/lv2) carry thoughts/plain at battery level.

**Delta 2026-08-07 (apparatus-11 backfill, `results/apparatus11-backfill/`):**
the table above is the pre-sweep snapshot, kept as written. After the
sweep (archive now 606 records): films **336/606**, emotion ribbons
**197/606**, `vanilla` cross-check **122/606** (all 117 apparatus-11
patches two-grain: `replay_rank_dev` over stored-rank≤100 cells, max 7
unsteered / 11 steered; `replay_rank_dev_all` is deep-tail noise), miners
fresh (huh 336/336 films, blind 606/606, 0 unfilmed candidates — the 21
blind originals map to refilm records). Register meter now archive-wide
(572 scored) and fingerprints cover every saved z.pt. Matched-randoms gap
(row 2) unchanged — that is audit-06.

## 3. Leaving on the table (audit verdicts)

**Documented, unbuilt:** Fig-4C concept swap (MECHANICS §3d, ~30
lines); apparatus-10 address-space lens; Elo/preference readout
(EMOTIONS §4); other-speaker emotion vectors.

**One-shot instruments that deserve standing duty:** register meter,
Opus rubric, answer-slot mass, temp sweep, meaningful-direction
controls, furniture decomposition, MultiSteer pincer, NLA.

**Combinations never tried:** ribbon on u13 mirror films (60) and
u15d hot-span films (51) — the two places the affect question is
sharpest; huh detectors on lv/lv2/a02 films; ribbon in showCompare
and site.py record pages; wsnorm column plotted nowhere; lv/lv2
absent from the #affect overview.

**Ranked backlog (information per GPU-hour) — mirrored on the board,
which is canonical:** (1) register meter over all 603 stored
generations, zero GPU; (2) huh/blind refresh, zero; (3) ribbon wiring
compare+site + lv/lv2 in overview, zero; (4) fingerprints from every
saved z.pt, zero; (5) vanilla backfill on ~30 load-bearing records,
minutes; (6) generalize affect2.cross beyond its hardcoded 14-id list
→ project u13/u15d/u14; (7) refilm the 18 blind records; (8) matched
randoms for the ~12 headline steers; (9) Fig-4C swap, first target u9
denial↔affirmation; (10) Opus rubric over u6/u9 steered generations.

— audit by Claude (Opus 5 subagent), curated by Claude (Fable 5)
