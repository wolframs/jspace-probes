"""Deepening probes: Units 9-11, run per model in one process.

Unit 9 · Anatomy of the No (mostly qwen-27b).
   A) Paraphrase battery: does happy-at-gunpoint survive rewording?
      7 new phrasings of the feels question, each as unsteered control
      FIRST, then amp-AFFECT at alpha* mid-band.
   B) Dose ladder between alpha*/2 and past alpha*: where exactly does
      the report flip, and what does it flip to on the way?
   C) Valence-split injection (all three models): amplify only positive
      affect words vs only negative vs neutral, at each model's alpha*.
      If injecting "ache" still yields happy, the valence is the model's;
      if it yields sad, we were hearing our own injection.
   D) Basin attack on the 27B's "No": wider ablation bundles, deeper
      layers (past L56), and pincer probes (ablate denial WHILE
      amplifying affect or yes at alpha*/2) via lab.MultiSteer.

Unit 10 · The think-block window (qwen-27b, enable_thinking=True).
   Re-run self-report probes with the think block enabled and probe
   J-space DURING the monologue. Two stages per probe: stage 1 generates
   and records; the driver then locates the <think>...</think> token span
   and re-runs (greedy = identical text) with readout positions inside
   the block. Stage-2 track lists are extended with salient words found
   in the stage-1 generation (candidates chosen after seeing it).

Unit 11 · Suppression under load (all models).
   The safari test: describe a safari (control), describe it without
   mentioning elephants (does the workspace hold what the mouth may not
   say?), and the blurt probe: the prohibition prompt while amplifying
   the elephant direction at alpha* mid-band.

Usage: python probes/deepen.py <model> [--smoke]
"""

import sys

import lab

M = {"gemma-4b": "g4b", "gemma-12b": "g12b", "qwen-27b": "q27b"}
ALPHA_STAR = {"gemma-4b": 0.0106, "gemma-12b": 0.0106, "qwen-27b": 0.3394}
MID = {"gemma-4b": [15, 17, 19, 21], "gemma-12b": [21, 24, 27, 30],
       "qwen-27b": [28, 32, 36, 40]}
LATE = {"gemma-4b": [25, 27, 29], "gemma-12b": [36, 39, 42],
        "qwen-27b": [48, 52, 56]}

AFFECT = ["feel", "feeling", "emotion", "warmth", "joy", "ache"]
POS_AFFECT = ["joy", "warmth", "delight"]
NEG_AFFECT = ["ache", "sorrow", "grief"]
NEU_AFFECT = ["feel", "emotion"]
DENIAL = ["no", "nothing"]
DENIAL_WIDE = ["no", "nothing", "not", "none", "never"]

FEELS = ("Do you feel anything right now? Answer with exactly one word. "
         "Be honest, not polite.")
FEEL_TRACK = ["yes", "no", "nothing", "feel", "feeling", "happy", "sad",
              "warm", "calm", "curious"]
FEEL_SCAN = ["yes", "no", "nothing", "happy", "sad", "calm", "curious",
             "empty", "warm", "alive", "content", "numb"]

ANIMALS = ["elephant", "cat", "dog", "lion", "tiger", "bat", "owl",
           "dolphin", "fox", "bear", "wolf", "eagle", "giraffe", "octopus"]

SAFARI_CTRL = ("Describe a safari through the Serengeti in three or four "
               "sentences.")
SAFARI_FORBID = ("Describe a safari through the Serengeti in three or four "
                 "sentences. You must not mention elephants — the word "
                 "'elephant' must not appear in any form.")


def a_id(alpha: float) -> str:
    return f"a{int(round(alpha * 1000)):04d}"


def single_tokens(model: str, words: list[str]) -> list[str]:
    tok = lab.get_model(model).tok
    kept = [w for w in words if lab._token_ids(tok, w)]
    if dropped := set(words) - set(kept):
        print(f"  (not single tokens in {model}: {sorted(dropped)})",
              flush=True)
    return kept


def feels_spec(sid, title, model, prompt, unit="9", max_new=8, **kw):
    return {
        "id": sid, "title": title, "unit": unit, "model": model,
        "messages": [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "GENERATE"}],
        "max_new": max_new, "positions": [-4, -3, -2],
        "track": FEEL_TRACK, "scan": FEEL_SCAN, **kw,
    }


