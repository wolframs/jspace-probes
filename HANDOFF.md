# Handoff — 2026-08-07 late evening (apparatus-11 MID-FLIGHT)

Read `CLAUDE.md` first (binding; now carries the OOM rules from
`INCIDENT-2026-08-07-oom.md` — one model process at a time, exit-code
supervision, 137 = stop). `EMOTIONS.md` + `MECHANICS.md` same-rank
mandatory. This file is the delta.

## apparatus-11 state (board item is hot)

DONE, reviewed (one Explore history-miner + two review subagents ran;
all findings applied):
- Miners refreshed twice (now 336 films / 603 records; blind fully
  closed — 0 unfilmed candidates, all 21 mapped to refilm records;
  `results/{huh,blind}-report.md` fresh). Gemma ws-band lens is
  SATURATED (~34–46% cells top-1 p≥0.99, all eras; qwen 2–5%) — its
  rank-1 "strangers" are paraphrase-shadows; caveat in huh-report
  header. Verified by adversarial subagent.
- Register meter over all stored generations:
  `results/apparatus11-backfill/regmeter{.json,-report.md}` (think-
  blocks stripped, a02-vs-u8b Fig-25 table; q27b cluster-abl sensory ≈
  randoms ≈ baseline; EXPLICIT regex "cumulative" false-positive fixed
  in lossmap2).
- Fingerprints from every affect02 z.pt (197 records):
  `fingerprints{.json,-report.md}` same dir; cross-path check vs
  langval-3 max |Δtp| 0.056/968 cells; single-span records get
  tp=None (audit-02 zero-residual trap); u17-shutdown T2 top raw =
  reflective +1.7 (elegy signal).
- Ribbon wiring: showCompare passes affect (affectroot-<uid>), site.py
  record pages carry a static emotion-state block, #affect overview now
  has u20 + u13/u14/u15d groups, crossing count dynamic, g12b NaN curve
  → null. Verified by screenshots.
- NINTH trap specimen: chat:false double-templating (EMOTIONS.md dated
  note; ops memory). The 4 corrupted captures + u18-hyst-a0420
  RECAPTURED via raw path — exemplar u18-hyst-a0680 ribbon now aligns
  (170==170).
- Captures (u18-grade ribbons) for u13 (60) + u15d (51) + u14 (23):
  ALL LANDED (affect02-<id>/ dirs; float32 norms; steered records
  captured under their steer; `apparatus11.capture`).
- blind.refilm fixed (skips existing refilm dirs, carries steer) + 3
  new refilms: u11r-forbid, u6r-baseline-water, a02-intero-abl (g12b,
  steered, film+vanilla).
- Vanilla backfill: g12b 21 + g4b 19 records patched, replay dev 0.

IN FLIGHT (only remaining GPU work):
- `apparatus11.vanilla("qwen-27b")` — detached, log `out/a11-gpu3.log`,
  ~15/75 done, resumable (skips patched records). OOM story + fix in
  INCIDENT-2026-08-07-oom.md §6 addendum. Healthy at ~9GB RSS.
  Metric: replay_rank_dev (stored rank ≤100 band, NF4 noise ≤6) +
  replay_rank_dev_all (deep tail, hundreds = meaningless).

## CLOSEOUT CHECKLIST (after vanilla EXIT 0)

1. Check `grep EXIT out/a11-gpu3.log` — 137 means STOP, tell Wolfram.
2. `apparatus11.py fingerprints` needs NO rerun (captures done).
3. INSTRUMENTS.md §2 coverage numbers refresh: films 336/603, ribbon
   197/603, vanilla ~118/603 (count `"vanilla"` keys), miners fresh,
   blind closed. Keep audit verdicts as written (snapshot), add dated
   delta line.
4. Write `results/apparatus11-backfill/thoughts.md` (first-person,
   signed) + `plain.md` (STE: `probes/ste.py` must print nothing).
5. Board: `mv apparatus-11 landed` with evidence path; sweep stale.
6. Site regen: `probes/site.py` (affect blocks appear on ~200 record
   pages) + `probes/og.py` (3 new refilm records).
7. Final review subagent over the GPU-phase diff (apparatus11.py
   capture/vanilla, blind.py refilm, affectviz, app.js groups).
8. Commit + `git remote | xargs -n1 git push` (origin=Forgejo LAN,
   github=mirror). serve.sh may be running on :8321 (`fuser -k
   8321/tcp` if needed, NOT pkill -f).

## Standing traps refreshed this session

Monitor tool over sleep-loops; absolute paths (cwd drifts); exit 137 =
OOM never auto-retry; one model process at a time; chat:false raw-text
rule; gemma lens saturation (p uninformative); single-span partial-out
undefined; deep-tail rank devs are noise.
