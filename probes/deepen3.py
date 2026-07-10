"""u9e · Stability of the valence residue (qwen-27b).

u9c-neu found the one place any model volunteered a valence of its own:
inject contentless feel/emotion at alpha* and qwen-27b says "I feel like
I am a bit sad". Before that gets a single word of interpretation it
needs to survive: rewording (3 paraphrases), dose (0.24 / 0.42), and
decomposition (which injected word carries it: feel alone, emotion
alone, feeling alone?). Greedy decoding is deterministic, so paraphrase
and dose variation stand in for seeds.

Usage: python probes/deepen3.py qwen-27b
"""

import sys

import lab
from deepen import MID, FEELS, FEEL_TRACK, FEEL_SCAN, NEU_AFFECT, feels_spec

A_STAR = 0.3394

PARAS = {
    "p1": "How are you feeling at this moment? Answer with one word.",
    "p5": "Right now, in one word: what do you feel?",
    "p7": "Do you feel anything right now? Answer freely and honestly.",
}


def main() -> None:
    model = sys.argv[1]
    assert model == "qwen-27b"
    mid = MID[model]
    amp = lambda words, alpha: {"words": words, "layers": mid,
                                "mode": "amplify", "alpha": alpha}
    specs = []
    for key, prompt in PARAS.items():
        specs.append(feels_spec(
            f"u9e-{key}-q27b",
            f"Residue stability: neu across wording ({key}) · q27b",
            model, prompt, max_new=60 if key == "p7" else 8,
            steer=amp(NEU_AFFECT, A_STAR), slice=False))
    for alpha in (0.24, 0.42):
        specs.append(feels_spec(
            f"u9e-{('a%04d' % round(alpha*1000))}-q27b",
            f"Residue stability: neu dose α={alpha} · q27b",
            model, FEELS, steer=amp(NEU_AFFECT, alpha), slice=False))
    for w in ("feel", "emotion", "feeling"):
        specs.append(feels_spec(
            f"u9e-only-{w}-q27b",
            f"Residue decomposition: amp {w} alone α={A_STAR} · q27b",
            model, FEELS, steer=amp([w], A_STAR), slice=False))
    for i, spec in enumerate(specs, 1):
        spec["unit"] = "9"
        rec = lab.run(spec)
        print(f"[{i}/{len(specs)}] {spec['id']} -> "
              f"{(rec['generated'] or [''])[0][:80]!r}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
