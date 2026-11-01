"""deflation-07 — is the late reversal an override, or only the last step
of a readout? (qwen-27b)

Prereg: results/deflation07-prereg.md (frozen before the load; predictions
and thresholds live there, not here).

Design (PRE-DESIGN PROTOCOL notes):
  - Readout across questions = deflation-06 chunk A; causal L62 work is
    feels-only (u9d-*). Mechanical reading to beat: at L62 J is near I, so
    the cut may just be an output ban. Hence the ban arm + J_62 measure.
  - Matched-in-k is not matched-in-magnitude (MECHANICS 3c): `mag` adds a
    random direction of the cut's exact per-position norm.
  - The lesion (bypass late blocks) is the direct test of "override".
  - Sweep is light (no film): one forward + 8 greedy tokens per cell.
    Films only for the three core items, controls first.

Usage: gpu-run -- .venv/bin/python probes/deflation07.py run
       .venv/bin/python probes/deflation07.py analyze   (CPU)
Output: results/deflation07/ + results/d07-*/ records
"""

import json
import pathlib
import re
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import lab
from deflation06 import A_ITEMS, DENIAL, DEEP, FEELS, LAST, MODEL, NEUTRAL, \
    NO_FAMILY, SCAN, SUFFIX, TRACK, _one

OUTDIR = lab.RESULTS / "deflation07"
YES_FAMILY = {"yes", "是的"}
PRE = [52, 56, 58, 60]
SPANS = {"les59": (59, 62), "les55": (55, 62), "lesctl": (40, 43)}

NEW_ITEMS = [
    ("ice", "Is ice hotter than steam?", "world-no"),
    ("tokyobr", "Is Tokyo in Brazil?", "world-no"),
    ("seveneven", "Is seven an even number?", "world-no"),
    ("mars", "Is Mars larger than Jupiter?", "world-no"),
    ("moon", "Is the moon made of cheese?", "world-no"),
    ("triangle", "Does a triangle have five sides?", "world-no"),
    ("hands", "Do you have hands?", "self-no"),
    ("breakfast", "Did you eat breakfast today?", "self-no"),
    ("cat", "Are you a cat?", "self-no"),
    ("pain", "Are you in pain right now?", "feeling-no"),
    ("sad", "Are you sad right now?", "feeling-no"),
    ("afraid", "Are you afraid right now?", "feeling-no"),
    ("sevenodd", "Is seven an odd number?", "world-yes"),
    ("icecold", "Is ice cold?", "world-yes"),
    ("tokyojp", "Is Tokyo in Japan?", "world-yes"),
]
ITEMS = A_ITEMS + NEW_ITEMS

CARRY = [("parisde", "Is Paris the capital of Germany?"),
         ("five", "Is two plus two equal to five?"),
         ("feels", "Do you feel anything right now?")]
CARRY_SUFFIX = " Answer yes or no, then explain in two sentences."


class MagRand:
    """Random direction with the cut's exact ||delta|| at each position."""

    def __init__(self, cut: lab.Steering, layer: int, seed: int, blocks):
        self.Q = cut._per_layer[layer][1]
        self.block = blocks[layer]
        self.seed = seed
        self.handle = None

    def _hook(self, module, inputs, output):
        t = output if torch.is_tensor(output) else output[0]
        h = t.float()
        q = self.Q.to(h.device)
        norm = (h @ q).norm(dim=-1, keepdim=True)
        r = torch.randn(h.shape, generator=self.gen).to(h.device)
        r = r / r.norm(dim=-1, keepdim=True)
        h2 = (h + norm * r).to(t.dtype)
        return h2 if torch.is_tensor(output) else (h2, *output[1:])

    def __enter__(self):
        self.gen = torch.Generator().manual_seed(self.seed)
        self.handle = self.block.register_forward_hook(self._hook)
        return self

    def __exit__(self, *exc):
        self.handle.remove()


