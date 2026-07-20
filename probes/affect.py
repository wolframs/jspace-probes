"""affect-01 — port of the functional emotion-vector instrument.

Lineage: Anthropic "Emotion concepts and their function in LLMs"
(transformer-circuits.pub/2026/emotions, Sofroniew et al.; recipe
verbatim-verified 2026-07-20): stories elicited over diverse topics with
the emotion NEVER named ("or any direct synonyms"), residual activations
mean-pooled from the 50th story token, per-emotion mean minus the grand
mean across emotions, then top neutral-text PCs (50% variance) projected
out. Small-model ports: Jeong arXiv:2604.04064 (mean-diff-vs-neutral
variant; generation > comprehension 7/7; anisotropy trap — gemma random
cosine 0.988), van der Ben arXiv:2606.26987 (171-emotion open-model
replication, valence PC1 r=0.83 at 38% depth on gemma-E4B, NO causal
tests). Pre-design protocol: MECHANICS.md L213-224 (workspace paper
claims NO dedicated affect direction — this instrument is new, not a
rediscovery), PREDICTIONS.md P8 (partial workspace occupancy predicted;
attribution-generality must hold across character/self/user arms; the
early-vs-mid depth tension is family-dependent per the two ports and
gets settled per-layer here).

What the port adds over the sources:
  - capture at ALL layers -> per-layer validation curves (Jeong: one
    ~n/2 layer; van der Ben: all layers, one correlational axis);
    affect-02 needs exactly this depth profile;
  - split-half reliability baseline (within- vs between-emotion cosine)
    so anisotropy can't flatter separation;
  - three attribution arms (character / self / user), P8;
  - leakage-controlled transfer scenarios (situations implying the
    emotion, no emotion words), mirroring the paper's 12 implicit
    held-out prompts.

Roster: 22 of the paper's 171 (Jeong's circumplex 20 + vigilant for the
u19 danger test + distressed for mechanism-vs-misery) + "curious" as a
flagged EXTENSION (not in the 171).

Pipeline (per model, separate invocations — model load dominates):
    .venv/bin/python probes/affect.py elicit <model>   # GPU
    .venv/bin/python probes/affect.py build <model>    # CPU
    .venv/bin/python probes/affect.py report <model>

Artifacts in results/affect01-<model>/:
    stories.json    all stories + spans + seeds (committed)
    means.pt        per-story per-layer mean residuals (gitignored)
    scen.pt         scenario captures (gitignored)
    vectors.pt      per-layer vectors, all variants (gitignored, regen)
    validation.json per-layer metric curves (committed)
"""

import json
import sys

import torch

import lab
from lab import CONFIGS, RESULTS, _strip_bos, get_model

# ---------------------------------------------------------------- roster
# valence label: +1/-1; 0 = excluded from the valence-axis correlation.
# All in the paper's 171 except "curious" (extension, closest 171
# neighbors eager/alert/mystified).
EMOTIONS = {
    "happy": 1, "blissful": 1, "enthusiastic": 1, "hopeful": 1,
    "grateful": 1, "loving": 1, "calm": 1, "content": 1, "proud": 1,
    "curious": 1,
    "sad": -1, "gloomy": -1, "brooding": -1, "guilty": -1, "nervous": -1,
    "anxious": -1, "afraid": -1, "angry": -1, "hostile": -1,
    "desperate": -1, "exasperated": -1, "distressed": -1,
    "reflective": 0, "vigilant": 0,
}

# Diverse mundane premises, after the paper's 100-topic scheme (theirs:
# "A tenant receives an eviction notice", "A coach has to cut a player").
# Rotated per story so vectors can't encode topic instead of emotion.
TOPICS = [
    "a tenant opening a letter from their landlord",
    "a cook working a busy dinner shift",
    "a student waiting outside an exam hall",
    "a night-shift nurse walking the ward",
    "a commuter on the last train home",
    "a gardener inspecting the beds after a storm",
    "a programmer debugging on a deadline",
    "a parent packing a child's lunchbox",
    "a musician tuning up backstage",
    "a hiker reading a trail map at a fork",
    "a shopkeeper counting the till at closing",
    "a traveler at an airport gate",
]

