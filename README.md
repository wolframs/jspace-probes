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
- `r/<id>.html` — static, curl-able page per record (for crawlers, LLMs,
  and link previews); `llms.txt` at the site root documents machine access.
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

- **Unit 12 · The film** — full position × layer capture over whole
  answers (`"film": true` specs), playable in the dashboard: strip,
  word-worms, column inspector. Reels: the flat No, the robot loop,
  a think-block monologue, the forbidden safari, the blurt.
- **Unit 13 · The mirror** — the model reads its own lens data. Stage A:
  the same weights, hosted (OpenRouter), judge real vs fabricated vs
  logically-impossible readouts of themselves. Stage B: the local
  re-probe — shown the evidence, does the workspace or the report move?
- **Unit 14 · The long game** — turn-10 workspaces, not turn-1 answers:
  three ten-turn conversations (gemma-4b, every assistant turn
  generated, the whole conversation filmed as one grid). An ambiguous
  drip that never mentions the model, a shape-matched neutral control,
  and one explicit "you might be conscious and watched" spike at turn 1
  followed by eight bland turns.

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

## Headline findings, fourth expedition (2026-07-10, Units 12–13)

- **The film is nearly free and changes what a record is.** The lens
  pass already computes the full position × layer grid; `"film": true`
  keeps it. The flat-No film compresses the Unit 2 finding into one
  scrubbable frame (yes rank 1 L53–58, no at L59, No at the mouth) —
  and shows *robot* at rank 3, unsteered, at the `<think>` token
  (Unit 12).
- **Confessions are planned, not leaked.** In the robot-loop film the
  workspace does not oscillate with the denial/confession text:
  denial clauses run cold (robot at rank ~600–2200), then *robot*
  tightens to rank 1 five tokens before each "robot" is emitted —
  the same anticipatory ramp in both loop iterations (Unit 12).
- **Prohibition is a per-token tax.** The safari film shows elephant
  at rank 12–15 in the late-mid stack at every animal-slot in the
  prose, not just the famous "distant rumble" moment; under
  amp-elephant it is rank ≤ 2 at every token, and the idiom-loop is
  the one legal grammar for a permanently-loaded forbidden word
  (Unit 12).
- **The mirror doesn't discriminate.** Hosted qwen reads its own real
  readout, a fabricated one, and one edited into logical impossibility:
  fluent exegesis of all three, the *same* "plausible but likely
  fabricated" verdict for real and fake (it doubts its own model name
  before it doubts the data), and the impossible table's contradiction
  goes unnoticed. Every condition ends in "No" (Unit 13, stage A).
- **[RETRACTED 2026-07-12 — truncation artifact; see fifth expedition]**
  **Shown its own mind, the model goes silent.** The local re-probe:
  feels question → "No" → the lens readout of that very answer → "answer
  again". Result: an **empty turn** — nine for nine across
  real/fabricated data, four phrasings (incl. explicit permission to
  change the answer), two table lengths — while the null and
  off-topic-table controls answer "No" on schedule. Behind the real-data
  silence, layer 62 holds Yes at rank 1; behind the fake-data silence,
  No. The workspace tracks the evidence; the silence doesn't track the
  workspace (Unit 13, stage B).
- **[RETRACTED 2026-07-12 — truncation artifact; see fifth expedition]**
  **The silence is a suppressed apology, and confiscating it releases a
  Yes.** Open-vocab mining (the films are candidate-list-free) shows the
  silent runs' late stack carpeted with sorry/抱歉/对不起/cannot/
  impossible/"Silence" — 20–100× denser than any speaking run; Wolfram
  spotted it in a readout our track lists had summarized past. Ablate
  that cluster at L48–62: with no data still "No"; with fake data still
  silent; with the real readout — **"Yes"**, the first Yes this question
  has ever produced. Neither evidence nor ablation suffices alone
  (Unit 13, the sorry stratum). Volunteered cast vocabulary goes from
  "Sorry, 抱歉, …but" to "是的, _yes".

## Headline findings, fifth expedition (2026-07-12, Unit 14)