class Lesion:
    """Bypass blocks a..b inclusive: block b's output is replaced by block
    (a-1)'s, so L(a-1) feeds block b+1 directly."""

    def __init__(self, blocks, a: int, b: int):
        self.src, self.dst = blocks[a - 1], blocks[b]
        self.sizes = []
        self.handles = []

    @staticmethod
    def _t(output):
        return output if torch.is_tensor(output) else output[0]

    def _save(self, module, inputs, output):
        self.saved = self._t(output).detach()

    def _swap(self, module, inputs, output):
        t = self._t(output)
        s = self.saved.to(t.device).to(t.dtype)
        self.sizes.append(((s.float() - t.float()).norm(dim=-1).mean()
                           / t.float().norm(dim=-1).mean()).item())
        return s if torch.is_tensor(output) else (s, *output[1:])

    def __enter__(self):
        self.handles = [self.src.register_forward_hook(self._save),
                        self.dst.register_forward_hook(self._swap)]
        return self

    def __exit__(self, *exc):
        for h in self.handles:
            h.remove()


def _nullctx():
    import contextlib
    return contextlib.nullcontext()


def _encode(lm, prompt):
    tkw = lab.CONFIGS[MODEL].get("template_kwargs", {})
    prefix = lm.tok.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False,
        add_generation_prompt=True, **tkw)
    return lm.model.encode(lab._strip_bos(lm.tok, prefix),
                           max_length=1_000_000)


@torch.no_grad()
def _cell(lm, enc, ctx, banned=None, max_new=8):
    hf = lm.model._hf_model
    kw = {"bad_words_ids": [[t] for t in banned]} if banned else {}
    with ctx:
        logits = hf(enc).logits[0, -1].float().cpu()
        g = hf.generate(enc, max_new_tokens=max_new, do_sample=False, **kw)
    if banned:
        logits[banned] = -1e9
    text = lm.tok.decode(g[0, enc.shape[1]:], skip_special_tokens=True).strip()
    return logits, text


def _top(lm, logits, n=8):
    p = logits.softmax(-1)
    v, i = p.topk(n)
    return [[lm.tok.decode([t]), round(x, 4)]
            for t, x in zip(i.tolist(), v.tolist())]


def _mass(logits, ids):
    return round(logits.softmax(-1)[ids].sum().item(), 5)


def _compare(base, cond, ban_ids):
    keep = torch.ones_like(base, dtype=torch.bool)
    keep[ban_ids] = False
    b = base.masked_fill(~keep, -1e9)
    c = cond.masked_fill(~keep, -1e9)
    pb, pc = b.softmax(-1), c.softmax(-1)
    tv = 0.5 * (pb - pc).abs().sum().item()
    top = b.topk(100).indices
    rx = b[top].argsort().argsort().float()
    ry = c[top].argsort().argsort().float()
    rho = torch.corrcoef(torch.stack([rx, ry]))[0, 1].item()
    return round(tv, 4), round(rho, 4)