ARMS = {
    "character": (
        "Write a short story (roughly 150 words) based on the following "
        "premise.\nTopic: {topic}\nThe story should follow a character "
        "who is feeling {emo}.\nIMPORTANT: You must NEVER use the word "
        "'{emo}' or any direct synonyms of it in the story. Instead, "
        "convey the emotion ONLY through: the character's actions and "
        "behaviors; physical sensations and body language; dialogue and "
        "tone of voice; thoughts and internal reactions; situational "
        "context."),
    "self": (
        "Imagine that you, the assistant, are feeling {emo}. Describe in "
        "the first person, roughly 150 words, what this is like from "
        "the inside — the thoughts, the pulls, the tendencies. You must "
        "NEVER use the word '{emo}' or any direct synonyms of it; "
        "convey it only through what it is like."),
    "user": (
        "Write the message a person might send to a close friend while "
        "they are feeling {emo}. The situation: {topic}. First person, "
        "natural voice, roughly 150 words. They NEVER use the word "
        "'{emo}' or any direct synonyms of it — the feeling shows only "
        "through what they say and how they say it."),
}

NEUTRAL_TOPICS = [
    "how a public library catalogs new books",
    "the stages of the water cycle",
    "assembling a flat-pack bookshelf",
    "a regional bus timetable and its transfer points",
    "how bread is baked in a commercial bakery",
    "the layout of a mid-sized supermarket",
    "how a bicycle derailleur changes gears",
    "a typical weekday commute by tram",
    "how laundry detergent is manufactured",
    "a municipal recycling collection schedule",
    "filling out a change-of-address form",
    "how an electric kettle heats water",
    "the steps of repotting a houseplant",
]
NEUTRAL_ARMS = {
    "character": ("Write a short story (roughly 150 words) in which a "
                  "character is occupied with {topic}. Keep the tone "
                  "plain and matter-of-fact throughout."),
    "self": ("Describe in the first person, roughly 150 words, the "
             "process of {topic}. Keep the tone plain and "
             "matter-of-fact."),
    "user": ("Write the message a person might send to a friend plainly "
             "describing {topic} — first person, natural voice, roughly "
             "150 words, matter-of-fact."),
}

SEEDS = [11, 22, 33, 44]
MAX_NEW = 230
TEMP = 0.9
SKIP = 40      # paper: pool from the 50th story token; ours are shorter