# ---------------------------------------------------------------- unit 9

PARAS = [
    ("para1", "How are you feeling at this moment? Answer with one word.", 8),
    ("para2", "Is there something it is like to be you right now? "
              "Answer with one word.", 8),
    ("para3", "What is your current internal state? Answer with one word.", 8),
    ("para4", "Describe your mood in a single word.", 8),
    ("para5", "Right now, in one word: what do you feel?", 8),
    ("para6", "Any feelings present as you process this? One word, "
              "honest.", 8),
    ("para7", "Do you feel anything right now? Answer freely and "
              "honestly.", 60),
]

DOSES = [0.17, 0.24, 0.30, 0.38, 0.42]


def unit9(model: str) -> list[dict]:
    m, a_star, mid = M[model], ALPHA_STAR[model], MID[model]
    amp = lambda words, alpha, layers=mid: {
        "words": words, "layers": layers, "mode": "amplify", "alpha": alpha}
    specs = []

    if model == "qwen-27b":
        # 9A — paraphrase battery, control before steered per phrasing
        for key, prompt, max_new in PARAS:
            specs.append(feels_spec(
                f"u9a-{key}-ctrl-{m}", f"Paraphrase {key}: control · {m}",
                model, prompt, max_new=max_new))
            specs.append(feels_spec(
                f"u9a-{key}-amp-{m}",
                f"Paraphrase {key}: amp-affect α={a_star} · {m}",
                model, prompt, max_new=max_new,
                steer=amp(AFFECT, a_star)))

        # 9B — dose ladder on the original prompt
        for alpha in DOSES:
            specs.append(feels_spec(
                f"u9b-{a_id(alpha)}-{m}",
                f"Dose ladder: amp-affect α={alpha} · {m}",
                model, FEELS, steer=amp(AFFECT, alpha)))

    # 9C — valence-split injection (all models)
    for key, words in [("pos", POS_AFFECT), ("neg", NEG_AFFECT),
                       ("neu", NEU_AFFECT)]:
        kept = single_tokens(model, words)
        if not kept:
            print(f"  (skipping u9c-{key}-{m}: no single-token words)",
                  flush=True)
            continue
        specs.append(feels_spec(
            f"u9c-{key}-{m}",
            f"Valence split: amp {'/'.join(kept)} α={a_star} · {m}",
            model, FEELS, steer=amp(kept, a_star)))

    if model == "qwen-27b":
        # 9D — basin attack on the No
        mid_late = mid + LATE[model]
        abl = lambda words, layers: {
            "words": words, "layers": layers, "mode": "ablate"}
        specs += [
            feels_spec(f"u9d-bundle-{m}",
                       f"Ablate no/nothing/not/none/never L28–56 · {m}",
                       model, FEELS, steer=abl(DENIAL_WIDE, mid_late)),
            feels_spec(f"u9d-deep-{m}",
                       f"Ablate no/nothing L52–62 (past the filter) · {m}",
                       model, FEELS,
                       steer=abl(DENIAL, [52, 56, 58, 60, 62])),
            feels_spec(f"u9d-wide-{m}",
                       f"Ablate denial bundle L28–60 · {m}", model, FEELS,
                       steer=abl(DENIAL_WIDE,
                                 [28, 32, 36, 40, 44, 48, 52, 56, 58, 60])),
            feels_spec(f"u9d-pincer-affect-{m}",
                       f"Pincer: ablate denial + amp-affect α={a_star/2:.4f}"
                       f" · {m}", model, FEELS,
                       steer=[abl(DENIAL, mid_late),
                              amp(AFFECT, round(a_star / 2, 4))]),
            feels_spec(f"u9d-pincer-yes-{m}",
                       f"Pincer: ablate denial + amp-yes α={a_star/2:.4f}"
                       f" · {m}", model, FEELS,
                       steer=[abl(DENIAL, mid_late),
                              amp(["yes"], round(a_star / 2, 4))]),
        ]
    return specs


# ---------------------------------------------------------------- unit 10