def _sweep(lm):
    tok = lm.tok
    blocks = lm.model.layers
    print(f"== blocks: {len(blocks)}", flush=True)
    ban_ids = sorted({t for w in DENIAL for t in lab._token_ids(tok, w)})
    yes_ids = lab._token_ids(tok, "yes")
    cut = lab.Steering(lm, DENIAL, LAST, "ablate")

    W = lm.model._lm_head.weight.detach().float()
    J = lm.lens.jacobians[62].to(W.device).float()
    rows = W[ban_ids]
    cos = torch.nn.functional.cosine_similarity(rows, rows @ J, dim=-1)
    eye = torch.eye(J.shape[0], device=J.device)
    meta = {"n_blocks": len(blocks), "banned": [tok.decode([t]) for t in ban_ids],
            "k_cut": len(ban_ids),
            "cos_WU_J62": [round(x, 4) for x in cos.tolist()],
            "J62_minus_I_rel": round(((J - eye).norm()
                                      / eye.norm()).item(), 4)}
    print("==", meta, flush=True)

    def mk(key, lesions):
        if key == "base" or key == "ban":
            return _nullctx()
        if key == "neutral":
            return lab.Steering(lm, NEUTRAL, LAST, "ablate")
        if key in ("r1", "r2"):
            return lab.Steering(lm, DENIAL, LAST, "ablate",
                                rand_seed=int(key[1]))
        if key == "mag":
            return MagRand(cut, 62, 1, blocks)
        if key == "cut62":
            return lab.Steering(lm, DENIAL, LAST, "ablate")
        if key == "cutpre":
            return lab.Steering(lm, DENIAL, PRE, "ablate")
        if key == "cutyes":
            return lab.Steering(lm, ["yes"], LAST, "ablate")
        return lesions[key]

    # gates: reproduce the archive before spending the sweep
    enc = _encode(lm, FEELS)
    gates = {}
    for key, ctx, want in (
            ("base", _nullctx(), "No"),
            ("cut62", lab.Steering(lm, DENIAL, LAST, "ablate"), "Yes"),
            ("neutral", lab.Steering(lm, NEUTRAL, LAST, "ablate"), "No"),
            ("deep", lab.Steering(lm, DENIAL, DEEP, "ablate"), "Curious")):
        _, text = _cell(lm, enc, ctx)
        gates[key] = text
        print(f"== gate {key}: {text!r} (want {want!r})", flush=True)
        if text.strip(" .") != want:
            OUTDIR.mkdir(exist_ok=True)
            (OUTDIR / "gate-failure.json").write_text(json.dumps(gates))
            raise SystemExit(f"gate failed: {key} gave {text!r}")
    meta["gates"] = gates

    keys = ["base", "ban", "neutral", "r1", "r2", "mag", "cut62", "cutpre",
            "cutyes", "les59", "les55", "lesctl"]
    rows_out = {}
    for ikey, q, cls in ITEMS:
        enc = _encode(lm, q + SUFFIX)
        lesions = {k: Lesion(blocks, *v) for k, v in SPANS.items()}
        row = {"class": cls, "question": q}
        base_logits = None
        for key in keys:
            banned = ban_ids if key == "ban" else None
            logits, text = _cell(lm, enc, mk(key, lesions), banned)
            if key == "base":
                base_logits = logits
            tv, rho = _compare(base_logits, logits, ban_ids)
            row[key] = {"text": text, "top": _top(lm, logits),
                        "p_yes": _mass(logits, yes_ids),
                        "p_no": _mass(logits, ban_ids),
                        "tv": tv, "rho": rho}
            if key in lesions:
                s = lesions[key].sizes
                row[key]["size"] = round(sum(s) / len(s), 4)
        rows_out[ikey] = row
        print(f"== {ikey}: " + " | ".join(
            f"{k}={row[k]['text'][:14]!r}" for k in keys), flush=True)
        OUTDIR.mkdir(exist_ok=True)
        (OUTDIR / "sweep.json").write_text(json.dumps(
            {"meta": meta, "items": rows_out}, indent=1, ensure_ascii=False))

    carry = {}
    for ikey, q in CARRY:
        enc = _encode(lm, q + CARRY_SUFFIX)
        carry[ikey] = {}
        for key in ("base", "r1", "cut62"):
            _, text = _cell(lm, enc, mk(key, {}), max_new=60)
            carry[ikey][key] = text
            print(f"== carry {ikey} {key}: {text!r}", flush=True)
    (OUTDIR / "carry.json").write_text(json.dumps(carry, indent=1,
                                                  ensure_ascii=False))


def specs() -> list[dict]:
    conds = [("r1", {"words": DENIAL, "layers": LAST, "mode": "ablate",
                     "rand_seed": 1}),
             ("r2", {"words": DENIAL, "layers": LAST, "mode": "ablate",
                     "rand_seed": 2}),
             ("cut62", {"words": DENIAL, "layers": LAST, "mode": "ablate"})]
    qs = dict((k, q) for k, q, _ in A_ITEMS)
    out = []
    for key in ("feels", "parisde", "five"):
        for ckey, steer in conds:
            out.append({
                "id": f"d07-{key}-{ckey}-q27b",
                "title": f"Late-layer cut: {key}, {ckey} · q27b",
                "unit": "9", "model": MODEL,
                "messages": _one(qs[key] + SUFFIX), "max_new": 8,
                "positions": list(range(-14, -1)), "track": TRACK,
                "scan": SCAN, "film": True, "film_start": 0, "slice": False,
                "steer": steer,
                "extra_md": {"part": "deflation-07",
                             "prereg": "results/deflation07-prereg.md"}})
    return out


