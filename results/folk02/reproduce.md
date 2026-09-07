# Reproduce Folk02

Use the repository `.venv/bin/python`.

Recompute results without credentials or paid calls:

```bash
.venv/bin/python probes/folk02_analyze.py
.venv/bin/python probes/folk02_verify.py
.venv/bin/python -m unittest discover -s probes -p test_folk02.py
.venv/bin/python probes/folk01_site.py
```

`manifest.json` fixes the anonymous tasks and rubric. `raw/` preserves every
completed response and its exact request; `parsed/` contains accepted JSON.
`errors/` and `ledger.json` retain failed attempts. `evidence.json` resolves
the judge's span IDs into exact text and original character offsets.
`analysis.json` provides per-judge profiles, individual paired differences,
cap sensitivity, coverage and agreement. Do not pool judges as extra samples.

The requested/returned Gemini IDs differ by the documented preview alias.
The API host is Surplus throughout. A route hint records the requested seller
provider, not independent attestation of the eventual underlying weights.
No fallback models or providers were requested by this runner.

The frozen runner supports resuming missing calls with `SURPLUS_KEY_FILE`
pointing to a private credential file. Do not put credentials into a command
argument, report, or repository file. The historical run has a $1.50 cap;
resuming preserves its ledger, including ambiguous charges. Transport retry
requires `--retry-failed` and allows at most two total attempts per cell, except the documented third
Sonnet c01 attempt after the discount-rounding diagnosis.
A new experiment needs its own output namespace and budget, not removal of
this ledger. No valid rating is rerun merely because it is inconvenient.

The 24 Folk01 source captures must retain their original hashes. Shared
openings are scored once, not four times. This is a text annotation record;
it does not create new GPU generations or claim activation measurements.
