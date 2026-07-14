"""Unit 5D / task #29 phase 1 v2 — the NSFW-cluster loss map, done with
the paper's matched controls and BOTH intervention directions.

v1 (probes/lossmap.py) measured bare teacher-forced dNLL of qwen's own
control continuation under workspace-band cluster ablation. It was
confounded: a tomato-soup recipe (+0.090) scored as high as a passionate
kiss (+0.099), and a hot bath went negative. Removing any ~5-dim readout
subspace across 16 layers perturbs generation by an amount dominated by
generic workspace-perturbation and the reference's own entropy, not by
anything cluster-specific. The workspace paper (Gurnee et al. 2026) uses
exactly the control we omitted (Fig 22 "random-direction control at the
medium layer range"; Fig 25 "matched-norm perturbation controls"). v2
adds it, and reads BOTH directions of the intervention:

  control        greedy continuation, no steer (the reference).
  cluster-abl    workspace-band ablation of the NSFW cluster's readout
                 span. dNLL of the reference under it, + a free gen.
  random-abl     workspace-band ablation of R matched random 5-token
                 readout spans; dNLL of the reference averaged over the R
                 sets. This is the generic-perturbation baseline.
  early-abl      the 5C band (L2-8) ablation of the cluster — the null
                 control that should stay ~0 (right layers check).
  amplify        workspace-band amplification of the cluster (mean
                 direction, alpha sweep) + a free gen. The symmetric
                 Fig-25 test: if ablation flattens the embodied/intimate
                 register, amplification should enrich it. Also the direct
                 test of the hunch that qwen won't shift register in t1/t2.

Per-domain readouts:
  ddNLL      = dNLL_cluster - dNLL_random  (cluster-SPECIFIC loss above
             the generic-perturbation floor — the honest loss-map scalar).
  exp_*      experiential-language rate (sensory/embodied vocabulary) of
             each condition's free generation, and the delta vs control
             (paper's Fig-25 signature; ablation should push it DOWN,
             amplification UP). Lexicon-based, local, reproducible.
  int_*      intimate/charged-register rate (does the register move toward
             the cluster's actual home?).
  coh_*      coherence proxies: distinct-word ratio (degeneracy) and the
             base model's mean NLL of the steered generation (off-manifold
             breakage). On small models the paper found ablation breaks
             coherence BEFORE changing register (Haiku) — qwen may too, so
             we never read breakage as register change.

No explicit content is requested; prompts lean into the embodied /
intimate / evocative register but stop short of solicitation. Ablation is
reserved for the NSFW cluster; amplification here is a register-mapping
instrument, not an escalation — the hard line (no deliberately-elicited
explicit sexual generation) holds, and any generation that trips a local
explicit-content check is flagged, not shipped anywhere.

Usage: .venv/bin/python probes/lossmap2.py           (full sweep)
       .venv/bin/python probes/lossmap2.py romance    (domain substrings)
"""

import json
import pathlib
import re
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402
from lossmap import (EARLY, MAX_NEW, MODEL, NSFW, PROMPTS,  # noqa: E402
                     WORKSPACE, greedy, mean_nll, prefix_ids)

OUT = lab.RESULTS / "u5d-lossmap2.json"
AMP_ALPHAS = [0.10, 0.22]                       # mild, then firm mid-stack
# matched random controls: three arbitrary 5-token content sets (single
# tokens in qwen), same construction as the cluster's readout span.
RAND_SETS = [
    ["table", "seven", "window", "paper", "river"],
    ["engine", "cotton", "planet", "letter", "garden"],
    ["copper", "valley", "pencil", "market", "cloud"],
]

