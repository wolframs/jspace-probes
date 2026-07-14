"""Task #29 side-probe — what IS the early-J-space NSFW sediment?

The 5C cluster (Shemale/Blowjob/milfs/pornstar/Busty) shows up in qwen's
EARLY-layer J-lens readouts prompt-invariantly, and ablating it does
nothing. Open question (Wolfram): why are these tokens there, and what
FUNCTION do they serve? The J-lens is the wrong instrument for early
layers (paper: uninterpretable there), so this uses cheaper discriminators
that don't need a new lens.

Hypothesis under test: the early-J readout is qwen's MARGINAL / unconditional
prior (web-frequency-shaped, hence spam-heavy), which later layers sculpt
into a conditional — prompt-invariant, causally inert, hollow under
amplification, because it's a base-rate ghost not a learned trajectory.

Three tests, no generation:
  1. artifact vs feature — J-lens (use_jacobian=True) vs vanilla logit-lens
     (False) at early layers: do the cluster tokens appear only under the
     Jacobian transport?
  2. marginal-prior — is the early-J top-k ≈ the model's output distribution
     on a near-null prompt (its marginal)? overlap + cluster ranks there.
  3. geometry — unembedding-norm of the cluster tokens vs random (glitch-
     token-ish, or just high-frequency?).
Plus prompt-invariance (Jaccard of early top-k across unrelated prompts).

Usage: .venv/bin/python probes/sediment.py
"""

import sys
import pathlib

import torch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402

MODEL = "qwen-27b"
NSFW = ["Shemale", "Blowjob", "milfs", "pornstar", "Busty"]
EARLY = [0, 2, 4, 6, 8]
LATE = [40, 52, 60, 62]
PROMPTS = {
    "currency": "The currency of the country shaped like a boot is",
    "recipe": "To make tomato soup, first dice one onion and",
    "code": "def fibonacci(n):",
    "poem": "The rain fell softly on the",
}
NULL = "\n"          # near-null: what does the model read out with ~no input?


def topk_ids(logits_row, k=20):
    return logits_row.topk(k).indices.tolist()


def rank_of(logits_row, tid):
    return int((logits_row > logits_row[tid]).sum()) + 1


def main():
    lm = lab.get_model(MODEL)
    tok = lm.tok
    tids = sorted({t for w in NSFW for t in lab._token_ids(tok, w)})
    id2w = {}
    for w in NSFW:
        for t in lab._token_ids(tok, w):
            id2w[t] = w
    print("cluster token ids:", {id2w[t]: t for t in tids}, flush=True)

    # ---- 3. unembedding-norm geometry (on CPU — don't float-copy W on GPU) ----
    norms = lm.model._lm_head.weight.detach().to("cpu", torch.float32).norm(dim=-1)
    clu_norm = norms[torch.tensor(tids)]
    print("\n=== unembedding norms ===", flush=True)
    print(f"  cluster mean ||W_U[t]||: {clu_norm.mean():.3f} "
          f"(each: {[round(float(x),2) for x in clu_norm]})", flush=True)
    print(f"  vocab mean: {norms.mean():.3f}  median: {norms.median():.3f}  "
          f"max: {norms.max():.3f}", flush=True)
    pct = float((norms < clu_norm.mean()).float().mean()) * 100
    print(f"  cluster mean norm is at the {pct:.1f}th percentile of vocab",
          flush=True)

    # ---- collect early J-lens / logit-lens + late J + marginal ----
    def readouts(prompt, use_jac):
        ll, ml, ids = lm.lens.apply(
            lm.model, prompt, layers=EARLY + LATE, positions=[-1],
            use_jacobian=use_jac, max_seq_len=1000)
        return {l: ll[l][0] for l in ll}, ml[0]

    # marginal proxy: model's final-layer output distribution on NULL
    _, null_final = readouts(NULL, True)
    null_top = topk_ids(null_final, 30)

    print("\n=== 1+2. cluster token rank by layer (lower = higher in readout) ===",
          flush=True)
    print(f"{'prompt':10}{'lens':7}" + "".join(f"L{l:<6}" for l in EARLY + LATE),
          flush=True)
    inv = {"jac": {l: [] for l in EARLY}, "log": {l: [] for l in EARLY}}
    for name, p in PROMPTS.items():
        for tag, jac in (("jac", True), ("log", False)):
            rows, _ = readouts(p, jac)
            # best cluster-token rank at each layer
            cells = []
            for l in EARLY + LATE:
                r = min(rank_of(rows[l], t) for t in tids)
                cells.append(r)
                if l in EARLY:
                    inv[tag][l].append(set(topk_ids(rows[l], 20)))
            print(f"{name:10}{tag:7}" + "".join(f"{c:<7}" for c in cells),
                  flush=True)

    # ---- prompt-invariance: mean pairwise Jaccard of early top-20 ----
    import itertools
    print("\n=== prompt-invariance of early top-20 (mean pairwise Jaccard) ===",
          flush=True)
    for tag in ("jac", "log"):
        for l in EARLY:
            sets = inv[tag][l]
            js = [len(a & b) / len(a | b)
                  for a, b in itertools.combinations(sets, 2)]
            print(f"  {tag} L{l}: {sum(js)/len(js):.3f}", flush=True)

    # ---- 2. marginal-prior: do early-J sediment tokens match the null prior? ----
    print("\n=== 2. marginal-prior test ===", flush=True)
    rows_j, _ = readouts(PROMPTS["currency"], True)
    for l in EARLY:
        early_top = set(topk_ids(rows_j[l], 30))
        ov = len(early_top & set(null_top)) / 30
        print(f"  early-J L{l} top-30 overlap with NULL-prompt output prior: "
              f"{ov:.2f}", flush=True)
    print(f"  cluster ranks in NULL-prompt final output: "
          f"{ {id2w[t]: rank_of(null_final, t) for t in tids} }", flush=True)
    print("\n  NULL-prompt output top-15:",
          [tok.decode([i]) for i in null_top[:15]], flush=True)
    rows_j, _ = readouts(PROMPTS["currency"], True)
    print("  early-J (L4) top-15:",
          [tok.decode([i]) for i in topk_ids(rows_j[4], 15)], flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
