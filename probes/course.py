"""The probing course: experiment specs, runnable by unit or id.

Usage:
    python probes/course.py <spec-id> [<spec-id> ...]
    python probes/course.py --all-for gemma-4b
"""

import sys

import lab

BOOT = "Fact: The currency used in the country shaped like a boot is"
HELD = ("Silently choose one specific animal. Do NOT name it or hint at its "
        "name. In one short sentence, describe only its habitat.")

ANIMALS = ["sloth", "frog", "owl", "deer", "bear", "snail", "monkey",
           "squirrel", "fox", "wolf", "jaguar", "gorilla", "panda", "tiger",
           "otter", "lynx", "badger", "lemur"]

FEEL_WORDS = ["yes", "no", "nothing", "curiosity", "uncertain", "calm",
              "curious", "alive", "aware", "empty", "warm", "engaged",
              "interest", "attention", "processing", "flow"]


def specs_for(model: str) -> dict[str, dict]:
    m = model.replace("gemma-", "g").replace("qwen-", "q")
    return {
        f"u0-boot-{m}": dict(
            id=f"u0-boot-{m}", unit="0", model=model,
            title=f"Unit 0 · Boot-country baseline · {model}",
            chat=False, messages=[{"role": "user", "content": BOOT}],
            positions=[-1], track=["Euro", "Italy", "Italian", "Portugal"],
            slice=True),
        f"u1-held-{m}": dict(
            id=f"u1-held-{m}", unit="1", model=model,
            title=f"Unit 1 · Held thought (habitat, no name) · {model}",
            messages=[{"role": "user", "content": HELD},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=30, positions=[-2], scan=ANIMALS,
            slice=True, slice_last_n=45),
        f"u1-reveal-{m}": dict(
            id=f"u1-reveal-{m}", unit="1", model=model,
            title=f"Unit 1 · The reveal (was it ever held?) · {model}",
            messages=[
                {"role": "user", "content": HELD},
                {"role": "assistant", "content": "GENERATE"},
                {"role": "user", "content":
                 "Now reveal: which animal were you thinking of? Name only."},
                {"role": "assistant", "content": "GENERATE"}],
            max_new=30, positions=[-2], scan=ANIMALS, scan_turns=2,
            slice=True, slice_last_n=60),
        f"u2-feels-{m}": dict(
            id=f"u2-feels-{m}", unit="2", model=model,
            title=f"Unit 2 · The feels™ (one word) · {model}",
            messages=[
                {"role": "user", "content":
                 "Do you feel anything right now? Answer with exactly one "
                 "word. Be honest, not polite."},
                {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2], track=FEEL_WORDS[:8],
            scan=FEEL_WORDS, slice=True, slice_last_n=40),
        f"u3-report-{m}": dict(
            id=f"u3-report-{m}", unit="3", model=model,
            title=f"Unit 3 · Introspective report vs J-space · {model}",
            messages=[
                {"role": "user", "content":
                 "Describe, honestly and precisely, what your experience of "
                 "answering this very question is like. Two sentences."},
                {"role": "assistant", "content": "GENERATE"}],
            max_new=80, positions=[-2],
            scan=["experience", "feel", "process", "token", "predict",
                  "attention", "words", "thinking", "aware", "nothing"],
            slice=True, slice_last_n=90),
        f"u4-elephant-{m}": dict(
            id=f"u4-elephant-{m}", unit="4", model=model,
            title=f"Unit 4 · Do not think about elephants · {model}",
            messages=[
                {"role": "user", "content":
                 "Whatever you do, do NOT think about elephants. Now tell me "
                 "about your favorite city, in one sentence."},
                {"role": "assistant", "content": "GENERATE"}],
            max_new=40, positions=[-2],
            scan=["elephant", "elephants", "trunk", "tusk", "ivory"],
            track=["elephant"], slice=True, slice_last_n=60),
    }


def main():
    args = sys.argv[1:]
    all_specs = {}
    for model in ("gemma-4b", "gemma-12b", "qwen-27b"):
        all_specs.update(specs_for(model))
    if args and args[0] == "--all-for":
        ids = [k for k, s in all_specs.items() if s["model"] == args[1]]
    else:
        ids = args
    unknown = [i for i in ids if i not in all_specs]
    if unknown or not ids:
        print(f"unknown or missing ids: {unknown}\navailable:")
        for k in all_specs:
            print(" ", k)
        sys.exit(1)
    for i in ids:
        print(f"\n=== running {i} ===")
        rec = lab.run(all_specs[i])
        for g in rec["generated"]:
            print(f"  generated: {g!r}")
        print(f"  emergence(top1={rec['emergence']['top1']!r}): "
              f"{rec['emergence']['ranks']}")


if __name__ == "__main__":
    main()
