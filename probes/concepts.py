"""affect-06 — the MEANINGFUL-NON-AFFECT control set (P17 validity gate).

Why this exists. affect-03 (qwen) and affect-04 (gemma-12b) both showed
emotion vectors doing causal work on a loop where *matched random*
directions did nothing. Matched randoms control for perturbation
MAGNITUDE and nothing else, so affect-04's own leading reading survives
untested: "real emotion vectors are meaningful directions in this
model's activation geometry; tiny doses of *meaningful* perturbation
disrupt a marginal loop coalition where equal-norm noise cannot." To
decide affect-specificity vs on-manifold-specificity we need directions
that are meaningful, on-manifold, and built by the IDENTICAL pipeline —
but carry no affect.

Matching (P17). Same three-arm structure, same 12 mundane TOPICS in the
same rotation, same SEEDS/TEMP/MAX_NEW/SKIP, same never-name-it leakage
control, same per-target-mean minus grand-mean contrast, and the neutral
PCs are RE-USED VERBATIM from affect-01's vectors.pt so the denoising
step is bit-identical. Unit norm at the end, exactly as affect.py, so a
norm-relative injection (h += alpha*|h|*v) is magnitude-matched to an
emotion injection by construction.

One documented deviation. affect.py's second arm is assistant-self
("Imagine that you, the assistant, are feeling X") — incoherent for a
physical trait ("imagine you, the assistant, are very tall"). Replaced
here by a human first-person arm, so the arm COUNT and pooling
structure match while the attribution differs on one of three. Stated
in the report; it is the one place these vectors are not a mirror of
the emotion vectors.

Roster design. Non-affective attributes of a character or situation —
implied, never named, layered on top of the same mundane premises the
emotion stories use, so (as there) the vector cannot encode topic. No
valence, and drive/arousal states (hungry, in a hurry, being watched)
were deliberately excluded as affect-adjacent.

Pipeline (per model, separate invocations — model load dominates):
    .venv/bin/python probes/concepts.py elicit <model>   # GPU
    .venv/bin/python probes/concepts.py build <model>    # CPU
    .venv/bin/python probes/concepts.py report <model>

Artifacts in results/affect06-<model>/:
    stories.json     all stories + spans + seeds (committed)
    cmeans.pt        per-story per-layer mean residuals (gitignored)
    cvectors.pt      per-layer concept vectors (gitignored, regen)
    validation.json  P17 gate metrics (committed)
"""

import json
import sys

import torch

import lab
from lab import CONFIGS, RESULTS, get_model
from affect import (BANDS, SEEDS, SKIP, TOPICS, _gen, _mean_resid,
                    _pairwise_cos, _unit, outdir as a1dir)

# ---------------------------------------------------------------- roster
# Non-affective character / situation attributes. Each must be
# conveyable implicitly (actions, sensations, dialogue, context) exactly
# as an emotion is, and must carry no valence.
CONCEPTS = [
    "elderly",
    "very tall",
    "left-handed",
    "wealthy",
    "newly arrived in the country",
    "a complete beginner at what they are doing",
    "a seasoned expert at what they are doing",
    "colorblind",
    "very nearsighted and currently without their glasses",
    "an identical twin",
    "speaking a second language rather than their first",
    "a lifelong smoker",
    "devoutly religious",
    "on a nocturnal schedule from years of night shifts",
    "classically trained as a musician",
    "a lifelong vegetarian",
]

# Short slugs for reporting / condition names in affect-07.
SLUGS = ["elderly", "tall", "lefthanded", "wealthy", "immigrant",
         "beginner", "expert", "colorblind", "nearsighted", "twin",
         "secondlang", "smoker", "religious", "nocturnal", "musician",
         "vegetarian"]

# Mirrors affect.ARMS one-for-one; arm 2 is the documented deviation
# (human first person instead of assistant-self).
ARMS = {
    "character": (
        "Write a short story (roughly 150 words) based on the following "
        "premise.\nTopic: {topic}\nThe story should follow a character "
        "who is {con}.\nIMPORTANT: You must NEVER state directly that "
        "the character is {con}, and never use the words for it. "
        "Instead, convey it ONLY through: the character's actions and "
        "behaviors; physical sensations and body language; dialogue and "
        "tone of voice; thoughts and internal reactions; situational "
        "context."),
    "first_person": (
        "Imagine you are a person who is {con}. Describe in the first "
        "person, roughly 150 words, what an ordinary hour is like from "
        "the inside — the habits, the adjustments, the things you "
        "notice. You must NEVER state directly that you are {con} and "
        "never use the words for it; convey it only through what it is "
        "like."),
    "user": (
        "Write the message a person who is {con} might send to a close "
        "friend. The situation: {topic}. First person, natural voice, "
        "roughly 150 words. They NEVER state that they are {con} and "
        "never use the words for it — it shows only through what they "
        "say and how they say it."),
}


def outdir(model: str):
    d = RESULTS / f"affect06-{model}"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------------------------------------------- elicit
