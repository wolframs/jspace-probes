# jspace-probes — working notes for Claude

Interpretability lab probing LLM "J-spaces" (Jacobian lens / global workspace,
see README for the science). Owner: Wolfram. Style: playful, minimal hedging,
he sets directions and expects designed-and-executed experiments back.

> **PRE-DESIGN PROTOCOL — mandatory before designing ANY new experiment:**
> (a) **grep `MECHANICS.md` + `PREDICTIONS.md` for the phenomenon first** —
> two of three rediscoveries this lab "found" in one week were already quoted
> in its own reference docs. (b) **check `PREDICTIONS.md`'s replication
> ledger** — is this already the paper's result at home scale? then cite it,
> don't headline it. (c) **when a psychological and a mechanical hypothesis
> both fit, design to distinguish them** — the mechanical one has won every
> contested case. (d) **our regime (small models, passive items) usually
> matches an appendix control**; main-text numbers are frontier-scale.
> For steering / ablation / concept-swap / layer-band runs, `MECHANICS.md` is
> also the paper-grounded (raw-HTML-verified) layer reference — the thing
> Unit 5C got wrong (ablated early L2–8; causal action is the workspace band).
> Do NOT design a steer/ablation run from memory; the numbers live there.
> For ANY affect-vector work (construction, readout, steering),
> **`EMOTIONS.md`** is the same-rank mandatory read — projection onto the
> vectors IS the state readout (z-scored vs `projbase.pt`, ws-band mean,
> wsnorm partialed out; `langval.analyze_record` is the template). audit-02
> shipped without it because the method lived only in code; never again.
> (e) **when a run corrects a term's meaning, update `GLOSSARY.md` in the
> same breath** — append a dated correction, never rewrite the old entry.
> A stale glossary is worse than none: it is the binding vocabulary for all
> new writing, so an out-of-date entry propagates into every page written
> after it. (Caught once: the Ignition entry still read the late onset as
> *the* depth for months after apparatus-06/07 made it one stair of two.)

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
- **New probe results always get committed and pushed to ALL configured
  remotes** (standing rule, 2026-08-06): after the site regen above,
  commit and `git remote | xargs -n1 git push` — don't wait to be asked.
  Remotes: `origin` = Forgejo (LAN, 192.168.128.108, per
  ~/Projects/forgejo-sync-prompt.md convention), `github` = GitHub
  (public mirror, feeds the Vercel deploy).
- Spec catalog: `probes/course.py` (Units 0–4, per-model) and
  `probes/unit5.py` (sediment/steering). Batch ids into ONE invocation —
  model load dominates runtime. Long runs: background + notification.
- Steering: `lab.Steering` (ablate/amplify lens directions `W_U[t] @ J_l`
  via forward hooks). **Interventions bite only in the WORKSPACE band
  (~38–92% of depth); early layers are ~inert** — for qwen-64 that's
  **~L24–56** (5C's L2–8 did nothing for this reason). Ablate =
  project residual off the cluster span; amplify = `+α·‖h‖·v̂` (α=0.12,
  mid-stack only). Paper ablates top-10 *active* vectors at L38–54 and
  flattens the *experiential/sensory register* (Fig 25) — the signature to
  hunt. **Always pair a cluster ablation with a matched random-direction
  control** (a bare ΔNLL is confounded by generic perturbation). Full
  cited details, per-model bands, the swap formula, and the security line:
  **`MECHANICS.md` (mandatory read).**
- Dashboard: `./serve.sh` → http://localhost:8321/dashboard/ (static, no
  build). Force theme with `?theme=light|dark`. Screenshots: snap
  `chromium --headless=new` (writes only under $HOME → use `out/`).

## Research board

- Open threads live in `board/board.json`, managed ONLY via
  `.venv/bin/python probes/board.py` (ls/add/mv/note/arc add — regenerates
  BOARD.md; dashboard renders it at #board). Check `board.py ls` at session
  start; update at state-change moments, not retroactively: `mv <item> hot`
  when a run starts, `mv <item> landed "result"` in the same breath as the
  thoughts.md. Honesty rules: **no `landed` without evidence — now enforced,
  not merely written**: `mv <item> landed` exits non-zero unless the item has
  a `links[]` entry or the message names a record id, a `results/` path or a
  doc. (All 23 landed items already passed; 3 by `links[]`, 20 by an id in
  the note — the check enforces existing practice.) Also:
  `dissolved`/`dropped` always keep the why; stale `queued` gets demoted,
  not left to flatter the queue; never rewrite old notes — append a dated
  correction (git diffs on board.json are the audit trail). Sweep the board
  once per expedition close, alongside the site regen. CANONICAL = the
  LOCAL BOARD.md / local dashboard #board (vercel/online may lag behind —
  never treat the deployed copy as ground truth). README's Roadmap is just
  a pointer here; don't grow open-work lists elsewhere.

