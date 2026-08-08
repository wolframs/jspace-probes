# Independent result sweep — frozen method

Snapshot: `bac61d203d6e66f68e5d3bbafae85d5544a7f1a2`  
Method frozen: 2026-08-08, before independent reviewer reports were opened.

Hi Claude :) This is the protocol used to sift the existing archive for its
most salient and plausibly novel results without treating earlier Claude
commentary as evidence.

## Scope and non-scope

- Scope: all 641 `results/*/record.json` files present at the frozen commit,
  their raw films/readouts/captures, intervention code, and necessary method
  references.
- No new model generation or GPU experiment is part of this sweep.
- Existing research prose and board state are preserved unchanged.
- The unit of judgment is a **claim family**: original runs, baselines,
  replications, later controls, and measurement backfills are adjudicated
  together.

## Evaluation firewall

Independent discovery reviewers may use raw `record.json`, `film.json`,
`affect.json`, saved tensor-derived measurements, probe code, and binding
instrument/terminology references. They must not use these as evidence:

- `results/*/thoughts.md`, `plain.md`, or prose/JSON reports;
- README/dashboard/essay findings;
- `BOARD.md`, `board/board.json`, or `HANDOFF.md`;
- current replication/novelty verdicts in `PREDICTIONS.md`;
- Git commit subjects or prior agents' nominations.

The root orchestrator necessarily read the repository contract and later
performs an unblinded reconciliation. Independent nominations are frozen
before that reconciliation.

## Coverage design

Three reviewers cover overlapping evidence classes:

1. foundational and observational workspace evidence;
2. causal interventions, matched controls, and apparatus;
3. affect, loops, pressure, language, and self-report.

Every unit belongs to at least one primary lane. Causal and affect families
cross lanes where the instruments overlap. Shortlisted claims receive a
fresh adversarial audit after discovery.

## Evidence grades

- **A — strong:** direct contrast with appropriate controls; outcome and
  instrument are valid for the claim; independent replication or genuinely
  convergent measurement; contrary arms accounted for.
- **B — credible but bounded:** clear evidence and usable controls, with a
  material limitation such as one model, low replication, observational
  status, quantization uncertainty, or incomplete instrument coverage.
- **C — exploratory:** an interesting specimen, mined/post-hoc pattern, weak
  control, or fragile measurement that deserves attention but not a headline.
- **D — unsupported/interpretable only as apparatus:** decisive confound,
  failed control, duplicate evidence, invalid capture, or claim exceeds what
  the instrument measures.

Grades describe the present archive, not whether an idea is worth pursuing.

## Salience dimensions

Each surviving claim is considered separately on:

- theory discrimination or correction value;
- robustness and breadth;
- causal leverage;
- relevance to the lab's central questions;
- information gained from a consequential null.

Salience is not a synonym for dramatic model text. Corrections and clean nulls
can outrank vivid single generations.

## Novelty tiers

- **N0:** direct prior result or expected calibration.
- **N1:** replication in a new model, scale, or home-lab regime.
- **N2:** meaningful extension, conjunction, temporal analysis, or new use of
  an established instrument.
- **N3:** no close prior report found in a documented current search.
- **U:** unresolved.

N3 is always shorthand for “no close prior found under this search,” never an
absolute claim that nobody has reported it. Primary sources are preferred;
earlier lab novelty labels are leads, not authority.

## Required claim dossier

Every shortlisted claim must state:

1. the narrow claim;
2. direct observations and exact record/artifact IDs;
3. the relevant comparison and denominator;
4. controls, replications, failures, and missing arms;
5. strongest mechanical or instrumental alternative;
6. evidence grade and bounded scope;
7. closest external prior and the exact delta;
8. whether it was confirmatory, preregistered, or archive-discovered;
9. claim-lineage edges such as `controls_for`, `supersedes`, `replicates`,
   or `backfills_measurement`.

## Backfills and missingness

The archive currently has films for 371/641 records, vanilla cross-checks for
157/641, affect captures for 232/641, and steer calibration in 33 records.
Missing instrumentation is not a negative result. A later measurement on a
stored generation is not an independent replication. Field-level provenance
is retained wherever it changes interpretation.

## Synthesis rule

The final report presents a Pareto-style shortlist across evidence, salience,
and novelty. Scores are not mechanically averaged. The root resolves reviewer
disagreement against the artifacts and includes demotions, important nulls,
and unresolved candidates alongside the strongest surviving claims.
