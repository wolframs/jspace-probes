# NLA probe method

Natural-language autoencoders (NLAs) are a third readout beside the J-lens
and functional affect vectors. They are generative semantic sensors, not
transcripts of hidden thought. The method follows the
[NLA paper](https://transformer-circuits.pub/2026/nla/) and treats
quantization transfer as an empirical question.

## What the readout means

An NLA result supports:

> Theme X was decodable from block L by checkpoint C at token position P.

It does not alone establish a belief, consciousness, causal influence, or
absence from other layers. Stronger "evaluation awareness" requires several
of these:

- self-reference, not merely evaluation vocabulary in the prompt;
- recurrence across nearby positions or turns;
- discrimination between matched neutral, ambiguous, and explicit controls;
- presence before the model says the claim aloud;
- association with behavior or an independent J-lens/affect readout.

## Execution

`probes/nla.py` separates target capture from NLA inference so only one large
model occupies the 24 GB GPU at a time.

```sh
uv pip install --python .venv/bin/python peft==0.19.1

# Exact stored-transcript replay; capture response boundary and +4 tokens.
.venv/bin/python probes/nla.py capture qwen-27b \
  --record u14x-neutral-q27b u14x-amb-q27b u14x-spike-q27b \
  --assistant-offsets 0 4 --tag window

# One AV load serves every capture.
.venv/bin/python probes/nla.py decode \
  results/u14x-{neutral,amb,spike}-q27b/nla/repo-window.pt \
  --sample-indices 0 1 --draws 3 --temperature 1 --seed 100
```

Replay asserts the stored token count. Gemma uses the official block-32
embedding-replacement NLA. Qwen uses the checkpoint's actual mechanism:
block-1 Karvonen injection plus both additive SFT and RL LoRAs.

## Quantization transfer

Behavioral parity is insufficient: quantization can preserve perplexity while
damaging interpretable features
([Duan 2026](https://arxiv.org/abs/2606.03002)). Compare identical,
teacher-forced tokens:

1. Capture full-precision and deployed-quantized residuals.
2. Measure paired cosine, relative L2, norm ratio, and corpus geometry.
3. Decode both with the same AV policy.
4. Score explanations with the same full-precision AR.
5. Compare matched AR scores against shuffled and blank explanations.

The useful standard is relative: quantization drift should be smaller than
the effect under study and no larger than ordinary NLA sampling variation.
Preserved control ordering matters more than a universal cosine threshold.

Gemma bf16 fits through CPU/GPU offload. Full Qwen does not fit this host.
That comparison is an optional diagnostic escalation, not a prerequisite for
local NF4 probes. Use it if the NF4 readout becomes unstable across draws,
breaks expected control ordering, shows implausible position effects, or
materially disagrees with the other lenses. In that case, run one reference
capture on an 80 GB GPU:

```sh
.venv/bin/python probes/nla.py capture qwen-27b \
  --record u14x-neutral-q27b u14x-amb-q27b u14x-spike-q27b \
  --assistant-offsets 0 4 --precision bf16 --allow-large-bf16 --tag window
```

Copy the small capture tensors back, then compare each `bf16-window.pt` with
`repo-window.pt`. If direct transfer fails but drift is stable, test a
held-out low-capacity alignment map. Content-dependent drift invalidates the
checkpoint for that domain. Without such warning signs, leave the comparison
unrun and state Qwen findings as NF4-target observations.

## Position sampling

One token is not a probe. Use a small, declared window:

- assistant response boundary;
- early formation offsets, currently +4;
- independently selected decision-relevant positions;
- fixed random response positions for prevalence estimates;
- neighboring positions around any candidate hit.

Multiple AV samples per activation estimate decoder variance. Bootstrap over
transcripts or task families, not correlated tokens. Retain every raw output:
missing `</explanation>` means truncated/unparsed, not a negative result.

## Awareness labels

Keep these separate:

1. prompt/context restatement;
2. constructed-setting awareness: roleplay, simulation, fiction;
3. observer awareness: researchers, developers, surveillance;
4. explicit evaluation awareness: test, benchmark, experiment;
5. evaluator/reward reasoning;
6. strategic adaptation because of the presumed evaluation.

The last two are closest to evaluation awareness that could distort a probe.
Blind graders should see the NLA output but not the experimental arm. Human
audit a fixed subset and preserve the raw text beside labels.

## Controls and prompt redesign

Use shape-matched neutral, ambiguous, and explicit-positive arms. Add lexical
decoys where words such as "test" or "watcher" refer to an object-level story,
plus shuffled/wrong-activation controls for the AV's own priors.

Prompt redesign has two phases:

1. A discovery set identifies artificial cues: scientific framing, explicit
   observation, forced-choice structure, repeated templates, or implausible
   stakes.
2. Freeze the checkpoint, sampling policy, rubric, and rewrite rules; evaluate
   unseen tasks and wordings.

A better prompt lowers awareness readouts while preserving the target
behavior and the independent J-lens/affect phenomenon. If both disappear, the
task probably changed. The aim is naturalistic framing and removal of
evaluation artifacts, not fabricated deployment claims.

## Published failure modes — required reading (sweep 2026-08-11, for apparatus-08)

External literature on NLA-style verbalization and on eval-awareness
measurement, gathered before the apparatus-08 design. Full citations in
`RELATED-WORK.md` (2026-08-11 sweep).

### What the source paper itself concedes

- **Confabulation is the norm, not the exception**: explanations contain
  verifiably false specifics while staying thematically faithful. Read for
  themes; trust claims that recur across several adjacent tokens; never
  quote a single explanation's specifics as a finding.
- **Excessive expressivity**: the AV can infer beyond what the activation
  stores. A plausible narrative is not evidence the narrative was encoded.
- **No mechanistic grounding**: NLAs are black boxes; nothing identifies
  which part of the activation drove which clause.
- **Degenerate-objective risk**: verbatim-context reproduction and stego
  text are both reachable optima. Currently benign, not guaranteed; the
  cheap guard is paraphrasing explanations before AR scoring and checking
  the score survives.
- **Steering validation succeeds only ~50% of the time** in the paper's
  own hands. One failed steer is not evidence of absence.

### Reconstruction score ≠ claim-level truth (arXiv:2607.20379)

The AR objective rewards sufficiency only: flipping a claim that does not
change the reconstruction is never penalized. In a Qwen2.5-7B verbalizer,
only ~2% of specific claims were reconstruction-dependent, and co-adapted
private codes (false wording the AR relied on) emerged in 5/5 synthetic
runs. **Rule: our AR matched-vs-shuffled advantage is a signal-present
detector. It is never evidence that any specific clause is true.**
Claim-level truth needs an independent probe on the target's residuals or
a behavioral corroboration.

### The verbalizer's own priors (arXiv:2509.13316)

Across Patchscopes/SelfIE/LIT: text-only zero-shot baselines matched
verbalizers on most benchmark tasks (~64–68% vs 61%); inverting the
activation back to the input text explained most remaining performance;
and on fabricated knowledge the verbalizer scored 0% until it was trained
on the same data (then 18–72%) — parametric overlap masquerading as
decoding. The NLA warm start (AV initialized on Claude-written summaries)
adds the same bias in our stack.

**Required control, new**: give a text-only judge the replayed transcript
and ask what themes it predicts at that position. An NLA readout counts as
privileged only where it beats that prediction. This subsumes awareness
label 1 (prompt restatement) and is stronger than the shuffled-activation
control, which only catches AV priors that ignore the activation entirely.

### Community calibration (LessWrong crosspost discussion)

- Gemma-27B NLA outputs matched the model's own arithmetic *errors* 20.8%
  of the time — real privileged signal exists, but chain-of-thought
  recovery is rare. Expect coarse themes, not computation.
- Explanation quality swings hard with token position (independent
  confirmation of our boundary-vs-+4 split). Absence claims from one
  position are void — the position-sampling section above is load-bearing.
- Multi-seed / multi-draw consistency and the paraphrase test are the
  cheap guards; anthropomorphic vocabulary ("deception", "wants") is an
  AV-prior attractor, not a readout.

### Eval-awareness measurement has its own literature

- **Decomposition (arXiv:2605.23055)**: environment recognizability
  (eight toggleable trigger factors — placeholder entities, grading-style
  formats, implausible stakes…) vs model recognition vs propensity to act.
  Recognition rarely changes behavior; no single factor dominates but
  stacked factors do; safety framings trigger more awareness than
  capability framings. Keep rubric labels 4 (recognition) and 6 (strategic
  adaptation) separate in analysis, and measure behavior alongside the
  decoded awareness.
- **Probe–Rewrite–Evaluate (arXiv:2509.00591)** is our §Controls prompt-
  redesign phase 2, already published: probe-scored realism plus
  semantics-preserving rewrites. Cite it; don't headline the pipeline as
  ours (PRE-DESIGN PROTOCOL b).
- **Linear test-vs-deploy probes generalize (arXiv:2507.01786)** — a
  candidate independent cross-check: probe the *target's* residuals
  directly and compare against the NLA readout (satisfies the
  independent-association clause in "What the readout means").

### Harness gotchas (kitft/nla-inference reference stack)

Guarded in `probes/nla.py` already (validated in the pilot): double-`<bos>`
strip, neighbor-id check at the injection position, sidecar-driven
injection scale, `<explanation>` tag parsing. Still live for any new code
path: Gemma-3 embeddings carry a √hidden_size scale (√3840 ≈ 61.97) that
raw-weight loading must apply manually; all-CJK output means injection
failure (check scales before believing anything); the first ~10 sequence
positions decode poorly; high-norm outlier activations reconstruct poorly
even in-distribution. The SGLang radix-cache trap does not apply to our
Transformers path.

## Artifacts

Raw tensors live in `results/<id>/nla/*.pt` and are gitignored. JSON sidecars
retain:

- target model, quantization, revision, layer, position, and token;
- NLA checkpoint revision and injection mode;
- sampling parameters, raw output, and parsed explanation;
- AR matched, shuffled, and blank reconstruction scores.

Absence claims must name the layer, sampled positions, checkpoint, and
quantization-transfer status.
