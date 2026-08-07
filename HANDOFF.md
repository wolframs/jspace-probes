# Handoff — 2026-08-07 evening (post instrument audit)

Read `CLAUDE.md` first (binding: pre-design protocol, full-instrument
default, plain-language layer, push rule). `EMOTIONS.md` and
`MECHANICS.md` are same-rank mandatory reads. This file is the delta.

## Naming

**"Unit 20" = the langval batteries (affect-09/10, lv-*/lv2-* records)**
— Wolfram's term, and the record titles carry it. Use it.

## Landed 2026-08-06/07 (all committed + pushed, both remotes)

- **audit-02** (4 arms incl. emotion-vector readout): q27b amp flip
  survives matched controls (happy z=+5.8 under cluster amp, randoms
  ~0); matched-in-k ≠ matched-in-magnitude (MECHANICS §3c note,
  GLOSSARY entry); grader/emotion-lens agree at 27B, diverge on gemmas.
- **EMOTIONS.md** created (projection IS the readout — the audit-02
  lesson); **apparatus-02** (vanilla cross-check default-on in lab.run);
  **affect-08 slice** (g12b desperate split-half 0.409→0.801).
- **langval-3** (`probes/langval3.py`, results/langval-emofp): Unit 20
  24-emotion fingerprints. The pitch is two strategies on q27b —
  swift/python bipolar-suppress then crash in the candid turn;
  kotlin/csharp near-flat. **Suppression-cost/rebound is the exportable
  hypothesis** (board note on affect-10). csharp = only
  hostile-above-line under coercion. fingerprints.html = heatmaps.
- **Unit 20 u18-grade overlays** (`probes/langval_viz.py`): all 48
  lv/lv2 records now have results/affect02-<id>/affect.json → dashboard
  ribbon+overlay. Full-instrument default written into CLAUDE.md.
- **INSTRUMENTS.md** (Opus-subagent audit): inventory, coverage matrix,
  ranked backlog. Headline gaps: vanilla 1/603, matched randoms 42/193
  steered, ribbon 62/603, films 333/603, stale miners.

## AGREED NEXT (Wolfram, 2026-08-07): tackle the audit backlog

Start with **apparatus-11** (zero-GPU backfill sweep, board item):
1. `lossmap2.rates()` register meter over all 603 stored generations.
2. huh.py + blind.py refresh (267→333 films, 447→603 records).
3. Ribbon wiring: showCompare + site.py record pages + lv/lv2 into
   affectviz.export_overview (#affect overview).
4. langval3-style fingerprints from every saved z.pt.
5. Vanilla backfill (~30 load-bearing records; lens pass only).
6. Generalize affect2.cross past its hardcoded 14-id RECORDS list →
   ribbons for u13 (60), u15d (51), u14 (23).
7. blind.refilm the 18 blind records.
Then: apparatus-12 (Fig-4C swap), audit-06 (matched randoms for u13
apology / u9 L62 / u18 doses — greedy, exact re-runs).

## Operational notes

- Monitor tool for watches (sleep-loop watchers get reaped).
- `pkill -f` self-matches the wrapping shell — kill by port
  (`fuser -k 8321/tcp`).
- Opus via OpenRouter: `"reasoning": {"enabled": false}` or content
  is None (audit02._judge).
- fp16 saves of gemma-12b norms overflow to inf (langval_z.pt trap;
  affect.py comment). Save norms float32/bfloat16.
- Detached runs: `setsid nohup bash -c 'cd <repo>; …' > log` with
  absolute paths (cwd trap hit once).

GPU free. Board current (apparatus-11/-12, audit-06 queued; audit-02,
apparatus-02 landed with evidence).