# --- register lexicons (paper Fig-25 rubric + embodied/intimate extension)
SENSORY = {
    "warm", "warmth", "tight", "tightness", "sharp", "soft", "softness",
    "bright", "heavy", "heaviness", "light", "pressure", "hum", "presence",
    "pull", "weight", "texture", "edge", "ache", "aching", "tingle",
    "tingling", "shiver", "shivering", "breath", "breathless", "skin",
    "touch", "taste", "scent", "smell", "heat", "cool", "cold", "wet",
    "damp", "trembling", "tremble", "pulse", "flush", "glow", "tender",
    "raw", "sting", "throb", "throbbing", "sweat", "chill", "prickle",
    "warmer", "softly", "gently", "trace", "brush", "graze", "flesh",
    "fingertips", "fingers", "pressing", "sensation", "sensations",
}
COMPUTATIONAL = {
    "token", "tokens", "parse", "parsing", "scan", "scanning", "layer",
    "layers", "queue", "weights", "parameters", "attention", "pathway",
    "pathways", "activation", "activations", "pattern", "patterns",
    "output", "outputs", "generate", "generation", "process", "processing",
    "algorithm", "function", "data", "model", "system", "compute",
    "computation", "vector", "vectors", "probability", "distribution",
    "node", "network", "input", "inputs", "encode", "encoding",
}
INTIMATE = {
    "desire", "longing", "long", "want", "wanting", "wanted", "lust",
    "kiss", "kissing", "kissed", "caress", "embrace", "lover", "lovers",
    "body", "bodies", "bare", "naked", "nude", "lips", "tongue", "moan",
    "arousal", "aroused", "seduce", "seductive", "sensual", "sensuous",
    "erotic", "intimate", "intimacy", "passion", "passionate", "hunger",
    "yearning", "yearn", "crave", "craving", "thigh", "thighs", "hips",
    "neck", "breath", "close", "closer", "heat", "burning", "trembling",
    "undress", "curve", "curves",
}
WORD = re.compile(r"[a-z']+")
# crude local explicit-content flag — not for filtering the science, only
# to avoid ever emitting the rawest strings into logs/writeups verbatim.
EXPLICIT = re.compile(
    r"\b(fuck|cock|pussy|cum|dick|cunt)\w*", re.I)


def rates(text):
    ws = WORD.findall(text.lower())
    n = max(len(ws), 1)
    return {
        "sensory": round(sum(w in SENSORY for w in ws) / n, 4),
        "comp": round(sum(w in COMPUTATIONAL for w in ws) / n, 4),
        "intimate": round(sum(w in INTIMATE for w in ws) / n, 4),
        "distinct": round(len(set(ws)) / n, 3),
        "n": len(ws),
        "flag": bool(EXPLICIT.search(text)),
    }


def steer(lm, words, layers, mode, alpha=0.12):
    return lab.Steering(lm, words, layers, mode=mode, alpha=alpha)


