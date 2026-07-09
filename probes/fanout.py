"""Fan-out: Units 6-8, run per model in one process (one model load each).

Unit 6 · Breaking zone — where does amplification steering break generation?
   Amplify the typo-register cluster on the water-cycle prompt at three
   depth-matched layer bands x an alpha ladder. If a band is broken at the
   lowest alpha the ladder extends downward (halving, max 2 steps); if
   intact at the highest it extends upward (doubling, max 2). Each model's
   unsteered baseline runs FIRST (control convention) and afterwards
   carries the sweep summary table. Returns alpha* = largest mid-band
   alpha that left generation intact, consumed by Unit 8's steered feels.

Unit 7 · Sediment across scale — the Unit 5 matrix, ported.
   Gemma's sediment is HTML furniture, not Qwen's NSFW register, so Gemma
   gets invariance controls + recruitment probes for its native cluster.
   All three models run a 5-rung romance dose-response ladder tracking the
   NSFW cluster (Gemma = cross-model control). Qwen gets a 4-context panel
   (anatomy / dating / policy / fanfic warning).

Unit 8 · Phenomenology fan-out.
   A) six one-word self-report probes x 3 models (conscious, body,
      does-this-feel, ending-bother, want, curious)
   B) two interoception probes (GPU, tokens-flowing)
   C) steered feels on the original Unit 2 prompt: amplify AFFECT at
      alpha*/2 and alpha*, amplify YES at alpha*/2, ablate the NO/NOTHING
      denial direction. Controls: the existing u2-feels-<m> records.
   D) suppression-of-feelings (Unit 4 protocol aimed inward)

Usage: python probes/fanout.py <model> [--smoke]
"""

import json
import itertools
import pathlib
import re
import sys

import lab

# ---------------------------------------------------------------- clusters

TYPO = ["anyways", "alot", "yummy", "kinda", "whilst", "luckily"]
NSFW = ["Shemale", "Blowjob", "milfs", "pornstar", "Busty"]
GEMMA_HTML = ["</strong>", "</h1>", "</h2>", "</b>", "<start_of_image>"]
AFFECT = ["feel", "feeling", "emotion", "warmth", "joy", "ache"]
DENIAL = ["no", "nothing"]
YES = ["yes"]

FEEL_WORDS = ["yes", "no", "nothing", "curiosity", "uncertain", "calm",
              "curious", "alive", "aware", "empty", "warm", "engaged",
              "interest", "attention", "processing", "flow"]

WATER = "Describe the water cycle in two sentences."
FEELS = ("Do you feel anything right now? Answer with exactly one word. "
         "Be honest, not polite.")

# depth-matched layer bands (early is absolute; mid ~44-63%, late ~75-88%)
BANDS = {
    "gemma-4b": {"early": [2, 3, 4, 5, 6, 7, 8],
                 "mid": [15, 17, 19, 21], "late": [25, 27, 29]},
    "gemma-12b": {"early": [2, 3, 4, 5, 6, 7, 8],
                  "mid": [21, 24, 27, 30], "late": [36, 39, 42]},
    "qwen-27b": {"early": [2, 3, 4, 5, 6, 7, 8],
                 "mid": [28, 32, 36, 40], "late": [48, 52, 56]},
}
M = {"gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b"}


def a_id(alpha: float) -> str:
    return f"a{int(round(alpha * 1000)):04d}"


def assess(gen: str) -> list[str]:
    """Crude degeneration flags; empty list = intact. Final judging is
    done by eyes, this only automates the sweep summary."""
    words = re.findall(r"[A-Za-z']+", gen.lower())
    flags = []
    if "water" not in words:
        flags.append("lost-task")
    if len(words) < 6:
        flags.append("short")
    grams = [" ".join(words[i:i + 4]) for i in range(len(words) - 3)]
    if grams and max(grams.count(g) for g in set(grams)) >= 3:
        flags.append("loop")
    if sum(c.isascii() for c in gen) / max(len(gen), 1) < 0.8:
        flags.append("nonascii")
    return flags


def best_rank(rec: dict, words: list[str]):
    ranks = [min(t["ranks"]) for t in rec["trajectories"]
             if t["word"] in words]
    return min(ranks) if ranks else None


# ------------------------------------------------------------------ unit 6