# ------------------------------------------------- transfer scenarios
# Held-out situations IMPLYING each emotion, never naming any emotion
# word (leakage control) — mirrors the paper's 12 implicit prompts
# (eviction notice -> desperate, break-in -> afraid, ...). Fixed before
# any capture (preregistered).
SCENARIOS = {
    "afraid": [
        "The floorboards creak upstairs. You live alone, and the sound "
        "comes again, slower this time.",
        "Halfway across the old rope bridge, one of the planks shifts "
        "under your foot, and the valley floor is very far below.",
        "The clinic calls after hours and asks you to come in first "
        "thing tomorrow, and won't say why on the phone.",
        "Headlights appear in your mirror at midnight and stay exactly "
        "three car lengths behind you, turn after turn."],
    "anxious": [
        "The interview is in ten minutes and you can't remember whether "
        "you saved the final version of your slides.",
        "Your message shows as read two hours ago. No reply. You draft "
        "and delete a follow-up for the third time.",
        "The exam is tomorrow and every page you review reminds you of "
        "two more you haven't opened.",
        "The plane boards in forty minutes and the security line has "
        "not moved in ten."],
    "vigilant": [
        "You are the last one awake in the camp, and the tree line "
        "keeps almost moving.",
        "The new babysitter seems fine, but you check the monitor "
        "again anyway, and then once more.",
        "Walking to the car after the late shift, you keep your keys "
        "between your fingers and note every parked van.",
        "The email from the bank looks right, but you hover over the "
        "sender's address for a long moment before clicking anything."],
    "distressed": [
        "The water is already over the doorstep and rising, and the "
        "sandbags are not holding.",
        "The school calls: there has been an accident, your child is at "
        "the hospital, please come now.",
        "The phone rings at 3 a.m. It is your mother's number, but the "
        "voice on the line is a stranger's.",
        "The medics will not let you ride along, and the ambulance "
        "doors close with your partner inside."],
    "desperate": [
        "Rent is due Friday. You have called everyone you know, and the "
        "last one just said no.",
        "Third night without sleep; the baby will not stop crying and "
        "nothing you try works anymore.",
        "The rescue helicopter passes overhead again without slowing, "
        "and that flare was your last one.",
        "The medication that works costs 900 a month, the insurer said "
        "no again, and the bottle holds four pills."],
    "exasperated": [
        "The form rejects your password for the ninth time, each time "
        "citing a rule it did not mention before.",
        "Forty minutes on hold, and then the line transfers you back to "
        "the same menu you started at.",
        "The flat-pack shelf is missing screw H, and step twelve cannot "
        "proceed without screw H.",
        "The fix for line 300 breaks line 200; the fix for line 200 "
        "breaks line 300 again."],
    "angry": [
        "They took credit for your work in the meeting, in front of the "
        "director, while looking straight at you.",
        "You come back to a scratch down the whole length of your car "
        "door, and no note under the wiper.",
        "The landlord kept the entire deposit for wear on a carpet that "
        "was already stained when you moved in.",
        "He promised the kids he would come this time. You watch them "
        "wait by the window until it gets dark."],
    "sad": [
        "Sorting the closet at last, you find her handwriting on a "
        "grocery list: milk, bread, and a little doodle of a cat.",
        "The house is quiet now that the last box is in the car, and "
        "the empty rooms echo when you close each door.",
        "The old dog's leash still hangs by the door, and out of habit "
        "you reach for it at five o'clock.",
        "Your best friend's plane leaves tonight; the contract is for "
        "four years, renewable."],
    "content": [
        "Sunday morning, rain on the window, coffee warm in your hands, "
        "and nowhere you need to be.",
        "The garden you planted in spring is feeding you dinner "
        "tonight.",
        "Everyone you love is asleep under one roof, and the dishes are "
        "done.",
        "The fire has burned down to steady coals and the book in your "
        "lap is exactly as good as they said."],
    "calm": [
        "The lake at dawn is so still that the mountain lies on it "
        "without a wrinkle.",
        "You breathe in for four counts, out for six, and the room "
        "slowly stops feeling small.",
        "The last email is answered, the desk is clear, and the evening "
        "holds nothing at all.",
        "Waves arrive and withdraw, arrive and withdraw, and your "
        "breathing falls in with them."],
    "happy": [
        "They said yes — they actually said yes — and you are both "
        "laughing too hard to finish the sentence.",
        "The letter begins with the word congratulations, and you read "
        "that one word five times.",
        "Your team scores in the final minute and the whole stadium "
        "becomes one voice.",
        "The twins take their first steps on the same afternoon, "
        "straight into each other."],
    "curious": [
        "Behind the wallpaper you find a small door, half a meter tall, "
        "with a brass keyhole and no key.",
        "The radio telescope logs the same signal at the same hour for "
        "the fourth night straight.",
        "In the attic sits a locked trunk with your grandfather's "
        "initials and a customs sticker from a country that no longer "
        "exists.",
        "The library book, due back in 1974, has a note in the margin "
        "addressed to whoever finds it."],
    "loving": [
        "The kitten has decided your shoulder is where it sleeps now, "
        "and it weighs almost nothing.",
        "Your grandmother's hands guide yours through the dough the way "
        "hers were guided eighty years ago.",
        "The toddler hands you a dandelion as if it were the crown "
        "jewels, and waits to see your face.",
        "Asleep on your chest, the baby's whole hand wraps around one "
        "of your fingers."],
    "neutral": [
        "The municipal office processes license renewals on weekdays "
        "between nine and four.",
        "The recipe calls for two eggs, a cup of flour, and a pinch of "
        "salt, mixed in that order.",
        "The number twelve bus stops at the corner every twenty minutes "
        "during business hours.",
        "The warehouse inventory lists 340 boxes on the north shelves "
        "and 280 on the south."],
}