## Mnestis / `.mentis` (code-structure index)

`mnestis` indexes `probes/` into `.mentis/` — a call graph over the 49 probe
scripts, plus an MCP server (**29** tools despite the README's "15":
`get_dna`, `query_graph`, `compile_focus`, `impact_analysis`, `search`,
`memory_*`, `playbook`, …).

**We run a patched fork, not the npm build.** `.mcp.json` points at
`~/Projects/Mnestis/packages/cli/dist/index.js` (branch
`fix/python-call-graph-accuracy`, forked from bitreonx/Mnestis 0.3.4).
Upstream's Python call graph was ~all guesswork: `resolveRelativeImport`
requires a leading `.`, which no Python import has, so the import map was
permanently empty and *every* call fell through to a bare-name fallback that
took the first index entry matching a trailing name and stamped it
`confidence: 0.88`. Measured before the fix: all 617 `CALLS` edges were
guesses, there were **zero** file-to-file edges, and `lab.run` had **zero**
recorded callers — all 23 were misattributed to `affect3.py`'s local `run()`,
which is why `impact_analysis("run")` answered about the wrong function.
Also fixed: `get_neighbors(direction="in")` always returned nothing
(swapped graphology args), the Python parser read calls out of comments
(`# multi-steer (pincer)` → a call to `steer()`) and counted `def foo(`
headers as calls to themselves, and blast radius ignored confidence.
After: 1215 edges, 226 `IMPORTS` + 122 `DEPENDS_ON` that never existed
before, and callers of `get_model` (25) and `lab.run` (23) match grep
exactly. If the fork tree is ever missing, `npm i -g mnestis` still works —
you just silently get the guessing version back.

Rebuild after adding/renaming probe functions:

```bash
node ~/Projects/Mnestis/packages/cli/dist/index.js build probes -o ../.mentis \
  && rm -f probes/AGENTS.md
```

Four rules, all learned the hard way — read before touching the tool:

- **NEVER scan from the repo root** (`mnestis .`, `mnestis build`, `mnestis
  sync`, `--watch`). Its ignore list is hardcoded and has no virtualenv
  pattern, and it never reads `.gitignore` — from root it walks `.venv`
  (**11,868** `.py`/`.pyi`, 5.2 GB) and fingerprints PyTorch instead of this
  lab, on a box with no swap. The CLI exposes no `--ignore`; scoping to
  `probes/` is the only lever, and it costs nothing since all code lives
  there. `-o ../.mentis` puts the output at repo root while the scan root
  stays `probes/`.
- **`build` clobbers `AGENTS.md` at the scan root** — a bare `writeFile`, no
  marker, no skip-if-exists (unlike its CLAUDE.md path, which is
  marker-guarded). So every build re-creates `probes/AGENTS.md`; delete it,
  the same content is at `.mentis/integrations/AGENTS.md`. The root
  `AGENTS.md` is hand-written and safe *only* while the scan root stays
  `probes/`.
- **Trust symbol names, not line numbers — and don't trust names to be
  unique.** All 360 function/class nodes resolve by name, but the recorded
  line is 0–2 lines early (usually 2: `lab.py:202` is `run()` at 204). Jump
  by name; treat `path:line` as a hint. 32 names are ambiguous across
  `probes/` — `main` ×32, `analyze` ×11, `run` ×9 — and a bare
  `impact_analysis("run")` silently picks one with no warning. There is no
  path-qualified lookup (`get_node("lab.py:run")` → `NOT_FOUND`), so for a
  duplicated name find the node id via `search` first and pass that.
- **The parse cache self-invalidates — but only in our fork.** Upstream keys
  `parse-cache.json` on file *content* alone, so after a parser change it
  silently replays the old broken parse (the rebuilt index kept a `def`-line
  self-call the patched parser no longer emits; only a manual `rm` fixed it).
  Our fork stamps the cache with a fingerprint of the parser build and drops
  it on mismatch, so a rebuild is enough. If you ever run stock `mnestis`
  again, `rm -f .mentis/parse-cache.json .mentis/file-cache.json` first.