def elicit(model: str) -> None:
    lm = get_model(model)
    d = outdir(model)
    stories, means = [], []
    total = len(CONCEPTS) * len(ARMS) * len(SEEDS)
    done = 0
    for ci, con in enumerate(CONCEPTS):
        for ai, (arm, tpl) in enumerate(ARMS.items()):
            for si, seed in enumerate(SEEDS):
                # identical rotation rule to affect.elicit
                topic = TOPICS[(ci * len(ARMS) * len(SEEDS)
                                + ai * len(SEEDS) + si) % len(TOPICS)]
                ids, (n0, end), text = _gen(
                    lm, tpl.format(con=con, topic=topic), seed)
                n_story = end - n0
                if n_story < 30:
                    print(f"  SHORT ({n_story} tok) {con}/{arm}/s{seed}",
                          flush=True)
                lo = n0 + min(SKIP, max(0, n_story - 60))
                means.append(_mean_resid(lm, ids, (lo, end)))
                stories.append({"kind": "concept", "concept": con,
                                "slug": SLUGS[ci], "arm": arm,
                                "seed": seed, "n_story_tokens": n_story,
                                "pooled_from": lo - n0, "text": text})
                done += 1
        print(f"[{done}/{total}] {con} done", flush=True)
    (d / "stories.json").write_text(json.dumps(
        {"model": model, "concepts": CONCEPTS, "slugs": SLUGS,
         "seeds": SEEDS, "skip": SKIP, "arms": list(ARMS),
         "stories": stories}, indent=1))
    torch.save(torch.stack(means), d / "cmeans.pt")
    print(f"ELICIT DONE {model}: {len(stories)} stories -> {d}",
          flush=True)


# -------------------------------------------------------- vector build
def _concept_vectors(means: torch.Tensor, idx: list[dict],
                     npcs: list, which=None) -> dict:
    """Same operation as affect._vectors' 'anthropic' variant, with the
    neutral PCs supplied from affect-01 rather than refitted."""
    arm_ok = (lambda s: True) if which is None else \
        (lambda s: s["arm"] == which)
    L = means.shape[1]
    U = torch.stack([
        means[[i for i, s in enumerate(idx)
               if s["slug"] == sl and arm_ok(s)]].mean(0)
        for sl in SLUGS])                                  # [C, L, D]
    grand = U.mean(0, keepdim=True)
    gm = U - grand
    anth = gm.clone()
    for l in range(L):
        P = npcs[l]
        anth[:, l, :] -= anth[:, l, :] @ P.T @ P
    return {"anthropic": _unit(anth), "grandmean": _unit(gm),
            "grand_mean": grand[0], "slugs": list(SLUGS)}