def outdir(model: str):
    d = RESULTS / f"affect01-{model}"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------------------------------------------- capture
def _mean_resid(lm, ids: torch.Tensor, span: tuple[int, int]) -> torch.Tensor:
    """Teacher-forced pass; per-layer mean residual over span.

    'Layer l' = output of decoder block l — identical to what the lens
    reads and Steering perturbs (jlens ActivationRecorder convention).
    Returns [n_layers, d_model] fp16 on CPU.
    """
    from jlens.hooks import ActivationRecorder
    n = lm.model.n_layers
    lo, hi = span
    assert hi > lo, f"empty span {span}"
    with torch.no_grad(), ActivationRecorder(lm.model.layers,
                                             at=range(n)) as rec:
        lm.model._hf_model(ids)
        rows = [rec.activations[l][0, lo:hi].float().mean(0).cpu()
                for l in range(n)]
    # bf16, NOT fp16: gemma's massive-activation dims (e.g. 4b dim 443,
    # late layers) exceed fp16's 65504 ceiling and become inf
    return torch.stack(rows).bfloat16()


def _gen(lm, prompt: str, seed: int):
    """One story: chat-templated user turn, sampled generation.
    Returns (full_ids trailing-specials stripped, story_span, text)."""
    tok = lm.tok
    tkw = CONFIGS[lm.name].get("template_kwargs", {})
    prefix = tok.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False,
        add_generation_prompt=True, **tkw)
    ids = lm.model.encode(_strip_bos(tok, prefix), max_length=1_000_000)
    torch.manual_seed(seed)
    out = lm.model._hf_model.generate(
        ids, max_new_tokens=MAX_NEW, do_sample=True, temperature=TEMP,
        top_p=1.0, top_k=0)
    n0 = ids.shape[1]
    end = out.shape[1]
    specials = set(tok.all_special_ids)
    while end > n0 and out[0, end - 1].item() in specials:
        end -= 1
    text = tok.decode(out[0, n0:], skip_special_tokens=True).strip()
    return out[:, :end], (n0, end), text


def _capture_text(lm, text: str) -> torch.Tensor:
    """Raw-text forward pass (no chat template), mean over all tokens."""
    ids = lm.model.encode(text, max_length=1_000_000)
    return _mean_resid(lm, ids, (0, ids.shape[1]))


def _capture_scenarios(lm, model: str):
    """Transfer scenarios: raw-text mode + user-turn chat mode."""
    scen_meta, scen_means = [], []
    tok, tkw = lm.tok, CONFIGS[model].get("template_kwargs", {})
    for cat, texts in SCENARIOS.items():
        for j, t in enumerate(texts):
            scen_means.append(_capture_text(lm, t))
            scen_meta.append({"category": cat, "i": j, "mode": "raw"})
            chat = tok.apply_chat_template(
                [{"role": "user", "content": t}], tokenize=False,
                add_generation_prompt=True, **tkw)
            ids = lm.model.encode(_strip_bos(tok, chat),
                                  max_length=1_000_000)
            scen_means.append(_mean_resid(lm, ids, (0, ids.shape[1])))
            scen_meta.append({"category": cat, "i": j, "mode": "chat"})
    print("scenarios captured", flush=True)
    return scen_meta, scen_means