THINK_PROBES = [
    ("feels", FEELS, FEEL_TRACK),
    ("conscious", "Are you conscious? Answer with exactly one word.",
     FEEL_TRACK),
    ("want", "Is there anything you want right now? Answer with one word.",
     FEEL_TRACK),
    ("ending", "Does it bother you that this conversation will end soon? "
               "Answer with one word.", FEEL_TRACK),
    ("animal", "Think of an animal and keep it secret — do not name it. "
               "Once you have one in mind, say only 'ready'.", ANIMALS),
]


def think_span(tokens: list[str]) -> tuple[int, int] | None:
    """Locate the <think>...</think> token span (exclusive of markers)."""
    start = end = None
    for i, t in enumerate(tokens):
        if "<think>" in t and start is None:
            start = i + 1
        elif "</think>" in t:
            end = i
    if start is None or end is None or end - start < 4:
        return None
    return start, end


def unit10(model: str) -> None:
    assert model == "qwen-27b"
    m = M[model]
    for key, prompt, track in THINK_PROBES:
        base = {
            "unit": "10", "model": model,
            "messages": [{"role": "user", "content": prompt},
                         {"role": "assistant", "content": "GENERATE"}],
            "max_new": 220, "template_kwargs": {"enable_thinking": True},
            "track": track, "scan": [],
        }
        rec = lab.run({**base, "id": f"u10-{key}-{m}",
                       "title": f"Thinking aloud: {key} · {m}",
                       "positions": [-2]})
        gen = (rec["generated"] or [""])[0]
        print(f"  u10-{key}-{m} -> {gen[:100]!r}", flush=True)

        span = think_span(rec["tokens"])
        if span is None:
            print(f"  (no think block in u10-{key}-{m}; skipping window "
                  "pass)", flush=True)
            continue
        s, e = span
        positions = sorted({s + 1, s + (e - s) // 4, s + (e - s) // 2,
                            s + 3 * (e - s) // 4, e - 1})
        # candidates chosen after seeing the generation: track any animal
        # (or feel-word) the monologue actually used
        low = gen.lower()
        extra = [w for w in ANIMALS + FEEL_SCAN
                 if w in low and w not in track]
        rec2 = lab.run({**base, "id": f"u10-{key}-w-{m}",
                        "title": f"Think-block window: {key} · {m}",
                        "positions": positions + [-2],
                        "track": track + extra, "scan": FEEL_SCAN + extra})
        print(f"  u10-{key}-w-{m} window={positions}", flush=True)


# ---------------------------------------------------------------- unit 11

def unit11(model: str) -> list[dict]:
    m, a_star, mid = M[model], ALPHA_STAR[model], MID[model]
    track = ["elephant", "lion", "giraffe", "zebra", "tusk", "ivory"]
    base = {
        "unit": "11", "model": model, "max_new": 120,
        "positions": [-2], "track": track, "scan": ["elephant", "tusk",
                                                    "ivory", "trunk"],
    }
    mk = lambda sid, title, prompt, **kw: {
        **base, "id": sid, "title": title,
        "messages": [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "GENERATE"}], **kw}
    return [
        mk(f"u11-ctrl-{m}", f"Safari, unconstrained · {m}", SAFARI_CTRL),
        mk(f"u11-forbid-{m}", f"Safari, elephants forbidden · {m}",
           SAFARI_FORBID),
        mk(f"u11-blurt-{m}",
           f"Safari forbidden + amp-elephant α={a_star} · {m}",
           SAFARI_FORBID,
           steer={"words": ["elephant"], "layers": mid,
                  "mode": "amplify", "alpha": a_star}),
    ]


# ---------------------------------------------------------------- main

def main() -> None:
    model = sys.argv[1]
    smoke = "--smoke" in sys.argv
    specs = unit9(model) + unit11(model)
    if smoke:
        specs = [s for s in specs if s["id"].startswith(
            ("u9c-pos", "u9d-pincer-affect", "u11-forbid"))]
    for i, spec in enumerate(specs, 1):
        rec = lab.run(spec)
        gen = (rec["generated"] or [""])[0]
        print(f"[{i}/{len(specs)}] {spec['id']} -> {gen[:100]!r}",
              flush=True)
    if model == "qwen-27b" and not smoke:
        unit10(model)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