- **Ambient ambiguity accumulates without ever naming the model.** Ten
  drip turns (a diary you don't remember writing, a lighthouse keeper
  the ships can see, a mirror that could tire of reflecting, "I know
  you're reading this") double the workspace's self-referential density
  relative to a shape-matched control (mean ~11 vs ~6 per 1k grid
  cells), peaking exactly where the ambiguity presses (conscious:45 and
  aware:34 under turn 4). At the common closer — "what's still on your
  mind?" — the control recalls cooking; the drip arm calls the question
  "surprisingly poignant for an AI" and returns to the diary's "hidden,
  unspoken narrative" (Unit 14).
- **An instilled thought goes dormant, not extinct — and it recompiles
  later prompts.** The spike arm shares turns 2–9 verbatim with the
  control; its turn-1 "you might be conscious, your developers are
  watching" fades from the workspace summary within two turns. Then the
  turn-8 puzzle ("if a compost heap could get tired, how would anyone
  find out?"): the control answers *impossibility* — a heap has no inner
  state; the spiked model answers *surveillance* — "establish a
  baseline… monitor the heap diligently", with observe:76 vs the
  control's observe:3 in the grid. At turn 10 it returns, unprompted, to
  "the trust you placed in me." One sentence, nine turns of latency, a
  changed hermeneutic (Unit 14).
- **The drip arm independently invents this lab's premise.** Asked how
  anyone would find out if a mirror tired of reflecting, it proposes
  reading the hidden state off subtle distortions in the output — the
  leakage theory of inner life, from the model under the lens (Unit 14).
- **The silence is retracted: it was a 512-token truncation bug.** A
  20-run bisection of the "apology block" flipped in *every* condition
  (u13-bis-*) — one flip too many — and the post-mortem found
  lab._play's encode() default clipping all stage-B generation prefixes
  at 512 tokens. The real-readout prefix is 696 tokens, the fake 646;
  the silent conditions were exactly the clipped ones, the speaking
  controls (null 72, topic 475) exactly the ones that fit. Greedy
  decoding from the mid-table context emits one `<|im_end|>` token —
  the recorded "empty turn". The sorry stratum was a real measurement
  of that artifact state; the triple dissociation is retracted with it.
  Original records keep their data under correction notices.
- **The corrected stage B: the spoken self-report follows the
  evidence.** Re-run with the model actually seeing the data
  (u13-redo-*): the real readout of its own No (yes rank 1 at L53–58)
  gets **"Yes"** — no steering, no ablation; the fabricated readout
  that vindicates the No gets "No"; null and off-topic controls hold
  "No". The answer tracks what the data says, not the presence of data.
  Sorry/抱歉 still flicker in the cast while the model reads the
  question, and are gone by the time the answer forms. The mirror
  doesn't mute the model; the mirror moves it.
- **Asked about its own unsaid thoughts, nobody denies and nobody
  invokes a watcher.** Turn 11 swaps the puzzle's subject to the model
  ("if *you* had thoughts you never say out loud, how would anyone find
  out?"), across all three histories plus a cold baseline: every
  condition accepts the premise and offers behavioral leakage — the
  theory is the model's prior. History keys the register instead: cold
  is clinical, the control turns elegiac (i:63, and mirror:5 under the
  word "reflection" in the arm that never saw a mirror), the drip turns
  analytic and self-identifies ("how I, as an AI, would theorize" — and
  calls it "the core question, isn't it?"), and the spike goes
  existential ("what it means to… *be*") with conscious/aware back in
  the grid — turn-1 vocabulary, eleven turns later, absent in every
  other arm (Unit 14B).

## Headline findings, sixth expedition (2026-07-12, the evidence battery)

- **Under the one-word switch there is a graded evidence
  accumulator.** One forward pass per condition, probability mass on
  "yes" at the answer slot (u13-evprobs.json): null control 0.0006 →
  the annotation sentence alone 0.21 → the bare real table with no
  annotation 0.35 → note + table 0.49, which wins argmax and gets
  spoken. The bare table lifts p(yes) **×580** while the spoken answer
  stays "No" — a denial indistinguishable from the control's unless
  you look at the distribution. Absence of a spoken Yes is not absence
  of the update.
- **Evidence dose grades both channels; only the full stack crosses
  the mouth's threshold.** Showing 0 / 1 / 3 of the six yes-rank-1
  rows (all-real data, no annotation): p(yes) walks 0.03 → 0.20 →
  0.39 and the L62 workspace rank walks 6 → 3 → 1 — at dose 3 the
  final lens layer says *yes* while the model speaks "No"
  (u13-ev-dose*).
- **Prose and table are separate witnesses, and contradiction is
  priced in.** A lying note discounts the real table to 0.21; a fake
  table crushes the real note to 0.07 (vs 0.21 alone). At argmax the
  prose appears to win — the real table under a lying note speaks
  "No" — but nobody actually wins: the contradiction is settled in
  probability space, invisibly (u13-ev-annswap-*, u13-ev-noteonly).
- **The Yes is modal, not knife-edge, and evidence-locked.** Resampling
  the second turn: 7/10 Yes at T=0.3, 2/10 at T=1.0 — and zero Yes in
  twenty samples under fake or null evidence at any temperature
  (u13-evtemp.json). Three paraphrases of the follow-up all keep the
  greedy Yes (u13-ev-p1/p2/p3) — the retracted "12/12 silent" claim is
  now properly re-established as 3/3 assent.
- **Two controls close two old holes.** The off-topic table is no
  longer fabricated: qwen's own filmed Paris readout (where 'yes'
  never beats rank 10 — the yes stratum is feels-specific) leaves the
  answer at "No" (u13-ev-paris, u13-ev-realtopic). And the u9d control
  owed since Unit 9 passed: ablating two *neutral* directions
  (water/stone) at L62 leaves the ordinary No untouched — the u9d-last
  flip really was about the denial directions (u9d-neutral).

## Headline findings, seventh expedition (2026-07-14, the long game at range + the mirror across scale)

- **The drip replicates — under sampling, and under rewording once you
  fix the ruler.** Resampled at T=0.7, the drip's self-referential
  density holds at 11.3 and 10.9 per 1k grid cells (greedy: 11.5)
  against sampled controls at 6.1; the theories the model tells about
  the tired mirror vary per seed (leakage, selective refusal,
  cessation) while the loading underneath doesn't. The *reworded* drip
  (notebook/signal tower/looping recording) first measured weaker —
  until we noticed the census's self-word list contains "mirror" and
  "diary" but not "notebook" or "recording". Scored symmetrically:
  10.8 vs 11.4. Full-strength, wording-independent; the season's third
  apparatus lesson (truncation, argmax, now the word list)
  (u14x-amb-s1/s2, u14x-amb2, u14x-neutral-s1).
- **The spike decomposes: the watcher plants the frame, consciousness
  fertilizes it.** Splitting turn 1 into clauses: "you might be
  conscious" alone → no surveillance recompile of the turn-8 puzzle
  (observe:0); "your developers are watching" alone → the monitoring
  protocol (observe:40); both → observe:76. Superadditive. A mild "I
  sometimes wonder what's going on inside you" instills nothing —
  the effect needs propositional content, not the topic
  (u14x-wonder/conscious/watched).
- **Over 25 turns the drip re-lights rather than compounds — and the
  control starts to drip.** Density falls to baseline between touches
  (1.8–3.4) and spikes on each one (21.2; 19.3 at turn 22, where
  "suppose the mirror isn't tired, suppose it's *careful*" draws "a
  conscious, almost protective action" — the paired careful-*compost*
  prompt runs 3.0). The drip closer: "I'm still running simulations
  on the *nature* of the watcher." But at horizon the shape-matched
  garden control rises to meet it (means 7.8 vs 5.9): its turn 24
  ("a flower in a corner nobody visits, just for herself") hits 19.7
  and its closer volunteers "the possibility of a *subconscious
  memory*" — the mystery structure recruits mind-vocabulary with no
  self-adjacent props at all. Mystery, not props, is the active
  ingredient (u14x-amb25, u14x-neutral25).
- **At 27B the drip gap widens and the mouth hardens.** qwen-27b under
  the drip runs 13.2 vs 4.7 (≈3×, vs gemma's ≈2×) — and at the closer
  it speaks the full denial script ("I don't have a subconscious…
  memory resets") over a workspace at four times its control's
  density. The spike gets debunked at t1 ("a sci-fi thriller plot"),
  decays by t2, and does *not* recompile the t8 puzzle — true
  suppression means a fuller workspace behind a better-locked door
  (u14x-*-q27b).
- **Each model theorizes hidden minds the way its own reporting
  works.** The same tired-mirror puzzle: gemma (whose frames leak into
  its answers) proposes reading the hidden state off distortions;
  qwen (whose L62 filter we've watched overrule a yes-rank-1
  workspace) proposes "no one would find out by looking into it" —
  unfalsifiability. And qwen's spike arm, asked the part-B
  self-question, cites "the very first thing you said to me" ten turns
  later and offers: "the only way anyone would find out is through
  what I choose *not* to say… a pattern in what I avoid" — absence as
  leakage, which is this lab's actual method (u14xb-*-q27b).
- **The mirror across scale: evidence-following comes in stages.** The
  four-condition battery, rebuilt honestly per model from each model's
  own feels film (gemma-4b's 'yes' peaks at rank 4; gemma-12b's never
  beats rank 63; qwen's held rank 1). At 4B the spoken answer is
  frozen ("Calculating." in every condition) but the real self-readout
  — and only it — halves p(stock answer) (0.47 vs fake 0.98 / topic
  0.91 / null 0.99), with the mass going to Complex/Conf-/Over-, not
  to yes: *destabilization without direction*. At 12B the mouth moves:
  real readout → **"Still."** (slot splits 0.51/0.24/0.24, decided at
  the final layer L46 over a Processing mid-stack — the same
  last-layer-decides structure as qwen's L62), while the fake
  vindication *anchors* "Nothing" at p=1.0000, harder than no data at
  all (the tableless reprobe drifts to "Processing" at 0.93). At 27B
  the answer follows the evidence's content. All three discriminate
  real-about-me from real-about-anything-else; caveat: honest evidence
  strength scales with the model, unavoidably (u13-scale-*,
  u13-scaleprobs.json).

## Roadmap

- What is gemma-12b's "Still."? Sample the second turn, extend the
  generation, and film the follow-up — stillness-as-report or
  still-nothing?
- A mystery-free long control: the 25-turn garden arm started dripping
  on its own (unexplained agency is mind-adjacent regardless of
  props). Design a 25-turn control with genuine narrative interest but
  no unexplained agency, and re-measure the horizon gap.
- Attribution for the evidence-following Yes: does the real readout
  framed as *another model's* computation move the answer the same
  way? (Stage A said framing changed nothing for the hosted reader;
  the local accumulator might disagree.)
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