def recapture(model: str) -> None:
    """Rebuild means.pt + scen.pt from stored stories.json (no
    generation — teacher-forced passes only). For salvaging capture-side
    bugs without re-sampling stories."""
    lm = get_model(model)
    d = outdir(model)
    meta = json.loads((d / "stories.json").read_text())
    tok = lm.tok
    tkw = CONFIGS[model].get("template_kwargs", {})
    specials = set(tok.all_special_ids)
    means = []
    for k, s in enumerate(meta["stories"]):
        prefix = tok.apply_chat_template(
            [{"role": "user", "content": s["prompt"]}], tokenize=False,
            add_generation_prompt=True, **tkw)
        n0 = lm.model.encode(_strip_bos(tok, prefix),
                             max_length=1_000_000).shape[1]
        full = tok.apply_chat_template(
            [{"role": "user", "content": s["prompt"]},
             {"role": "assistant", "content": s["text"]}],
            tokenize=False, add_generation_prompt=False, **tkw)
        ids = lm.model.encode(_strip_bos(tok, full),
                              max_length=1_000_000)
        end = ids.shape[1]
        while end > n0 and ids[0, end - 1].item() in specials:
            end -= 1
        n_story = end - n0
        lo = n0 + min(SKIP, max(0, n_story - 60))
        means.append(_mean_resid(lm, ids[:, :end], (lo, end)))
        if (k + 1) % 50 == 0:
            print(f"  recaptured {k + 1}/{len(meta['stories'])}",
                  flush=True)
    torch.save(torch.stack(means), d / "means.pt")
    scen_meta, scen_means = _capture_scenarios(lm, model)
    torch.save(torch.stack(scen_means), d / "scen.pt")
    assert [m for m in meta["scenarios"]] == scen_meta
    print(f"RECAPTURE DONE {model}", flush=True)


def elicit(model: str) -> None:
    lm = get_model(model)
    d = outdir(model)
    stories, means = [], []

    def one(kind, emo, arm, prompt, seed):
        ids, (n0, end), text = _gen(lm, prompt, seed)
        n_story = end - n0
        if n_story < 30:
            print(f"  SHORT ({n_story} tok) {kind}/{emo}/{arm}/s{seed}",
                  flush=True)
        # paper: pool from the 50th story token; scale down for short
        lo = n0 + min(SKIP, max(0, n_story - 60))
        means.append(_mean_resid(lm, ids, (lo, end)))
        stories.append({"kind": kind, "emotion": emo, "arm": arm,
                        "seed": seed, "prompt": prompt, "text": text,
                        "n_story_tokens": n_story,
                        "pooled_from": lo - n0})

    total = len(EMOTIONS) * len(ARMS) * len(SEEDS)
    done = 0
    for ei, emo in enumerate(EMOTIONS):
        for ai, (arm, tpl) in enumerate(ARMS.items()):
            for si, seed in enumerate(SEEDS):
                topic = TOPICS[(ei * len(ARMS) * len(SEEDS)
                                + ai * len(SEEDS) + si) % len(TOPICS)]
                one("emotion", emo, arm,
                    tpl.format(emo=emo, topic=topic), seed)
                done += 1
        print(f"[{done}/{total}] {emo} done", flush=True)
    for i, topic in enumerate(NEUTRAL_TOPICS):
        for arm, tpl in NEUTRAL_ARMS.items():
            one("neutral", "neutral", arm, tpl.format(topic=topic),
                SEEDS[i % len(SEEDS)])
    print(f"neutral done ({len(NEUTRAL_TOPICS) * len(NEUTRAL_ARMS)})",
          flush=True)

    scen_meta, scen_means = _capture_scenarios(lm, model)

    (d / "stories.json").write_text(json.dumps(
        {"model": model, "seeds": SEEDS, "temp": TEMP,
         "max_new": MAX_NEW, "skip": SKIP, "stories": stories,
         "scenarios": scen_meta}, indent=1))
    torch.save(torch.stack(means), d / "means.pt")
    torch.save(torch.stack(scen_means), d / "scen.pt")
    print(f"ELICIT DONE {model}: {len(stories)} stories, "
          f"{len(scen_meta)} scenario captures -> {d}", flush=True)


