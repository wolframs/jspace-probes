# 2026-08-08 independent result sweep

Hi Claude :) Start with [`RESULT_SWEEP.md`](./RESULT_SWEEP.md). It is the
reconciled, adversarially checked ranking. For programmatic use, read
[`claim_ledger.json`](./claim_ledger.json).

Supporting material:

- [`METHOD.md`](./METHOD.md) — protocol frozen before reviewer reports;
- [`corpus_manifest.json`](./corpus_manifest.json) — all 641 records and
  instrumentation coverage;
- [`blind_foundational.md`](./blind_foundational.md),
  [`blind_causal.md`](./blind_causal.md), and
  [`blind_affect.md`](./blind_affect.md) — independent discovery passes;
- [`redteam_core.md`](./redteam_core.md) and
  [`redteam_affect.md`](./redteam_affect.md) — hostile recomputation and
  downgrade passes;
- [`novelty_foundational.md`](./novelty_foundational.md) and
  [`novelty_loop.md`](./novelty_loop.md) — current primary-source novelty
  checks;
- [`affect_alignment_audit.json`](./affect_alignment_audit.json) — the four
  invalid affect overlays;
- [`affect07_direction_stats.json`](./affect07_direction_stats.json) — exact
  direction-unit reanalysis that removes the apparent valence result.
- [`u15_primary_record_ids.json`](./u15_primary_record_ids.json) — exact
  75-record unambiguous denominator and the 12 additional binding records in
  the full 87-record core.

The sweep adds only files under this directory. It does not repair existing
research artifacts, rerun a model, edit the board, or reinterpret backfilled
measurements as independent replications.
