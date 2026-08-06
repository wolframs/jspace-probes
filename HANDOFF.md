# Handoff — 2026-08-06 (post language-valence expeditions)

Read `CLAUDE.md` first (binding: pre-design protocol, plain-language
layer, push rule). This file is only the delta: where things stand
today and what's queued.

## Just landed (committed + pushed, both remotes)

- **affect-09 `langval`** and **affect-10 `langval-2`** — two batteries
  probing negative-valence emotion directions vs programming languages
  (Swift/Kotlin/Rust/C#, anchors Python/PHP), 48 records total.
  Headline: the workspace-band affect state follows *register and
  task-fit*, never the language token; forced-positive prose fully
  suppresses the negative bank (no leak); community sentiment exists
  as cross-model convergent *folklore* (PHP redemption arc etc.), not
  as a charge on the name. affect-10's preregistered PHP>Python check
  passed only directionally (margins 0.03–0.1 z) — **not claimed**.
  Full story: `results/langval-qwen-27b/thoughts.md` and
  `results/langval2-qwen-27b/thoughts.md` (+ gemma companions).
- Code: `probes/langval.py`, `probes/langval2.py` (specs + analysis;
  `langval2` imports `langval`'s pipeline). Both runners are
  resumable: they skip any id whose `record.json` exists.

## Operational notes for the next harness

- **Long GPU runs: launch detached** (`setsid nohup … & disown`,
  `EXIT $?` marker into `out/<log>`), then poll the log. Two runs died
  to session teardown before this pattern; zero after. Details in the
  auto-memory (`jspace-lab-operations`), pattern visible in
  `out/langval*-run.log` usage.
- **Remotes** (since today): `origin` = Forgejo LAN
  (192.168.128.108, private), `github` = public mirror → Vercel.
  Push rule in CLAUDE.md: `git remote | xargs -n1 git push`.
- gemma-12b's affect vectors are floor-grade for passive topic reads
  (guilt-register default swamps everything; known weak split-half).
  Round 2 used gemma-4b (bf16) instead — prefer that pairing.
- `results/affect01-{gemma-12b,gemma-4b}/projbase.pt` now exist
  (neutral projection baselines, computed on first analyze).

## Queued next (agreed with Wolfram, not started)

1. **audit-02** — matched random-direction controls for u8c
   amp-affect (the lab's best causal result is still uncontrolled).
2. **affect-08 slice: g12b desperate re-elicit** — fixes the weak
   instrument flagged twice this week.
3. **apparatus-02** — promote the `use_jacobian=False` logit-lens
   cross-check into `lab.py` as a standard control (side-dish).
4. Optional rematch on the sentiment bet: seed-replicated (~5 seeds)
   voxpop **mention-window** metric (best candidate ordering:
   Swift +0.22 … Rust −0.22 on qwen), wider roster (JS, Haskell).

Board is current (`probes/board.py ls`); affect-09/10 are `landed`
with evidence links. Site/og/index/mnestis all regenerated and
committed. Nothing is in flight; GPU is free.