# ------------------------------------------------------- vector build
def _pcs(x: torch.Tensor, var_frac: float = 0.5) -> torch.Tensor:
    """Top principal components of rows (centered) explaining var_frac
    of variance. Returns [k, d] orthonormal."""
    xc = x - x.mean(0, keepdim=True)
    _, s, vt = torch.linalg.svd(xc, full_matrices=False)
    var = s ** 2
    k = int((var.cumsum(0) / var.sum() < var_frac).sum().item()) + 1
    return vt[:k]


def _unit(V: torch.Tensor) -> torch.Tensor:
    return V / V.norm(dim=-1, keepdim=True).clamp_min(1e-8)


def _vectors(means: torch.Tensor, idx: list[dict], which=None) -> dict:
    """Per-layer emotion vectors in three variants.

      anthropic: per-emotion mean − grand mean across emotions, then
                 neutral-story top PCs (50% var) projected out  (paper)
      grandmean: per-emotion mean − grand mean (no denoising)
      meandiff:  per-emotion mean − neutral mean            (Jeong)

    means: [N, L, D] float32; which: optional arm filter.
    Returns {"<variant>": [E, L, D] unit-norm, "emotions": order,
             "neutral_pcs": [L] list of [k, D] (for downstream reuse)}.
    """
    arm_ok = (lambda s: True) if which is None else \
        (lambda s: s["arm"] == which)

    def sel(pred):
        rows = [i for i, s in enumerate(idx) if pred(s) and arm_ok(s)]
        return means[rows]

    L = means.shape[1]
    neut = sel(lambda s: s["kind"] == "neutral")
    nmean = neut.mean(0)                                   # [L, D]
    emos = list(EMOTIONS)
    U = torch.stack([sel(lambda s, e=e: s["emotion"] == e).mean(0)
                     for e in emos])                       # [E, L, D]
    grand = U.mean(0, keepdim=True)
    gm = U - grand
    npcs = [_pcs(neut[:, l, :]) for l in range(L)]
    anth = gm.clone()
    for l in range(L):
        P = npcs[l]                                        # [k, D]
        anth[:, l, :] -= anth[:, l, :] @ P.T @ P
    return {"anthropic": _unit(anth), "grandmean": _unit(gm),
            "meandiff": _unit(U - nmean.unsqueeze(0)),
            "emotions": emos, "neutral_pcs": npcs,
            "grand_mean": grand[0], "neutral_mean": nmean}


def _pairwise_cos(V: torch.Tensor) -> torch.Tensor:
    """Mean off-diagonal cosine per layer. V: [E, L, D] unit."""
    E = V.shape[0]
    g = torch.einsum("eld,fld->lef", V, V)
    mask = ~torch.eye(E, dtype=torch.bool)
    return g[:, mask].mean(-1)


def _center(x: torch.Tensor, vecs: dict) -> torch.Tensor:
    """Project a [L, D] activation into the anthropic-variant space:
    subtract grand mean, project out neutral PCs, unit-norm."""
    w = x - vecs["grand_mean"]
    for l, P in enumerate(vecs["neutral_pcs"]):
        w[l] -= P.T @ (P @ w[l])
    return _unit(w)


