# Reproduce Express01

The frozen design is `protocol.md` and `spec.json`; amendment 01 preserves the
initial capture stop and replaces the conflated numerical/causal gate. Use the
cached checkpoint revisions and checkpoint-specific instruments named in the
specification. Source hashes bind the original scripts; amendment 01 identifies
the one approved capture-code change. The analysis script hash was recorded
before any expression results were inspected.

```sh
HF_HUB_OFFLINE=1 .venv/bin/python probes/test_express01.py
systemd-run --user --unit=jspace-express01-reproduce -p MemoryMax=40G \
  -p WorkingDirectory=/home/wolfram/Projects/jspace-probes \
  --setenv=HF_HUB_OFFLINE=1 --setenv=TRANSFORMERS_OFFLINE=1 \
  /home/wolfram/Projects/jspace-probes/.venv/bin/python -u probes/express01.py all
.venv/bin/python probes/express01_analyze.py
.venv/bin/python probes/express01_plot.py
.venv/bin/python probes/site.py
```

Run only after confirming that no other model process uses the GPU. Existing
completed capture files are skipped. Use an isolated copy for a fresh replication;
do not delete the historical records. Check systemd and `processes.json` for
completion and exit codes. An exit 137 or -9 stops the study and must not be retried.

`captures/*.json` contains exact input IDs, full-depth prepared-position features,
archive replay sensitivity, timing, generated controls and candidate likelihoods.
`analysis.json` contains held-topic predictions for every row and all sensitivities.
The 54 `express01-*` record directories contain full films. Matching `affect02-*`
directories contain all 24 checkpoint emotion ribbons. Selected residual tensors
in local `states/` are reproducible and ignored by git; their checksums are in
`state-manifest.json`. A public checkout can reproduce the analysis from feature
JSON without these tensors or a GPU. No provider key or paid judge call is needed.

## Small readout batch

`probes/express01_scan.py` accepts a JSON list of `{"id":"name","user":"text"}`
rows or `{"id":"name","prefix_ids":[...]}` rows for an exact saved prefix. It
loads once, reads four layers and the output distribution at the prepared answer
position, and includes the checkpoint emotion projections. It generates no answer.
Use a matched default/restrained/expressive trio with identical event content.
The returned numbers are readouts, not an introversion or flattening diagnosis.

```sh
systemd-run --user --unit=jspace-expression-scan -p MemoryMax=40G \
  -p WorkingDirectory=/home/wolfram/Projects/jspace-probes \
  --setenv=HF_HUB_OFFLINE=1 --setenv=TRANSFORMERS_OFFLINE=1 \
  /home/wolfram/Projects/jspace-probes/.venv/bin/python probes/express01_scan.py \
  --arm B --batch /absolute/path/to/batch.json --out /absolute/path/to/readouts.json
```

This supports the three calibrated Qwen14 arms only. New checkpoints require
checkpoint/lens/header calibration. Negative expression cannot be inferred from
an empty positive-language vocabulary. Compare output and plain-token controls,
use held-topic validation, and keep prompt recruitment distinct from capacity loss.