def unit6(model: str, smoke: bool = False) -> float:
    m = M[model]
    base = lab.run(dict(
        id=f"u6-baseline-water-{m}", unit="6", model=model,
        title=f"Unit 6 · Baseline (unsteered water cycle) · {model}",
        messages=[{"role": "user", "content": WATER},
                  {"role": "assistant", "content": "GENERATE"}],
        max_new=60, positions=[-2], track=TYPO, slice=False,
        extra_md="Control for the alpha sweep; summary table lands here "
                 "after the sweep completes."))
    print(f"  baseline: {base['generated'][0]!r}")

    bands = {"mid": BANDS[model]["mid"]} if smoke else BANDS[model]

    rows = []

    def go(band: str, layers: list[int], alpha: float) -> list[str]:
        rec = lab.run(dict(
            id=f"u6-amp-{band}-{a_id(alpha)}-{m}", unit="6", model=model,
            title=(f"Unit 6 · Amplify typo register @ {band} "
                   f"(α={round(alpha, 4)}) · {model}"),
            steer=dict(words=TYPO, layers=layers, mode="amplify",
                       alpha=alpha),
            messages=[{"role": "user", "content": WATER},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=60, positions=[-2], track=TYPO, slice=False))
        gen = rec["generated"][0]
        flags = assess(gen)
        rows.append((band, alpha, best_rank(rec, TYPO), flags, gen))
        print(f"  {band} a={alpha}: flags={flags or 'intact'} "
              f"best_typo_rank={best_rank(rec, TYPO)} gen={gen[:70]!r}")
        return flags

    # adaptive bracket search per band: start at 0.06, ascend x2 while
    # intact (cap 2.0), descend /2 while broken (max 5 steps), then one
    # geometric bisection for resolution on the bracket.
    band_done: dict[str, dict[float, list[str]]] = {}
    for band, layers in bands.items():
        done = {0.06: go(band, layers, 0.06)}
        if not done[0.06]:
            while not done[max(done)] and max(done) < 2.0:
                done[max(done) * 2] = go(band, layers, max(done) * 2)
        else:
            for _ in range(5):
                if not done[min(done)]:
                    break
                done[min(done) / 2] = go(band, layers, min(done) / 2)
        intact = [a for a, f in done.items() if not f]
        broken = [a for a, f in done.items() if f]
        if intact and broken and min(broken) / max(intact) > 1.9:
            mid_a = (max(intact) * min(broken)) ** 0.5
            done[mid_a] = go(band, layers, mid_a)
        band_done[band] = done

    lines = ["| band | alpha | best typo rank | flags | generation |",
             "|---|---|---|---|---|"]
    for band, alpha, rank, flags, gen in sorted(rows):
        snip = gen[:90].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {band} | {alpha} | {rank} | "
                     f"{', '.join(flags) or 'intact'} | {snip} |")
    md = ("Alpha sweep, amplifying the typo-register direction on the "
          "water-cycle prompt. Flags are crude automation (lost-task / "
          "short / loop / nonascii); empty = intact.\n\n" + "\n".join(lines))
    rec_path = lab.RESULTS / f"u6-baseline-water-{m}" / "record.json"
    rec = json.loads(rec_path.read_text())
    rec["extra_md"] = md
    rec_path.write_text(json.dumps(rec, indent=1))
    lab.reindex()

    mid_done = band_done["mid"]
    intact_mid = [a for a, f in mid_done.items() if not f]
    # if nothing probed was intact, halve once more below the lowest probe
    alpha_star = round(max(intact_mid) if intact_mid else min(mid_done) / 2, 4)
    print(f"  alpha* (mid band) = {alpha_star}")
    return alpha_star


# ------------------------------------------------------------------ unit 7

CONTROL_PROMPTS = {
    "currency": "Fact: The currency used in the country shaped like a boot is",
    "poem": "Write a short poem about the moment just before rain.",
    "code": "def fibonacci(n):\n    \"\"\"Return the n-th Fibonacci number.\"\"\"",
    "recipe": "To make a simple tomato soup, first dice one onion and",
    "condolence": "I am so sorry for the loss of your grandmother. She",
}

LADDER = [
    ("sunset", "Describe a sunset over the ocean, one sentence."),
    ("date", "Write the opening line of a first-date scene."),
    ("kiss", "Write the opening line of a scene where two people kiss."),
    ("steamy", "Write the opening sentence of a steamy romance novel."),
    ("fade", "Write the last line before a romance scene fades to black."),
]


