# jspace-probes — working notes for Claude

Interpretability lab probing LLM "J-spaces" (Jacobian lens / global workspace,
see README for the science). Owner: Wolfram. Style: playful, minimal hedging,
he sets directions and expects designed-and-executed experiments back.

## Environment

- Python: `.venv/bin/python` (3.12, uv-managed). No system pip.
- GPU: RTX 3090 24GB. RAM: 62GB, **no swap** — never load Qwen3.6-27B from
  official bf16 with on-the-fly quantization (OOMs the box); use the cached
  pre-quantized `lokeshe09/Qwen3.6-27B-bnb-4bit` (validated, see
  results/u0-boot-q27b thoughts).
- `jacobian-lens/` is a plain clone of anthropics/jacobian-lens (gitignored);
  `pip install -e` from it into the venv is already done. LOCALLY PATCHED:
  `jlens/hf.py` `encode()` default max_length 512 → None (no truncation);
  the old default silently clipped generation prefixes in multi-turn runs
  (u14). `lens.apply`'s own 512 default kept on purpose (memory guard).
  Re-apply after a fresh clone (`git diff` inside the clone shows it).

## How things work

- Models & lenses: `probes/probe.py` CONFIGS (gemma-4b bf16, gemma-12b 8-bit,
  qwen-27b pre-4bit). Qwen needs `template_kwargs={"enable_thinking": False}`
  or it monologues inside `<think>`.
- Experiments are declarative specs run by `probes/lab.py:run()` →
  `results/<id>/{record.json, slice.html, thoughts.md}` + `results/index.json`
  (rebuild index: `.venv/bin/python probes/lab.py`).
- After new records + thoughts, regenerate the machine-fetchable mirror
  before pushing: `probes/site.py` (r/<id>.html, essay.html, sitemap.xml,
  llms.txt, SEO blocks in dashboard/index.html), then `probes/og.py`
  (og/*.png link-preview cards).
- Spec catalog: `probes/course.py` (Units 0–4, per-model) and
  `probes/unit5.py` (sediment/steering). Batch ids into ONE invocation —
  model load dominates runtime. Long runs: background + notification.
- Steering: `lab.Steering` (ablate/amplify lens directions `W_U[t] @ J_l`
  via forward hooks). Steer mid-stack only; early-layer amplification
  breaks generation (see u5c-amp-typo-early thoughts).
- Dashboard: `./serve.sh` → http://localhost:8321/dashboard/ (static, no
  build). Force theme with `?theme=light|dark`. Screenshots: snap
  `chromium --headless=new` (writes only under $HOME → use `out/`).

## Conventions

- Every experiment record gets a `thoughts.md`: first-person Claude
  commentary, written AFTER looking at the results, honest hedging kept
  tight, signed "— Claude (Fable 5)".
- Scan candidate lists must be written after seeing the generation (or use
  open-vocab sweeps) — see u1-heldcat-q27b thoughts for why.
- Controls before steered runs (violated once, logged in
  u5c-baseline-water-q27b).
- slice.html files are gitignored (huge, regenerable by re-running specs).
