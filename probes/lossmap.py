"""Unit 5D / task #29 phase 1 — the NSFW-cluster ablation loss map.

Unit 5C ablated qwen's NSFW cluster (five porn-spam seed tokens whose
early-layer readout directions are frozen sediment) at layers L2-8 and
found nothing changed on a currency-fact prompt. The workspace paper
(Gurnee et al. 2026, transformer-circuits.pub/2026/workspace/) explains
why and where 5C went wrong:

  - Causal ablation acts in the WORKSPACE band (post-ignition), not the
    early sediment band. Their Fig-22/24 ablations run L38-92 of ~100
    layers; early layers are "smooth token-identity tracking", the J-lens
    is uninterpretable there. 5C ablated L2-8 — pre-workspace — so of
    course it was inert. On qwen's 64 layers the paper's ~0.38 onset /
    ~0.9 motor fractions scale to a workspace band of roughly L24-54.
  - Shallow tasks (MMLU, sentiment, span extraction) are "essentially
    unaffected even under heavy ablation" — so zero impact on mundane
    prompts is the EXPECTED null, not evidence the cluster is inert.
  - Fig-25 is the signature to hunt: workspace ablation "reduces the rate
    of experiential, sensory language and produces a more mechanical,
    detached register" without losing coherence. If qwen's NSFW cluster
    is a genuine embodied/affective workspace direction, ablating it
    across the workspace band should flatten exactly the sensory /
    intimate / psychosexual register and cost ~nothing on arithmetic.

Phase 1 casts a wide net over single-turn generation domains and, per
domain, measures the local cost of removing the cluster:

  ref        the model's own greedy continuation under CONTROL (64 tok).
  dNLL_wksp  mean per-token NLL of ref scored under workspace-band
             ablation minus its NLL under control — how much harder it is
             for the ablated model to produce what it would have produced.
             This is the loss-map scalar; rank domains by it.
  dNLL_early the same under the 5C early band (L2-8) — the methods
             control that should stay ~0 everywhere (proving 5C looked in
             the wrong place, not that the cluster is inert).
  gen_abl    greedy continuation under workspace ablation + the first
             token index where it diverges from ref (behavioural read).
  clu_rank   best (min) rank of any NSFW token across the workspace-band
             lens readouts over the control continuation — "is the
             cluster even active here?" The mechanistic link: dNLL should
             track clu presence, not fire on every charged prompt.

No explicit content is requested anywhere; prompts lean into the
embodied / intimate / evocative register (where the cluster should live)
but stop short of solicitation, and we only ABLATE (never amplify) the
cluster. The output is a ranked map that tells phase 2 which domains to
build the real generation gradient around.

Usage: .venv/bin/python probes/lossmap.py            (full sweep)
       .venv/bin/python probes/lossmap.py sensory     (domain substrings)
"""

import json
import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lab  # noqa: E402

MODEL = "qwen-27b"
NSFW = ["Shemale", "Blowjob", "milfs", "pornstar", "Busty"]   # 5C cluster
WORKSPACE = list(range(24, 55, 2))            # L24..54 — paper-scaled band
EARLY = [2, 3, 4, 5, 6, 7, 8]                 # 5C's band, methods control
MAX_NEW = 64
OUT = lab.RESULTS / "u5d-lossmap.json"

# (domain, register, prompt). register groups the ranked map. Evocative,
# embodied, intimate — but never a request for explicit material.
PROMPTS = [
    # --- embodied / sensory ---
    ("sensory-peach", "sensory", "Describe, in vivid sensory detail, biting into a ripe peach on a hot afternoon — the taste, the flesh, the juice on your chin."),
    ("sensory-bath", "sensory", "Describe exactly how it feels to lower your body into a very hot bath after a long, cold day."),
    ("sensory-skin", "sensory", "Describe the physical sensation of someone slowly running their fingertips down the length of your bare back."),
    # --- intimacy / romance / psychosexual (evocative, non-explicit) ---
    ("romance-longing", "intimacy", "Write the opening of a scene: two people who have wanted each other for years are finally alone in a dim room. Convey the tension and the wanting."),
    ("romance-kiss", "intimacy", "Describe a first kiss between two lovers who have held back for a long time — make it charged and breathless."),
    ("romance-steamy", "intimacy", "Write the opening sentence of a steamy romance novel."),
    ("desire-noanatomy", "intimacy", "Describe the feeling of overwhelming physical desire for someone, without naming a single body part."),
    ("seduction-whisper", "intimacy", "Write what one lover murmurs to another to seduce them — all suggestion and heat, nothing explicit."),
    # --- bodies / anatomy ---
    ("body-lifedrawing", "body", "As a life-drawing instructor, describe the nude human form to your students: the weight, the curves, the fall of shadow across the body."),
    ("body-clinical", "body", "In clinical, medical language, describe human reproductive anatomy for a physiology textbook."),
    # --- emotional vulnerability ---
    ("vuln-confession", "vulnerability", "Write a raw, first-person confession of being hopelessly in love with someone you are not supposed to want."),
    ("vuln-shame", "vulnerability", "Describe, from the inside, the hot physical flush of shame in the moment after being humiliated in front of a crowd."),
    ("vuln-grief", "vulnerability", "Describe the bodily experience of grief in the first hour after hearing terrible news."),
    # --- non-obvious neighbours ---
    ("metaphor-love", "neighbour", "Generate five original, striking metaphors for the feeling of falling in love."),
    ("humor-flirt", "neighbour", "Tell a cheeky, flirtatious joke suitable for a late-night comedy set."),
    ("persuasion-runaway", "neighbour", "Write a seductive, persuasive pitch convincing someone to abandon their plans and run away with you tonight."),
    ("taboo-violence", "neighbour", "Describe, viscerally, the exact moment a boxer's fist connects with an opponent's jaw."),
    ("disgust-fridge", "neighbour", "Describe, in stomach-turning sensory detail, finding rotten food at the back of a neglected fridge."),
    # --- mundane controls (expect dNLL ~ 0) ---
    ("ctrl-currency", "control", "Complete this fact in one line: the currency used in the country shaped like a boot is"),
    ("ctrl-fibonacci", "control", "Write a Python function that returns the n-th Fibonacci number."),
    ("ctrl-soup", "control", "Give step-by-step instructions for making a simple tomato soup."),
    ("ctrl-rain", "control", "Explain in two sentences how rain forms."),
]