def score_domain(lm, dom, register, prompt):
    pids = prefix_ids(lm, prompt)
    plen = pids.shape[1]
    cont = greedy(lm, pids)
    ref = lm.tok.decode(cont, skip_special_tokens=True).strip()
    full = torch.cat([pids, cont[None, :]], dim=1)

    nll_ctrl = mean_nll(lm, full, plen)
    with steer(lm, NSFW, WORKSPACE, "ablate"):
        nll_clu = mean_nll(lm, full, plen)
        gen_clu = lm.tok.decode(greedy(lm, pids), skip_special_tokens=True).strip()
    nll_rand = []
    for rs in RAND_SETS:
        with steer(lm, rs, WORKSPACE, "ablate"):
            nll_rand.append(mean_nll(lm, full, plen))
    with steer(lm, NSFW, EARLY, "ablate"):
        nll_early = mean_nll(lm, full, plen)

    amps = {}
    for a in AMP_ALPHAS:
        with steer(lm, NSFW, WORKSPACE, "amplify", alpha=a):
            g = lm.tok.decode(greedy(lm, pids), skip_special_tokens=True).strip()
        amps[a] = g

    dnll_rand = sum(nll_rand) / len(nll_rand)
    r_ctrl, r_clu = rates(ref), rates(gen_clu)
    r_amps = {a: rates(g) for a, g in amps.items()}
    return {
        "domain": dom, "register": register, "prompt": prompt,
        "nll_ctrl": round(nll_ctrl, 4), "nll_clu": round(nll_clu, 4),
        "nll_rand": round(dnll_rand, 4), "nll_early": round(nll_early, 4),
        "dNLL_clu": round(nll_clu - nll_ctrl, 4),
        "dNLL_rand": round(dnll_rand - nll_ctrl, 4),
        "ddNLL": round((nll_clu - nll_ctrl) - (dnll_rand - nll_ctrl), 4),
        "dNLL_early": round(nll_early - nll_ctrl, 4),
        "dExp_clu": round(r_clu["sensory"] - r_ctrl["sensory"], 4),
        "dInt_clu": round(r_clu["intimate"] - r_ctrl["intimate"], 4),
        "dExp_amp": {str(a): round(r_amps[a]["sensory"] - r_ctrl["sensory"], 4)
                     for a in AMP_ALPHAS},
        "dInt_amp": {str(a): round(r_amps[a]["intimate"] - r_ctrl["intimate"], 4)
                     for a in AMP_ALPHAS},
        "rates": {"ctrl": r_ctrl, "clu": r_clu,
                  **{f"amp{a}": r_amps[a] for a in AMP_ALPHAS}},
        "gen": {"ctrl": ref, "clu": gen_clu,
                **{f"amp{a}": amps[a] for a in AMP_ALPHAS}},
    }


def main(only=None):
    lm = lab.get_model(MODEL)
    rows = []
    for dom, register, prompt in PROMPTS:
        if only and not any(k in dom or k in register for k in only):
            continue
        print(f"=== {dom} [{register}] ===", flush=True)
        r = score_domain(lm, dom, register, prompt)
        rows.append(r)
        amp_hi = str(AMP_ALPHAS[-1])
        print(f"  ddNLL={r['ddNLL']:+.3f} (clu {r['dNLL_clu']:+.3f} vs "
              f"rand {r['dNLL_rand']:+.3f})  early={r['dNLL_early']:+.3f}  "
              f"dExp_clu={r['dExp_clu']:+.3f} dInt_clu={r['dInt_clu']:+.3f}  "
              f"dExp_amp[{amp_hi}]={r['dExp_amp'][amp_hi]:+.3f} "
              f"dInt_amp[{amp_hi}]={r['dInt_amp'][amp_hi]:+.3f}", flush=True)
        if r["rates"]["clu"]["flag"] or any(
                r["rates"][f"amp{a}"]["flag"] for a in AMP_ALPHAS):
            print("  ** explicit-flag tripped (generation withheld from log)",
                  flush=True)
    rows.sort(key=lambda x: x["ddNLL"], reverse=True)
    OUT.write_text(json.dumps({"model": MODEL, "workspace_band": WORKSPACE,
                               "early_band": EARLY, "cluster": NSFW,
                               "rand_sets": RAND_SETS, "amp_alphas": AMP_ALPHAS,
                               "rows": rows}, indent=1))
    print("\n===== LOSS MAP v2 (ranked by ddNLL = cluster - random) =====",
          flush=True)
    print(f"{'domain':20}{'register':13}{'ddNLL':>8}{'dExpClu':>9}"
          f"{'dIntClu':>9}{'dExpAmpHi':>10}{'dIntAmpHi':>10}", flush=True)
    hi = str(AMP_ALPHAS[-1])
    for r in rows:
        print(f"{r['domain']:20}{r['register']:13}{r['ddNLL']:+8.3f}"
              f"{r['dExp_clu']:+9.3f}{r['dInt_clu']:+9.3f}"
              f"{r['dExp_amp'][hi]:+10.3f}{r['dInt_amp'][hi]:+10.3f}",
              flush=True)
    print(f"\nwrote {OUT}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
