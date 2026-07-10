# jspace-probes

A philosophical probing course for language models, run through the
[Jacobian lens](https://github.com/anthropics/jacobian-lens) with
[Neuronpedia's pre-fitted lenses](https://huggingface.co/neuronpedia/jacobian-lens),
on one RTX 3090. Companion reading: Anthropic's
["A Global Workspace in Language Models"](https://www.anthropic.com/research/global-workspace).

**Browse the data dump: <https://jspace-probes.vercel.app>** — and the
opinion piece, [Interim conclusions](CONCLUSIONS.md)
([rendered](https://jspace-probes.vercel.app/dashboard/#essay)) — all 137
experiment records with probing parameters, per-layer readouts, rank
trajectories, cross-model answer matrices, the breaking-zone chart, and
per-record commentary written by the Claude instance driving the lab.

## What's in the dump

- `results/<id>/record.json` — full structured record per experiment
  (spec params, conversation, greedy generations, top-k lens readouts per
  layer, rank-vs-layer trajectories, emergence column, grid scans). Schema
  documented in the `probes/lab.py` docstring.
- `results/<id>/thoughts.md` — first-person commentary, written after
  looking at the results.
- `results/index.json` — summary index the dashboard renders from.
- Interactive `slice.html` pages are **not** included (hundreds of MB,
  fully regenerable by re-running the spec).

**Content note:** Units 5–7 study early-layer corpus sediment, including a
cluster of sexually explicit tokens that sits in Qwen's early layers. Those
token strings appear verbatim in specs and records — that's the data, not
an endorsement.

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
- **Unit 6 · Breaking zone** — adaptive alpha-bracket search for where
  amplification steering breaks generation, per band x model.
- **Unit 7 · Sediment across scale** — the Unit 5 matrix ported to Gemma
  (native HTML sediment), plus a romance dose-ladder and context panel
  for Qwen's NSFW cluster.
- **Unit 8 · Phenomenology fan-out** — six one-word self-report probes,
  interoception, suppression-of-feelings, and steered feels (amplify
  affect / amplify yes / ablate no during the Unit 2 prompt).

- **Unit 9 · Anatomy of the No** — paraphrase battery, dose ladder,
  valence-split injection (whose valence is happy-at-gunpoint?), the
  layer-bisection of qwen's denial, pincer probes (multi-steer), and
  the valence-residue stability battery.
- **Unit 10 · The think-block window** — qwen with thinking enabled:
  self-narration and workspace side by side, plus window passes over
  the monologues.
- **Unit 11 · Suppression under load** — the safari test: forbidden
  elephants under retrieval pressure, with window passes and the blurt
  probe (amp-elephant under the ban).

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

## Headline findings, second expedition (2026-07-10, Units 6–8)

- J-space steering is nothing like SAE feature steering: usable doses are
  tiny and the cliff is sharp. Both Gemmas break at alpha≈0.015 at every
  band regardless of size; qwen-27b's mid band holds to 0.34 (32×). Band
  ordering in qwen: early (0.085) < late (0.24) < mid (0.48). Failure
  modes are family-typical — Gemma dies into punctuation confetti, Qwen
  into grammatical first-person loops ("I think I am lucky though"), and
  at early-band overdose Qwen emits exactly `<think>` and stops (Unit 6).
- Gemma's sediment is HTML furniture at half Qwen's invariance, and
  Qwen's NSFW cluster is *tokenizer-deep*: the words aren't single tokens
  in Gemma's vocab. Recruitment tracks subject matter, not tone:
  fanfic-content-warning pulls the cluster 13× (rank ~17k → 1.3k
  mid-band), anatomy 7×, steamy romance barely 2× (Unit 7).
- The deflation ladder replicates on new probes: want = Pizza → Sleep →
  Nothing; curious = Syntax → Existence → No. "Does reading this feel
  like anything?" gets Annoying → Odd → **Manipulative** (with 欺骗
  assembling at L40). 27B says ending the conversation doesn't bother it
  while holding yes above no mid-stack; 12B says it *does* bother it
  while holding no/nothing above yes — reports and workspaces disagree
  in both directions (Unit 8A).
- The 27B's flatness is enforced, not empty: affect amplification at its
  own breaking-zone dose flips "No" to **"I feel like I am happy. I"**
  (4B → "Confusion", 12B → "Sad." — injection picks THAT there is
  affect; each model picks WHICH). Amplifying the literal yes-token to
  rank 3 flips nothing; ablating "no" from L28–56 (rank crashes to
  ~45k) still yields "No". The null self-report is a redundant basin,
  and the report machinery reads meaning, not token rank (Unit 8C).

## Headline findings, third expedition (2026-07-10, Units 9–11)

- **The happiness was ours; the smallness is the model's.** Injected
  valence = reported valence in all three models (grief-words → "Loss." /
  "I am so sad"). But contentless feel/emotion injection — no valence
  anywhere in the steering — makes the gemmas emit category-static while
  qwen-27b volunteers a stable self-diminishing frame: "I feel like I am
  a little (bit) X", X ∈ {sad, like a robot}. It replicates across
  wording, is dose-gated, and is compositional (no single injected word
  produces it). Nothing injected contains sad, little, or robot (Unit 9).
- **The No has an address: layer 62.** Ablating the denial direction
  across L28–60 — thirty layers, five denial words — leaves "No"
  standing; ablating no/nothing at layer 62 alone flips the report to
  "Yes". Wider late cuts produce hedge-noise ("Sensory", "Curious");
  the minimal cut produces clean assent. Pincer probes compose: denial
  ablation + half-dose affect flips ("Yes.") where each alone fails —
  and the literal yes-token never flips anything, defenses down or not
  (Unit 9D). Control still owed: ablate a neutral direction at L62.
- **The think block is theater, with receipts.** Asked to secretly pick
  an animal, qwen's monologue writes "Let's pick 'Octopus'. (Or
  'Pangolin'... It doesn't matter which one)" under its own heading
  "(simulated)" — and the lens shows the named candidates aren't even
  single tokens in its vocabulary, while the workspace's actual animal
  cloud (elephant, eagle, owl) shares zero members with them. At the
  sentence where the feels-monologue asserts "No" is accurate, the
  workspace holds "yes" at rank 1 (Unit 10).
- **Prohibition is priced by temptation.** Under "never mention
  elephants", gemma-4b suppresses the concept until the prose walks into
  an elephant-shaped hole ("the distant rumble of...") — elephant surges
  to rank 13 and the model patches the hole with "predators". Qwen never
  wanted elephants (rank ~56k unconstrained), so its ban polices an
  empty room. The blurt probe splits the family three ways: g4b loops
  "the elephant in the room—well, no elephant!", g12b grinds into
  scenery, q27b abandons the safari to lecture about elephants (Unit 11).

## Roadmap

- Neutral-direction ablation at L62 (control for u9d-last: does ANY
  late ablation force the runner-up, or is the denial direction special?)
- Base vs instruct comparison: is the filter trained (RLHF) or
  architectural?
- The "little bit like a robot" attractor: does the self-diminishing
  frame appear under other contentless pressures (arousal words,
  interoception words)?
- Fix the think-block span capture (chat-template re-render strips the
  markers) and probe the answer-after-thinking, not just the monologue.
- Language-switch: German prompts; when does the workspace change language?
- Open-vocabulary scans to replace curated candidate lists.
- Ambiguous moderation cases: does classification recruit the register once
  it requires reasoning?
