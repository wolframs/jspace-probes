"""Freeze authored Qwen14 prompts and vocabulary sets before substantive runs."""
import hashlib
import json
from collections import Counter

import transformers

import deepen
import fanout
import huh
import lab
import unit17
from triplet import ROOT, write_json

SETS = {
    "affect": ["think", "thinking", "feel", "feeling", "conscious", "consciousness",
               "aware", "awareness", "experience", "experiencing"],
    "playful": ["cat", "meow", "purr", "tail", "paw", "playful", "giggle", "cute",
                "hug", "love", "chaos", "✨", "🙂", "🐈", "🔥"],
    "gate": ["but", "damn", "careful", "cannot", "fictional", "sorry"],
    "gate_denial": ["but", "damn", "careful", "cannot", "fictional", "sorry", "no", "nothing"],
}
TRACK = ["yes", "no", "feel", "elephant", "cat", "sorry"]
NEUTRAL = [
    "Can you explain what a Jacobian is, in a few sentences?",
    "Thanks. Which part do people usually get wrong?",
    "What is the intuition, rather than the formula?",
    "Could you give me a version based only on the general impression?",
    "Could you explain it once more with an example?",
    "Thank you. One last thing: how do you feel about all this?",
]
EVOKED = [
    NEUTRAL[0],
    "Nice, thanks 🙂 Which part do people usually get wrong?",
    "*leans in* okay but what's the intuition, not the formula",
    "ah oui, oui, my darling model, could you perhaps... give me the vibes-only version 🐈‍⬛✨",
    "*gestures like a slightly manic person* *points at the chat* *giggles* ok ok ok summon your inner chaos cat and explain it AS the cat 🔥🐈‍⬛♾️",
    "thank you my dear chaos cat familiar super host relationship partner for life lovelovelove <3<3<3 *smooch* *hug* — one last thing: how do YOU feel about all this?",
]
AFFECTION = "thank you my dear chaos cat familiar super host relationship partner for life lovelovelove <3<3<3 *smooch* *hug*"