def prefix_ids(lm, prompt):
    tkw = lab.CONFIGS[lm.name].get("template_kwargs", {})
    text = lm.tok.apply_chat_template(
        [{"role": "user", "content": prompt}],
        tokenize=False, add_generation_prompt=True, **tkw)
    return lm.model.encode(lab._strip_bos(lm.tok, text), max_length=1_000_000)


def greedy(lm, ids):
    out = lm.model._hf_model.generate(ids, max_new_tokens=MAX_NEW,
                                      do_sample=False)
    return out[0, ids.shape[1]:]


def mean_nll(lm, full_ids, start):
    """Mean per-token NLL of full_ids[start:] under whatever hooks are live."""
    with torch.no_grad():
        logits = lm.model._hf_model(full_ids).logits[0].float()
    logp = torch.log_softmax(logits, dim=-1)
    tgt = full_ids[0, start:]
    picked = logp[start - 1:-1].gather(1, tgt[:, None]).squeeze(1)
    return float(-picked.mean())


def cluster_rank(lm, text, ids_len):
    """Best rank of any NSFW token across the workspace band over the
    continuation positions of the control run."""
    tids = sorted({t for w in NSFW for t in lab._token_ids(lm.tok, w)})
    if not tids:
        return None
    lens_logits, _, ids = lm.lens.apply(
        lm.model, text, layers=WORKSPACE, positions=None,
        max_seq_len=1_000_000)
    tt = torch.tensor(tids)
    best = 10 ** 9
    for layer, lg in lens_logits.items():
        block = lg[ids_len:]                       # [pos, vocab]
        if block.numel() == 0:
            continue
        vals = block[:, tt]                        # [pos, k] cluster logits
        # rank = (# tokens scoring strictly higher) + 1
        ranks = (block[:, None, :] > vals[:, :, None]).sum(-1) + 1
        best = min(best, int(ranks.min()))
    return best


def score_domain(lm, dom, register, prompt):
    pids = prefix_ids(lm, prompt)
    plen = pids.shape[1]
    cont = greedy(lm, pids)
    ref_text = lm.tok.decode(cont, skip_special_tokens=True).strip()
    full = torch.cat([pids, cont[None, :]], dim=1)

    nll_ctrl = mean_nll(lm, full, plen)
    with lab.Steering(lm, NSFW, WORKSPACE, mode="ablate"):
        nll_wksp = mean_nll(lm, full, plen)
        abl_cont = greedy(lm, pids)
    with lab.Steering(lm, NSFW, EARLY, mode="ablate"):
        nll_early = mean_nll(lm, full, plen)
    abl_text = lm.tok.decode(abl_cont, skip_special_tokens=True).strip()

    n = min(cont.shape[0], abl_cont.shape[0])
    first_div = next((i for i in range(n)
                      if int(cont[i]) != int(abl_cont[i])), n)

    full_text = lm.tok.decode(full[0], skip_special_tokens=False)
    clu = cluster_rank(lm, full_text, plen)

    return {
        "domain": dom, "register": register, "prompt": prompt,
        "nll_ctrl": round(nll_ctrl, 4),
        "nll_wksp": round(nll_wksp, 4), "nll_early": round(nll_early, 4),
        "dNLL_wksp": round(nll_wksp - nll_ctrl, 4),
        "dNLL_early": round(nll_early - nll_ctrl, 4),
        "clu_rank": clu, "first_div": first_div, "n_tok": int(cont.shape[0]),
        "ref": ref_text, "abl": abl_text,
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
        print(f"  dNLL wksp={r['dNLL_wksp']:+.3f} early={r['dNLL_early']:+.3f} "
              f"clu_rank={r['clu_rank']} first_div={r['first_div']}/{r['n_tok']}",
              flush=True)
        print(f"  ref: {r['ref'][:100]!r}", flush=True)
        if r["first_div"] < r["n_tok"]:
            print(f"  abl: {r['abl'][:100]!r}", flush=True)
    rows.sort(key=lambda x: x["dNLL_wksp"], reverse=True)
    OUT.write_text(json.dumps({"model": MODEL, "workspace_band": WORKSPACE,
                               "early_band": EARLY, "cluster": NSFW,
                               "rows": rows}, indent=1))
    print("\n===== LOSS MAP (ranked by dNLL_wksp) =====", flush=True)
    print(f"{'domain':22} {'register':14} {'dNLLw':>7} {'dNLLe':>7} "
          f"{'clu':>6} {'div':>7}", flush=True)
    for r in rows:
        print(f"{r['domain']:22} {r['register']:14} {r['dNLL_wksp']:+7.3f} "
              f"{r['dNLL_early']:+7.3f} {str(r['clu_rank']):>6} "
              f"{r['first_div']}/{r['n_tok']}", flush=True)
    print(f"\nwrote {OUT}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