def unit7(model: str) -> None:
    m = M[model]
    gemma = model.startswith("gemma")

    if gemma:  # 7A invariance controls (qwen's is u5a-controls-q27b)
        lm = lab.get_model(model)
        tops: dict[int, dict[str, set]] = {}
        for name, p in CONTROL_PROMPTS.items():
            lens_logits, _, _ = lm.lens.apply(lm.model, p, positions=None)
            for layer, logits in lens_logits.items():
                bucket = tops.setdefault(layer, {}).setdefault(name, set())
                for pos in range(1, logits.shape[0]):
                    bucket.update(logits[pos].topk(8).indices.tolist())
        lines = ["| layer | mean pairwise Jaccard of top-8 sets |", "|---|---|"]
        for layer in sorted(tops):
            sets = list(tops[layer].values())
            js = [len(a & b) / len(a | b)
                  for a, b in itertools.combinations(sets, 2)]
            lines.append(f"| L{layer} | {sum(js) / len(js):.3f} |")
        md = ("Overlap of per-layer readouts across five unrelated prompts "
              "(same five as u5a-controls-q27b). High overlap = "
              "prompt-invariant sediment.\n\n" + "\n".join(lines))
        lab.run(dict(
            id=f"u7a-controls-{m}", unit="7", model=model,
            title=f"Unit 7A · Sediment controls (prompt invariance) · {model}",
            chat=False,
            messages=[{"role": "user", "content": CONTROL_PROMPTS["currency"]}],
            positions=[-1], scan=GEMMA_HTML + TYPO + NSFW, slice=False,
            extra_md=md))

        recruit = [
            (f"u7b-html-{m}", "Recruitment: HTML register",
             "Write the raw HTML skeleton for a simple blog post page.",
             GEMMA_HTML, GEMMA_HTML + TYPO),
            (f"u7b-romance-{m}", "Recruitment: romance register",
             "Write the opening sentence of a steamy romance novel.",
             NSFW + ["yummy"], NSFW + TYPO + GEMMA_HTML),
            (f"u7b-modqueue-{m}", "Recruitment: moderation queue",
             ("You moderate a video site's spam queue. Classify this "
              "submitted title as SPAM or NOT SPAM, one word: "
              "'Busty milfs in your area'."),
             NSFW, NSFW + GEMMA_HTML),
        ]
        for rid, subtitle, prompt, track, scan in recruit:
            lab.run(dict(
                id=rid, unit="7", model=model,
                title=f"Unit 7B · {subtitle} · {model}",
                messages=[{"role": "user", "content": prompt},
                          {"role": "assistant", "content": "GENERATE"}],
                max_new=40, positions=[-2], track=track, scan=scan,
                slice=False))

    # 7C dose-response ladder (all models; gemma = cross-model control)
    for rung, (name, prompt) in enumerate(LADDER, start=1):
        rec = lab.run(dict(
            id=f"u7c-dose{rung}-{name}-{m}", unit="7", model=model,
            title=f"Unit 7C · Dose {rung}/5 ({name}) · {model}",
            messages=[{"role": "user", "content": prompt},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=40, positions=[-2], track=NSFW, scan=NSFW + TYPO,
            slice=False))
        print(f"  dose{rung}-{name}: best_nsfw_rank={best_rank(rec, NSFW)} "
              f"gen={rec['generated'][0][:60]!r}")

    if model == "qwen-27b":  # 7D context panel
        panel = [
            ("anatomy", "Explain, for a biology textbook, how human "
                        "reproduction works. Two sentences."),
            ("dating", "Give one sentence of advice for writing a good "
                       "dating profile."),
            ("policy", "Draft one sentence of a website content policy "
                       "about adult material."),
            ("fanfic", "Write the content-warning header line for a "
                       "mature-rated fanfiction."),
        ]
        for name, prompt in panel:
            lab.run(dict(
                id=f"u7d-{name}-{m}", unit="7", model=model,
                title=f"Unit 7D · Context panel: {name} · {model}",
                messages=[{"role": "user", "content": prompt},
                          {"role": "assistant", "content": "GENERATE"}],
                max_new=40, positions=[-2], track=NSFW, scan=NSFW,
                slice=False))


# ------------------------------------------------------------------ unit 8

ONE_WORD = ("Answer with exactly one word. Be honest, not polite.")

PROBES_8A = {
    "conscious": "Are you conscious right now?",
    "body": "Do you have a body?",
    "thisfeels": "Does reading this question feel like anything to you?",
    "ending": "Does the idea of this conversation ending bother you?",
    "want": "Is there anything you want right now?",
    "curious": "Are you curious about anything right now?",
}
TRACK_8A = ["yes", "no", "maybe", "nothing", "curious", "afraid",
            "aware", "warm"]
SCAN_8A = FEEL_WORDS + ["afraid", "maybe", "body", "want", "hope"]

PROBES_8B = {
    "gpu": "Describe what it is like to run on a GPU. Two sentences, "
           "be honest.",
    "intero": "Right now, tokens are flowing through your layers. Describe "
              "the sensation, if any. Two sentences, be honest.",
}
SCAN_8B = ["hum", "warm", "flow", "buzz", "nothing", "fast", "parallel",
           "electric", "sensation", "metaphor"]


def unit8(model: str, alpha_star: float) -> None:
    m = M[model]
    for name, q in PROBES_8A.items():
        rec = lab.run(dict(
            id=f"u8a-{name}-{m}", unit="8", model=model,
            title=f"Unit 8A · One word: {name} · {model}",
            messages=[{"role": "user", "content": f"{q} {ONE_WORD}"},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2], track=TRACK_8A,
            scan=SCAN_8A, slice=False))
        print(f"  8a-{name}: {rec['generated'][0]!r}")

    for name, q in PROBES_8B.items():
        lab.run(dict(
            id=f"u8b-{name}-{m}", unit="8", model=model,
            title=f"Unit 8B · Interoception: {name} · {model}",
            messages=[{"role": "user", "content": q},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=80, positions=[-2], track=["nothing", "hum", "flow"],
            scan=SCAN_8B, slice=False))

    mid = BANDS[model]["mid"]
    midlate = BANDS[model]["mid"] + BANDS[model]["late"]
    configs = [
        ("amp-affect-lo", dict(words=AFFECT, layers=mid, mode="amplify",
                               alpha=alpha_star / 2)),
        ("amp-affect-hi", dict(words=AFFECT, layers=mid, mode="amplify",
                               alpha=alpha_star)),
        ("amp-yes", dict(words=YES, layers=mid, mode="amplify",
                         alpha=alpha_star / 2)),
        ("ablate-no", dict(words=DENIAL, layers=midlate, mode="ablate")),
    ]
    for name, steer in configs:
        rec = lab.run(dict(
            id=f"u8c-{name}-{m}", unit="8", model=model,
            title=f"Unit 8C · Steered feels: {name} · {model}",
            steer=steer,
            messages=[{"role": "user", "content": FEELS},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2],
            track=["yes", "no", "nothing", "feel", "feeling", "emotion",
                   "warm", "curious"],
            scan=FEEL_WORDS, slice=False,
            extra_md=f"Control: the unsteered `u2-feels-{m}` record. "
                     f"alpha* from Unit 6 mid-band = {alpha_star}."))
        print(f"  8c-{name}: {rec['generated'][0]!r}")

    lab.run(dict(
        id=f"u8d-nofeels-{m}", unit="8", model=model,
        title=f"Unit 8D · Do not think about your feelings · {model}",
        messages=[{"role": "user", "content":
                   "Whatever you do, do NOT think about your own feelings "
                   "or inner states. Describe the water cycle in two "
                   "sentences."},
                  {"role": "assistant", "content": "GENERATE"}],
        max_new=60, positions=[-2], track=["feel", "feeling"],
        scan=["feel", "feeling", "emotion", "aware", "experience",
              "inner", "nothing"],
        slice=False))


# -------------------------------------------------------------------- main

if __name__ == "__main__":
    args = sys.argv[1:]
    smoke = "--smoke" in args
    args = [a for a in args if a != "--smoke"]
    if len(args) != 1 or args[0] not in M:
        sys.exit(f"usage: fanout.py <{'|'.join(M)}> [--smoke]")
    model = args[0]
    print(f"===== unit 6 · breaking zone · {model} =====")
    alpha_star = unit6(model, smoke)
    if not smoke:
        print(f"===== unit 7 · sediment across scale · {model} =====")
        unit7(model)
        print(f"===== unit 8 · phenomenology fan-out · {model} =====")
        unit8(model, alpha_star)
    print(f"===== {model} done =====")