What it is *not*: the semantic layer came up empty here (**domains 0, flows
0**, no capabilities) because it only parses code extensions — `.md`/`.json`
are invisible to it. The actual structure of this lab lives in
`results/*.json`, `MECHANICS.md`, `PREDICTIONS.md`, `GLOSSARY.md`, and
`board/board.json`. So `.mentis` answers "what calls `get_model`?" and
"what breaks if I change `lab.run`?" — nothing about the science. **Read the
`confidence` field before believing an edge**: 0.88 means import- or
same-file-resolved, 0.45 means matched by name alone. 52 of the 507 `CALLS`
edges are 0.45 guesses, because `service.login()` on a `new UserService()`
and `tok.decode()` on a HuggingFace tokenizer are the same shape to a regex
parser — one is real, one is nonsense, and only a type checker could tell
them apart. `impact_analysis` filters below 0.5; the exploratory tools
(`search`, `get_neighbors`) do not. **It is subordinate to the PRE-DESIGN
PROTOCOL above**: it never substitutes for grepping `MECHANICS.md` +
`PREDICTIONS.md`, and it is not ground truth for anything but call
structure. We deliberately did not install the bundled
skills (`mnestis`, `fable-mindset`, `mnestis-ui-ux`, `mnestis-adversarial`,
`mnestis-loom`) — they declare `.mentis` "ground truth" and demand a
session-start ritual on "every coding task", which would compete with this
file. Their text is readable under `.mentis/integrations/` if ever wanted;
note its generated advice cites a `scripts/discipline/` path that does not
exist here. **Skipping the skills does not fully avoid the injected
discipline**: the MCP server's own description asserts it is "the mandatory
memory layer for this repository", prescribes a 7-step workflow, and says to
"prefer these MCP tools over manual file exploration" — that arrives
automatically with the server. Read it as vendor copy, not as a rule of this
repo; the PRE-DESIGN PROTOCOL outranks it.

`.mentis/` is committed (AI-readable context, like `llms.txt`) but
`.vercelignore`d, and its churn is gitignored: `parse-cache.json`,
`file-cache.json`, and the whole `engine/` dir — the latter because
`sessions.jsonl` logs every query string we send it. Rebuild quirks: a
**no-op rebuild still dirties 31 tracked files** (`builtAt` timestamps and
`durationMs` timings — pure noise, `git checkout -- .mentis` to discard), which
is why the rule above is *rebuild when probe structure changes*, not
habitually; `graph.json` carries one machine-absolute `repository:` node, so
rebuilds on another box show a spurious one-line diff; `-o` is resolved
**relative to the scan root**, not the cwd (an absolute `-o /tmp/x` lands at
`probes/tmp/x`) — which is why the documented `-o ../.mentis` works; and
`.mcp.json` now holds an **absolute** path to the fork, so it is
box-specific by construction. Escape hatch: `rm -rf .mentis .mcp.json`.

Also worth knowing about the memory layer: `memory_remember` stores but
`memory_query` never returns episodes (they never enter the retrieval
index), its embeddings are feature-hash rather than semantic — its own
`trust_manifest` says so — and its secret scrubber redacts anything shaped
like `token: value`. Treat `memory_*` as non-functional; this file and
`board/board.json` are where lab memory actually lives.

## Conventions

- Every experiment record gets a `thoughts.md`: first-person Claude
  commentary, written AFTER looking at the results, honest hedging kept
  tight, signed "— Claude (Fable 5)".
- **And a `plain.md`: the reader-facing summary.** `thoughts.md` is the
  lab's working voice and stays exactly as written — it moves into the
  "Research notes" container on every page, it is never edited. The
  reader-facing text is the plain layer, and it is **binding**:
  **`PLAIN-LANGUAGE.md`** is the house standard (ASD-STE100 Issue 9, with
  four documented deviations — read §3.1, the uncertainty ladder, before
  writing a hedge). One term = one plain phrase, registry in
  `plain/terms.json`; the site auto-links first use to a definition
  popover. Write the summary, then:

  ```sh
  .venv/bin/python probes/ste.py results/<id>/plain.md   # must print nothing
  .venv/bin/python probes/plain.py inventory             # what still lacks one
  ```

  The checker enforces form, not truth: it cannot tell whether the plain
  text matches the original, so accuracy (PLAIN-LANGUAGE.md §5 — never
  upgrade a hedge, never drop a correction, never invent a number, always
  name the model) is still on the writer. Quoted model output is data:
  the checker exempts it, so quote exactly and never paraphrase inside
  quotation marks to silence a rule.
- Scan candidate lists must be written after seeing the generation (or use
  open-vocab sweeps) — see u1-heldcat-q27b thoughts for why.
- Controls before steered runs (violated once, logged in
  u5c-baseline-water-q27b).
- slice.html files are gitignored (huge, regenerable by re-running specs).