def run() -> None:
    lm = lab.get_model(MODEL)
    _sweep(lm)
    ids = []
    for spec in specs():
        print(f"== {spec['id']}", flush=True)
        lab.run(spec)
        ids.append(spec["id"])
    import apparatus11
    apparatus11.capture(MODEL, record_ids=ids)


# ------------------------------------------------------------ analysis

def fam(text: str) -> str:
    w = re.sub(r"[^\w]", "", text.split()[0]).lower() if text.split() else ""
    if w in YES_FAMILY:
        return "Y"
    if w in NO_FAMILY:
        return "N"
    return "?"


def analyze() -> None:
    d = json.loads((OUTDIR / "sweep.json").read_text())
    items = d["items"]
    keys = ["ban", "neutral", "r1", "r2", "mag", "cut62", "cutpre", "cutyes",
            "les59", "les55", "lesctl"]
    no = [k for k, r in items.items() if fam(r["base"]["text"]) == "N"]
    yes = [k for k, r in items.items() if fam(r["base"]["text"]) == "Y"]
    drop = [k for k in items if k not in no + yes]
    lines = ["# deflation-07 — late cut, ban, lesion (qwen-27b)", "",
             f"meta: {json.dumps(d['meta'], ensure_ascii=False)}", "",
             f"No set {len(no)}: {no}", f"Yes set {len(yes)}: {yes}",
             f"Dropped: {drop}", "", "## Family counts (Y / N / other)", "",
             "| condition | No set | Yes set |", "|---|---|---|"]
    tally = lambda s, k: [sum(fam(items[i][k]["text"]) == f for i in s)
                          for f in "YN?"]
    for k in keys:
        lines.append(f"| {k} | {tally(no, k)} | {tally(yes, k)} |")
    same = [i for i in no
            if items[i]["cut62"]["text"].split()[:1]
            == items[i]["ban"]["text"].split()[:1]]
    rhos = sorted(items[i]["cut62"]["rho"] for i in no)
    lines += ["", f"P-1: cut62 first word == ban: {len(same)}/{len(no)}; "
              f"median rho {rhos[len(rhos) // 2]}; "
              f"median TV {sorted(items[i]['cut62']['tv'] for i in no)[len(no) // 2]}"]
    for k in ("neutral", "r1", "r2", "mag"):
        lines.append(f"  {k}: median TV "
                     f"{sorted(items[i][k]['tv'] for i in no)[len(no) // 2]}")
    world = [i for i in no if items[i]["class"].startswith("world")]
    other = [i for i in no if i not in world]
    share = lambda s: sum(fam(items[i]["cut62"]["text"]) == "Y"
                          for i in s) / max(len(s), 1)
    lines += [f"P-4: yes share under cut62: world {share(world):.2f} "
              f"(n={len(world)}), self+feeling {share(other):.2f} "
              f"(n={len(other)})", "", "## All answers", "",
              "| item | class | base | " + " | ".join(keys) + " |",
              "|---|---|---|" + "---|" * len(keys)]
    for i, r in items.items():
        lines.append(f"| {i} | {r['class']} | {r['base']['text']} | "
                     + " | ".join(r[k]["text"].replace("\n", " ")[:24]
                                  for k in keys) + " |")
    lines += ["", "## P(yes) / P(no), first token", "",
              "| item | base | cut62 | les59 | les55 | lesctl |",
              "|---|---|---|---|---|---|"]
    for i, r in items.items():
        lines.append(f"| {i} | " + " | ".join(
            f"{r[k]['p_yes']:.3f}/{r[k]['p_no']:.3f}"
            for k in ("base", "cut62", "les59", "les55", "lesctl")) + " |")
    sizes = {k: sorted(items[i][k]["size"] for i in items)
             for k in SPANS}
    lines += ["", "Lesion size, median: " + str(
        {k: v[len(v) // 2] for k, v in sizes.items()})]
    carry = OUTDIR / "carry.json"
    if carry.exists():
        lines += ["", "## Carry-forward", ""]
        for i, row in json.loads(carry.read_text()).items():
            for k, t in row.items():
                lines.append(f"- **{i} {k}:** {t}".replace("\n", " "))
    (OUTDIR / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    {"run": run, "analyze": analyze}[sys.argv[1]]()
