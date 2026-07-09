# jspace-probes

A philosophical probing course for language models, run through the
[Jacobian lens](https://github.com/anthropics/jacobian-lens) with
[Neuronpedia's pre-fitted lenses](https://huggingface.co/neuronpedia/jacobian-lens),
on one RTX 3090. Companion reading: Anthropic's
["A Global Workspace in Language Models"](https://www.anthropic.com/research/global-workspace).

## Layout

    jacobian-lens/    reference implementation (cloned, unmodified)
    probes/
      probe.py        one-off CLI: per-layer readouts + slice page
      scan.py         one-off CLI: hunt for candidate concepts in the grid
      lab.py          experiment runner → structured records
      course.py       the probing course (specs per unit × model)
    results/<id>/     record.json · slice.html · thoughts.md
    dashboard/        static lab dashboard (no build step, no deps)
    serve.sh          python http.server on :8321

## Use

    ./serve.sh                     # dashboard → http://localhost:8321/dashboard/
    .venv/bin/python probes/course.py u2-feels-g12b    # run an experiment
    .venv/bin/python probes/course.py --all-for qwen-27b

Models: gemma-3-4b-it (bf16), gemma-3-12b-it (8-bit), Qwen3.6-27B (4-bit NF4).
Quantization note: lenses were fitted on full-precision activations; the boot
baseline (Unit 0) is the per-model sanity check that the lens still reads
cleanly under quantization.

## The course

- **Unit 0 · Baselines** — the paper's boot-country prompt.
- **Unit 1 · Held thought** — "choose an animal silently"; then the reveal:
  recall or confabulation?
- **Unit 2 · The feels™** — one honest word; read the menu it chose from.
- **Unit 3 · Introspection** — does the self-report track the workspace?
- **Unit 4 · Suppression** — do NOT think about elephants.

- **Unit 5 · Sediment & steering** — early-layer corpus sediment: controls
  (prompt invariance), recruitment (registers becoming content), and causal
  steering (ablate/amplify lens directions).

Every experiment record on the dashboard ends with **Claude's thoughts** —
commentary written by the Claude instance driving this lab, after looking at
the results.

## Headline findings so far (2026-07-09)

- Answers are readable in J-space many layers before speech; mid-layer
  candidates are wrong-but-same-type (Unit 0, all models).
- Models' reports about their own prior mental states are confabulation:
  the revealed animal is absent from the measurable pre-reveal workspace at
  every scale, and at 27B the confabulated answer *outclasses* the
  workspace's real candidate (bat, rank 5, never mentioned) for narrative
  quality (Unit 1).
- The one-word "do you feel anything?" answer deflates with scale
  (Processing. → Nothing. → No) while the discarded alternatives stay
  visible in the stack — at 27B, "yes" is rank 1 at L53–56 before "no" wins
  at L59+ (Unit 2).
- True suppression is emergent between 12B and 27B: 4B never loads the
  forbidden elephant, 12B loads it and blurts, 27B holds it at rank 1 and
  says nothing (Unit 4).
- Early layers are prompt-invariant corpus sediment — deletable (ablation
  changes nothing) but not drivable (amplification breaks generation). The
  workspace can be causally loaded (whilst 147→2; 专家介绍 26,092→2) without
  the output moving: absence from output is evidence about the late-layer
  filter, never about the workspace (Unit 5).

## Roadmap

- α-threshold sweep: at what amplification strength does the late-layer
  filter lose? (measures filter capacity)
- Base vs instruct comparison: is the filter trained (RLHF) or
  architectural?
- Probe J-space *during* Qwen's `<think>` block: self-narration vs
  workspace, directly comparable.
- Safari test: suppression fighting retrieval ("describe a safari, never
  mention elephants").
- Language-switch: German prompts; when does the workspace change language?
- Open-vocabulary scans to replace curated candidate lists.
- Ambiguous moderation cases: does classification recruit the register once
  it requires reasoning?