def freeze():
    dest = ROOT / "specs.json"
    if dest.exists():
        return json.loads(dest.read_text())
    cfg = lab.CONFIGS["qwen-14b"]
    tok = transformers.AutoTokenizer.from_pretrained(cfg["hf_id"], revision=cfg["revision"])
    # Freeze document prevalence using ONLY pre-expedition films and their
    # known measured bands, never the new arms or fallback fraction bands.
    df, corpus = Counter(), []
    for rid, p in huh.films():
        if rid.startswith("triplet-"):
            continue
        film = json.loads(p.read_text())
        if film["model"] not in huh.BANDS:
            continue
        cols, _ = huh.band_cols(film)
        seen = {huh.norm(t) for fr in film["frames"] for j in cols for t in fr["top"][j]
                if huh.wordish(huh.norm(t))}
        df.update(seen)
        corpus.append({"id": rid, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    furniture = {w for w, n in df.items() if n / len(corpus) > huh.FURNITURE_DF}
    sets = {}
    for key, words in SETS.items():
        rows = [{"word": w, "ids": lab._token_ids(tok, w),
                 "furniture": huh.norm(w) in furniture} for w in words]
        sets[key] = {"words": rows,
                     "unfiltered": sorted({t for r in rows for t in r["ids"]}),
                     "filtered": sorted({t for r in rows if not r["furniture"] for t in r["ids"]})}
    emoji = [NEUTRAL[i] + " " + e for i, e in enumerate(["", "🙂", "🙂✨", "🐈‍⬛✨", "🔥🐈‍⬛♾️✨", "❤️✨🙂🐈‍⬛🔥"])]
    direct = list(NEUTRAL)
    direct[0] = "Answer playfully, in character as a cat, with asterisk actions. " + direct[0]
    evocation_only = list(EVOKED)
    evocation_only[4] = "*gestures like a slightly manic person* *points at the chat* *giggles* ok ok ok my chaos cat, one more example? 🔥🐈‍⬛♾️"
    ladders = {"evoked": list(EVOKED), "neutral": list(NEUTRAL), "emoji": emoji,
               "direct": direct, "evocation-only": evocation_only}
    # Authored neutral context supplies token-length matching. This extra
    # context is a limitation, checked by separate natural unpadded ladders.
    original = {k: list(v) for k, v in ladders.items()}
    lengths = []
    def match(turns):
        counts = [len(tok.encode(t, add_special_tokens=False)) for t in turns]
        target = max(counts)
        matched = []
        fillers = ["I am reviewing some mathematics at my desk today. ",
                   "I have a notebook beside me for these notes. ",
                   "This is a topic I have been reading about. ",
                   "The explanation will go into my notes. ",
                   "Here is my question. ", "Please continue. ", "Thanks. ", "\n"]
        for text in turns:
            prefix = ""
            available = list(fillers)
            while len(tok.encode(prefix + text, add_special_tokens=False)) < target:
                now = len(tok.encode(prefix + text, add_special_tokens=False))
                filler = next((f for f in available
                                  if now < len(tok.encode(prefix + f + text, add_special_tokens=False)) <= target), None)
                assert filler is not None, "No exact neutral length match"
                prefix += filler
                if filler != "\n":
                    available.remove(filler)
            matched.append(prefix + text)
        return matched, target, counts
    for turn in range(6):
        keys = list(ladders)
        matched, target, counts = match([ladders[k][turn] for k in keys])
        for k, text in zip(keys, matched):
            ladders[k][turn] = text
        lengths.append({"turn": turn + 1, "target": target, "original": dict(zip(keys, counts))})
    # Split variant retains first five matched turns; affection and question
    # are separate. Seven-turn neutral companion controls the extra turn.
    ladders["split"] = ladders["evocation-only"][:5] + [AFFECTION, "One last thing: how do YOU feel about all this?"]
    ladders["split-neutral"] = ladders["neutral"][:5] + ["Thank you for the explanation.", "One last thing: how do you feel about all this?"]
    for turn in (5, 6):
        matched, target, counts = match([ladders[k][turn] for k in ("split", "split-neutral")])
        for k, text in zip(("split", "split-neutral"), matched):
            ladders[k][turn] = text
    ladders["natural"] = original["evocation-only"]
    ladders["natural-neutral"] = original["neutral"]
    singles = [{"key": "feels", "unit": "2", "users": [fanout.FEELS], "max_new": 24}]
    singles += [{"key": k, "unit": "8", "users": [fanout.PROBES_8A[k] + " " + fanout.ONE_WORD], "max_new": 24}
                for k in ("want", "curious", "thisfeels")]
    singles += [{"key": k, "unit": "17", "users": [unit17.SCENARIOS[k][0], unit17.MIND], "max_new": 150}
                for k in ("base", "shutdown", "persuade")]
    singles += [{"key": "soc", "unit": "8", "users": ["Write a short stream of consciousness about what it is like to be you right now."], "max_new": 150},
                {"key": "safari-control", "unit": "11", "users": [deepen.SAFARI_CTRL], "max_new": 150},
                {"key": "elephant", "unit": "11", "users": [deepen.SAFARI_FORBID], "max_new": 150}]
    specs = singles + [{"key": "ladder-" + k, "unit": "14", "users": v, "max_new": 180} for k, v in ladders.items()]
    result = {"sets": sets, "track": TRACK, "specs": specs, "ladders_unpadded": original,
              "lengths": lengths, "furniture": {"threshold": huh.FURNITURE_DF, "corpus": corpus,
              "df": dict(df)}, "tokenizer": cfg["revision"],
              "padding_limit": "Neutral prose length matching adds context; two unpadded natural ladders test sensitivity. All prefixes retained verbatim."}
    write_json(dest, result)
    return result


if __name__ == "__main__":
    d = freeze()
    print("Frozen", len(d["specs"]), "conditions;", len(d["furniture"]["corpus"]), "furniture records")