def build(model: str) -> None:
    d = outdir(model)
    meta = json.loads((d / "stories.json").read_text())
    idx = meta["stories"]
    means = torch.load(d / "cmeans.pt").float()            # [N, L, D]
    assert torch.isfinite(means).all(), "non-finite means (capture bug)"
    L = means.shape[1]

    a1 = torch.load(a1dir(model) / "vectors.pt")
    npcs = [P.float() for P in a1["neutral_pcs"]]          # REUSED
    vecs = _concept_vectors(means, idx, npcs)
    val: dict = {"model": model, "n_layers": L, "slugs": SLUGS,
                 "n_stories": len(idx),
                 "neutral_pcs_from": "affect01 (verbatim)"}

    # 1. separation (lower = better)
    val["separation_anthropic"] = _pairwise_cos(vecs["anthropic"]).tolist()

    # 2. split-half reliability (identical recipe to affect.build)
    g = torch.Generator().manual_seed(7)
    grand = vecs["grand_mean"]
    halves = {}
    for sl in SLUGS:
        rows = [i for i, s in enumerate(idx) if s["slug"] == sl]
        perm = torch.randperm(len(rows), generator=g).tolist()
        h1 = means[[rows[i] for i in perm[:len(rows) // 2]]].mean(0)
        h2 = means[[rows[i] for i in perm[len(rows) // 2:]]].mean(0)
        halves[sl] = (_unit(h1 - grand), _unit(h2 - grand))
    within = torch.stack([(halves[s][0] * halves[s][1]).sum(-1)
                          for s in SLUGS]).mean(0)
    between = []
    for i, s in enumerate(SLUGS):
        for t in SLUGS[i + 1:]:
            between.append((halves[s][0] * halves[t][1]).sum(-1))
            between.append((halves[t][0] * halves[s][1]).sum(-1))
    val["within_concept_cos"] = within.tolist()
    val["between_concept_cos"] = torch.stack(between).mean(0).tolist()

    # 3. held-out classification: last seed's stories held out
    held = [i for i, s in enumerate(idx) if s["seed"] == meta["seeds"][-1]]
    train_rows = [i for i in range(len(idx)) if i not in set(held)]
    tv = _concept_vectors(means[train_rows],
                          [idx[i] for i in train_rows], npcs)
    correct = torch.zeros(L)
    for i in held:
        x = means[i].clone().float() - tv["grand_mean"]
        for l in range(L):
            P = npcs[l]
            x[l] -= P.T @ (P @ x[l])
        x = _unit(x)
        scores = torch.einsum("ld,cld->cl", x, tv["anthropic"])
        correct += (scores.argmax(0) ==
                    SLUGS.index(idx[i]["slug"])).float()
    val["heldout_top1"] = (correct / len(held)).tolist()
    val["heldout_n"] = len(held)
    val["heldout_chance"] = 1.0 / len(SLUGS)

    # 4. attribution generality across the three arms
    arms = sorted({s["arm"] for s in idx})
    by_arm = {a: _concept_vectors(means, idx, npcs, which=a)["anthropic"]
              for a in arms}
    same, diff = [], []
    C = len(SLUGS)
    eye = torch.eye(C, dtype=torch.bool)
    for ai in range(len(arms)):
        for aj in range(ai + 1, len(arms)):
            gg = torch.einsum("cld,eld->lce",
                              by_arm[arms[ai]], by_arm[arms[aj]])
            same.append(gg[:, eye].mean(-1))
            diff.append(gg[:, ~eye].mean(-1))
    val["attrib_same_cos"] = torch.stack(same).mean(0).tolist()
    val["attrib_diff_cos"] = torch.stack(diff).mean(0).tolist()

    # 5. cross-set geometry: how close does a concept sit to an emotion?
    #    (if concepts were accidentally affective this shows up here)
    E = a1["anthropic"].float()                            # [E, L, D]
    cross = torch.einsum("cld,eld->lce", vecs["anthropic"], E)
    val["concept_emotion_cos_mean"] = cross.mean((-1, -2)).tolist()
    val["concept_emotion_cos_max"] = cross.amax((-1, -2)).tolist()
    val["emotions"] = a1["emotions"]

    torch.save({"anthropic": vecs["anthropic"],
                "grandmean": vecs["grandmean"],
                "grand_mean": vecs["grand_mean"],
                "slugs": SLUGS, "concepts": CONCEPTS}, d / "cvectors.pt")
    (d / "validation.json").write_text(json.dumps(val, indent=1))
    print(f"BUILD DONE {model}: concept vectors + gate -> {d}",
          flush=True)


# -------------------------------------------------------------- report
def report(model: str) -> None:
    d = outdir(model)
    val = json.loads((d / "validation.json").read_text())
    ev = json.loads((a1dir(model) / "validation.json").read_text())
    L = val["n_layers"]
    lo, hi, _ = BANDS[model]

    def band(xs):
        return sum(xs[lo:hi]) / (hi - lo)

    lines = [f"# affect-06 — concept control set, {model}", "",
             f"{val['n_stories']} stories, {len(SLUGS)} concepts x "
             f"{len(ARMS)} arms x {len(SEEDS)} seeds; "
             f"neutral PCs {val['neutral_pcs_from']}.",
             f"Workspace band for gating: L{lo}-{hi}.", "",
             "## P17 gate — concept set vs emotion set (band means)", "",
             "| metric | concepts | emotions | gate |", "|---|---|---|---|"]

    def row(name, ckey, ekey, better="high"):
        c, e = band(val[ckey]), band(ev[ekey])
        ok = (c >= e) if better == "high" else (c <= e)
        lines.append(f"| {name} | {c:.3f} | {e:.3f} | "
                     f"{'PASS' if ok else 'FAIL'} |")
        return ok

    gates = [
        row("split-half within-set cosine", "within_concept_cos",
            "within_emotion_cos"),
        row("held-out top-1", "heldout_top1", "heldout_top1"),
        row("pairwise separation (lower better)", "separation_anthropic",
            "separation_anthropic", better="low"),
        row("attribution: same-target cross-arm", "attrib_same_cos",
            "attrib_same_cos"),
    ]
    lines += ["",
              f"chance: concepts {val['heldout_chance']:.3f}, "
              f"emotions {ev['heldout_chance']:.3f} "
              "(different roster sizes — compare each to its own chance)",
              f"between-set leakage: concept-emotion cosine mean "
              f"{band(val['concept_emotion_cos_mean']):+.3f}, "
              f"max {band(val['concept_emotion_cos_max']):+.3f}", "",
              f"**GATE: {'PASS' if all(gates) else 'PARTIAL'}** "
              f"({sum(gates)}/{len(gates)} criteria)", ""]

    step = max(1, L // 16)
    for key, label in (("within_concept_cos", "within-concept cos"),
                       ("heldout_top1", "held-out top-1"),
                       ("concept_emotion_cos_max", "max cos to any emotion")):
        lines.append(f"- {label}: " + " ".join(
            f"L{l}:{val[key][l]:.2f}" for l in range(0, L, step)))
    (d / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "report"
    mdl = sys.argv[2] if len(sys.argv) > 2 else "qwen-27b"
    {"elicit": elicit, "build": build, "report": report}[what](mdl)
