# Reproduce the model-judge phase

Wolfram replaced the human-rating phase with blinded OpenRouter judges.
There is no participant recruitment or manual coding task to complete.
The [former human instructions](organizer-human-archive.md) remain an archive.

1. Read the [judge protocol](judges/protocol.md), including transport and parser amendments.
2. The 24 captured conversations are fixed. The task manifest contains anonymous paired text, both orders, and deduplicated openings.
3. Run `.venv/bin/python probes/folk01_judge.py run` with the local OpenRouter key. Completed exact requests are reused; missing requests consume API credit. Never publish the key.
4. Run `.venv/bin/python probes/folk01_judge_analyze.py` for the separate judge tables, uncertainty bounds, order checks and diagnostic associations.
5. Run `.venv/bin/python probes/folk01_judge_audit.py` for quote sensitivity and the arithmetic check. Run `.venv/bin/python probes/folk01_judge_verify.py` to check coverage, schema extraction, request hashes and quote flags.
6. Regenerate with `.venv/bin/python probes/folk01_site.py`, then the standard site and preview generators.

[Read the report](/folk01.html) or inspect [raw model judgments](judges/analysis.json).
Model judgments stay separate from the former human importer. No synthetic human responses are created.
The remaining two frozen topics are held out for future predictor validation.