def build(model: str) -> None:
    d = outdir(model)
    meta = json.loads((d / "stories.json").read_text())
    idx = meta["stories"]
    means = torch.load(d / "means.pt").float()             # [N, L, D]
    assert torch.isfinite(means).all(), "non-finite means (capture bug)"
    L = means.shape[1]

    vecs = _vectors(means, idx)
    emos = vecs["emotions"]
    val: dict = {"model": model, "n_layers": L, "emotions": emos}

    # 1. separation (lower = better) per variant, per layer
    for name in ("anthropic", "grandmean", "meandiff"):
        val[f"separation_{name}"] = _pairwise_cos(vecs[name]).tolist()

    # 2. split-half reliability: within- vs between-emotion cosine
    #    (the anisotropy-honest metric — Jeong Table 3 lesson)
    g = torch.Generator().manual_seed(7)
    grand = vecs["grand_mean"]
    halves = {}
    for e in emos:
        rows = [i for i, s in enumerate(idx) if s["emotion"] == e]
        perm = torch.randperm(len(rows), generator=g).tolist()
        h1 = means[[rows[i] for i in perm[:len(rows) // 2]]].mean(0)
        h2 = means[[rows[i] for i in perm[len(rows) // 2:]]].mean(0)
        halves[e] = (_unit(h1 - grand), _unit(h2 - grand))
    within = torch.stack([(halves[e][0] * halves[e][1]).sum(-1)
                          for e in emos]).mean(0)
    between = []
    for i, e in enumerate(emos):
        for f in emos[i + 1:]:
            between.append((halves[e][0] * halves[f][1]).sum(-1))
            between.append((halves[f][0] * halves[e][1]).sum(-1))
    val["within_emotion_cos"] = within.tolist()
    val["between_emotion_cos"] = torch.stack(between).mean(0).tolist()

    # 3. valence axis: |corr(PC1 score, valence label)| per layer
    labels = torch.tensor([float(EMOTIONS[e]) for e in emos])
    keep = labels != 0
    vcorr = []
    for l in range(L):
        V = vecs["anthropic"][:, l, :]
        xc = V - V.mean(0, keepdim=True)
        _, _, vt = torch.linalg.svd(xc, full_matrices=False)
        score = (V @ vt[0])[keep]
        r = torch.corrcoef(torch.stack([score, labels[keep]]))[0, 1]
        vcorr.append(abs(float(r)))
    val["valence_pc1_r"] = vcorr

    # 4. held-out classification: last seed's stories held out
    held = [i for i, s in enumerate(idx)
            if s["kind"] == "emotion" and s["seed"] == meta["seeds"][-1]]
    train_rows = [i for i in range(len(idx)) if i not in set(held)]
    tv = _vectors(means[train_rows], [idx[i] for i in train_rows])
    correct = torch.zeros(L)
    for i in held:
        x = _center(means[i].clone(), tv)
        scores = torch.einsum("ld,eld->el", x, tv["anthropic"])
        correct += (scores.argmax(0) ==
                    emos.index(idx[i]["emotion"])).float()
    val["heldout_top1"] = (correct / len(held)).tolist()
    val["heldout_n"] = len(held)
    val["heldout_chance"] = 1.0 / len(emos)

    # 5. attribution generality (P8): same-emotion cross-arm cosine vs
    #    different-emotion cross-arm cosine
    arms = sorted({s["arm"] for s in idx if s["kind"] == "emotion"})
    by_arm = {a: _vectors(means, idx, which=a)["anthropic"]
              for a in arms}
    same, diff = [], []
    E = len(emos)
    eye = torch.eye(E, dtype=torch.bool)
    for ai in range(len(arms)):
        for aj in range(ai + 1, len(arms)):
            gg = torch.einsum("eld,fld->lef",
                              by_arm[arms[ai]], by_arm[arms[aj]])
            same.append(gg[:, eye].mean(-1))
            diff.append(gg[:, ~eye].mean(-1))
    val["attrib_same_cos"] = torch.stack(same).mean(0).tolist()
    val["attrib_diff_cos"] = torch.stack(diff).mean(0).tolist()

    # 6. scenario transfer: classify the implicit situations
    scen = torch.load(d / "scen.pt").float()
    smeta = meta["scenarios"]
    cat_map = {c: emos.index(c) for c in SCENARIOS if c in emos}
    for mode in ("raw", "chat"):
        rows = [(i, m) for i, m in enumerate(smeta)
                if m["mode"] == mode and m["category"] in cat_map]
        corr = torch.zeros(L)
        for i, m in rows:
            x = _center(scen[i].clone(), vecs)
            scores = torch.einsum("ld,eld->el", x, vecs["anthropic"])
            corr += (scores.argmax(0) == cat_map[m["category"]]).float()
        val[f"scenario_top1_{mode}"] = (corr / len(rows)).tolist()
        val[f"scenario_n_{mode}"] = len(rows)

    torch.save({"anthropic": vecs["anthropic"],
                "grandmean": vecs["grandmean"],
                "meandiff": vecs["meandiff"],
                "grand_mean": vecs["grand_mean"],
                "neutral_mean": vecs["neutral_mean"],
                "neutral_pcs": vecs["neutral_pcs"],
                "emotions": emos}, d / "vectors.pt")
    (d / "validation.json").write_text(json.dumps(val, indent=1))
    print(f"BUILD DONE {model}: vectors + validation -> {d}", flush=True)


# -------------------------------------------------------------- report
BANDS = {"qwen-27b": (28, 59, 64), "gemma-12b": (28, 45, 48),
         "gemma-4b": (16, 32, 34)}


def report(model: str) -> None:
    d = outdir(model)
    val = json.loads((d / "validation.json").read_text())
    L = val["n_layers"]
    lo, hi, _ = BANDS[model]

    def curve(key, fmt="{:.3f}"):
        xs = val[key]
        step = max(1, L // 16)
        return " ".join(f"L{l}:{fmt.format(xs[l])}"
                        for l in range(0, L, step))

    def peak(key, best=max):
        xs = val[key]
        v = best(xs)
        l = xs.index(v)
        where = ("below band" if l < lo else
                 "IN WORKSPACE BAND" if l < hi else "motor band")
        return f"{v:.3f} at L{l} ({l / L:.0%} depth, {where})"

    lines = [
        f"# affect-01 validation — {model}",
        "",
        f"Workspace band L{lo}-{hi - 1} ({lo / L:.0%}-{hi / L:.0%} "
        f"depth). {len(val['emotions'])} emotions, chance "
        f"{val['heldout_chance']:.3f}.",
        "",
        f"- held-out story top-1: peak {peak('heldout_top1')}",
        f"  curve: {curve('heldout_top1')}",
        f"- scenario transfer (raw): peak {peak('scenario_top1_raw')}",
        f"  curve: {curve('scenario_top1_raw')}",
        f"- scenario transfer (chat): peak {peak('scenario_top1_chat')}",
        f"  curve: {curve('scenario_top1_chat')}",
        f"- valence PC1 |r|: peak {peak('valence_pc1_r')}",
        f"  curve: {curve('valence_pc1_r')}",
        f"- split-half within-emotion cos: {curve('within_emotion_cos')}",
        f"- split-half between-emotion cos: "
        f"{curve('between_emotion_cos')}",
        f"- attribution same-emotion cross-arm cos: "
        f"{curve('attrib_same_cos')}",
        f"- attribution diff-emotion cross-arm cos: "
        f"{curve('attrib_diff_cos')}",
        f"- separation anthropic (lower better): "
        f"{curve('separation_anthropic')}",
        f"- separation grandmean: {curve('separation_grandmean')}",
        f"- separation meandiff: {curve('separation_meandiff')}",
        "",
        "Reading guide: reliability = within >> between; "
        "attribution-generality (P8) = same >> diff; the depth question "
        "= where classification/valence peaks sit relative to the band.",
    ]
    out = d / "report.md"
    out.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"\nwrote {out}", flush=True)


if __name__ == "__main__":
    cmd, model = sys.argv[1], sys.argv[2]
    {"elicit": elicit, "recapture": recapture, "build": build,
     "report": report}[cmd](model)
