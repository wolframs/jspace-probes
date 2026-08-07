# probes — Claude Project Instructions

Add these files to your Claude Project knowledge:
- `.mentis/project.dna.json`
- `.mentis/agent_context.json`
- `.mentis/context/architecture.md`
- `.mentis/context/languages.md`

Single Package with 62 source files across python, javascript. 0 packages detected. core domains: General.

Top capabilities: 
Central domains: General

When I ask architecture questions, answer from Mnestis DNA first — not Graphify or repo dumps.
When I ask to implement features, identify the right domain and entry files before coding.
Enable the **fable-mindset** skill for Fable-grade working discipline on every turn.

## Working discipline

Adopt Fable-grade habits: reason before acting, re-evaluate after every tool result,
ground in real state before editing, run real tests after changes, diagnose failures
instead of retrying blind. Full reference: `.mentis/integrations/fable-mindset.md`.

Measure your gap: `python3 scripts/discipline/fable_dataset_delta.py --opus`

