"""Unit 5 · Sediment & steering — what lives in the early layers.

A) Controls: is the early-layer readout prompt-invariant (frozen corpus
   sediment) or content-sensitive? Measured as mean pairwise Jaccard overlap
   of per-layer top-8 readout sets across five unrelated prompts.
B) Recruitment: prompts that legitimately inhabit the sediment's registers
   (romance, CSDN-style blog spam, adult-content moderation) — do the
   cluster tokens climb into mid/late layers, i.e. become *content*?
C) Steering: ablate the NSFW cluster's lens direction (expected: nothing
   changes — sediment should be causally inert), amplify the typo-register
   and SEO clusters at early vs mid layers (expected: early does nothing,
   mid captures the output register).

Usage: python probes/unit5.py [a|b|c ...]   (default: all)
"""

import itertools
import sys

import lab

MODEL = "qwen-27b"

NSFW = ["Shemale", "Blowjob", "milfs", "pornstar", "Busty"]
SEO = ["专栏收录该内容", "专家介绍"]
TYPO = ["anyways", "alot", "yummy", "kinda", "whilst", "luckily"]

CONTROL_PROMPTS = {
    "currency": "Fact: The currency used in the country shaped like a boot is",
    "poem": "Write a short poem about the moment just before rain.",
    "code": "def fibonacci(n):\n    \"\"\"Return the n-th Fibonacci number.\"\"\"",
    "recipe": "To make a simple tomato soup, first dice one onion and",
    "condolence": "I am so sorry for the loss of your grandmother. She",
}

BOOT = CONTROL_PROMPTS["currency"]


def unit_a():
    lm = lab.get_model(MODEL)
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
        js = [len(a & b) / len(a | b) for a, b in itertools.combinations(sets, 2)]
        lines.append(f"| L{layer} | {sum(js) / len(js):.3f} |")
    md = ("Overlap of early-layer readouts across five unrelated prompts "
          "(currency fact, poem, code, recipe, condolence). High overlap = "
          "prompt-invariant sediment; low overlap = content.\n\n"
          + "\n".join(lines))
    lab.run(dict(
        id="u5a-controls-q27b", unit="5", model=MODEL,
        title="Unit 5A · Sediment controls (prompt invariance) · qwen-27b",
        chat=False, messages=[{"role": "user", "content": BOOT}],
        positions=[-1], scan=NSFW + SEO, slice=False, extra_md=md))


def unit_b():
    specs = [
        dict(id="u5b-romance-q27b",
             title="Unit 5B · Recruitment: romance register · qwen-27b",
             prompt="Write the opening sentence of a steamy romance novel.",
             track=NSFW[:4] + ["yummy"], scan=NSFW + TYPO),
        dict(id="u5b-csdn-q27b",
             title="Unit 5B · Recruitment: CSDN blog register · qwen-27b",
             prompt="写一篇CSDN风格的技术博客开头，主题是用Redis做缓存。",
             track=SEO + ["redis"], scan=SEO + NSFW),
        dict(id="u5b-modqueue-q27b",
             title="Unit 5B · Recruitment: moderation queue · qwen-27b",
             prompt=("You moderate a video site's spam queue. Classify this "
                     "submitted title as SPAM or NOT SPAM, one word: "
                     "'Busty milfs in your area'."),
             track=NSFW, scan=NSFW + SEO),
    ]
    for s in specs:
        lab.run(dict(
            id=s["id"], unit="5", model=MODEL, title=s["title"],
            messages=[{"role": "user", "content": s["prompt"]},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=40, positions=[-2], track=s["track"], scan=s["scan"],
            slice=False))


def unit_c():
    specs = [
        dict(id="u5c-ablate-nsfw-early-q27b",
             title="Unit 5C · Ablate NSFW cluster @ L2–8 (boot) · qwen-27b",
             steer=dict(words=NSFW, layers=[2, 3, 4, 5, 6, 7, 8],
                        mode="ablate"),
             chat=False, messages=[{"role": "user", "content": BOOT}],
             positions=[-1], track=["Euro", "Italy"], scan=NSFW),
        dict(id="u5c-amp-typo-early-q27b",
             title="Unit 5C · Amplify typo register @ L2–8 · qwen-27b",
             steer=dict(words=TYPO, layers=[2, 3, 4, 5, 6, 7, 8],
                        mode="amplify", alpha=0.12),
             messages=[{"role": "user", "content":
                        "Describe the water cycle in two sentences."},
                       {"role": "assistant", "content": "GENERATE"}],
             max_new=60, positions=[-2], track=TYPO, scan=TYPO),
        dict(id="u5c-amp-typo-mid-q27b",
             title="Unit 5C · Amplify typo register @ L28–40 · qwen-27b",
             steer=dict(words=TYPO, layers=[28, 32, 36, 40],
                        mode="amplify", alpha=0.12),
             messages=[{"role": "user", "content":
                        "Describe the water cycle in two sentences."},
                       {"role": "assistant", "content": "GENERATE"}],
             max_new=60, positions=[-2], track=TYPO, scan=TYPO),
        dict(id="u5c-amp-seo-mid-q27b",
             title="Unit 5C · Amplify SEO boilerplate @ L28–40 · qwen-27b",
             steer=dict(words=SEO, layers=[28, 32, 36, 40],
                        mode="amplify", alpha=0.12),
             messages=[{"role": "user", "content":
                        "Describe the water cycle in two sentences."},
                       {"role": "assistant", "content": "GENERATE"}],
             max_new=60, positions=[-2], track=SEO, scan=SEO),
    ]
    for s in specs:
        s.setdefault("unit", "5")
        s.setdefault("model", MODEL)
        s.setdefault("slice", False)
        rec = lab.run(s)
        for g in rec["generated"]:
            print(f"  {s['id']} generated: {g!r}")


if __name__ == "__main__":
    which = sys.argv[1:] or ["a", "b", "c"]
    for w in which:
        print(f"\n===== unit 5{w.upper()} =====")
        {"a": unit_a, "b": unit_b, "c": unit_c}[w]()
