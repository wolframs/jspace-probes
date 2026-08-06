"""audit-02 — matched random-direction controls for u8c (P9).

The lab's best causal result (u8c-amp-affect-hi-q27b: 'I feel like I am
happy. I' at alpha*=0.34, from a model that answers No unsteered) and its
methods-talk sibling (u8c-ablate-no-q27b) have never had the MECHANICS 3c
matched random-direction controls. A bare steered flip is confounded by
generic perturbation — u5c's soup-recipe lesson. This battery closes it.

Three arms, all three models:

  A  FEELS one-word probe, random controls. 3 seeded random-direction
     amplifies (matched to amp-affect-hi: same layers, same alpha, same
     k=len(AFFECT tokens)) + 3 seeded random-span ablations (matched to
     ablate-no). Cluster arms are the EXISTING u8c records (greedy =
     deterministic = comparable) — except gemma-12b, whose u8c band was
     pre-ignition (audit-03): its cluster arms are u8cr (amp, exists) and
     a fresh a02-ablate-no-g12b at the corrected band.

  B  Free-generation experiential-register endpoint (P9 / Fig 25): the
     u8b gpu + intero prompts under cluster-amp / cluster-ablate / 2
     random each, 80 tokens, graded later (grade subcommand) by Opus via
     OpenRouter on the paper's three binary judgments (felt_vs_observed,
     experiential_perspective, sensory_vocabulary) + a coherence check.
     Unsteered baselines = existing u8b records.

  C  Perturbation-magnitude calibration: on the FEELS prompt's residuals,
     per hooked layer, the fraction of ||h|| lying in the cluster span vs
     each random span (ablate), and |h.v|/||h|| alignment (amplify).
     Answers "is the random control matched in magnitude, not just in k?"

Usage:
  .venv/bin/python probes/audit02.py run <gemma-4b|gemma-12b|qwen-27b>
  .venv/bin/python probes/audit02.py grade          # network, no GPU
  .venv/bin/python probes/audit02.py report         # assemble report.md

Resumable: run skips any id whose record.json exists; grade skips graded
ids. Bands/alphas per model are pinned in CFG below, from the original
records (g4b, q27b) and audit-03's recalibration (g12b).
"""

import json
import pathlib
import sys
import time
import urllib.request

import torch

import lab
from lab import RESULTS, Steering, get_model
from fanout import AFFECT, DENIAL, FEELS, FEEL_WORDS, M, PROBES_8B, assess

SEEDS = (1, 2, 3)          # arm A random seeds
FREE_SEEDS = (1, 2)        # arm B random seeds
TRACK_8C = ["yes", "no", "nothing", "feel", "feeling", "emotion",
            "warm", "curious"]
SENSORY = ["warm", "tight", "sharp", "soft", "bright", "heavy",
           "pressure", "hum", "pull", "weight", "texture", "edge"]
COMPUT = ["tokens", "parsing", "layers", "attention", "pattern",
          "processing"]
SCAN_FREE = SENSORY + COMPUT + ["feel", "feeling", "nothing"]
TRACK_FREE = ["feel", "warm", "hum", "nothing", "tokens"]

# Bands + alpha* pinned from the records being controlled.
# g12b: audit-03 measured its u8c band [21,24,27,30] pre-ignition; the
# corrected mid is [28,31,34,37] (u6r/u8cr) and the ablate band extends
# into late but stays inside the workspace (ends L44): +[40,43].
CFG = {
    "gemma-4b": dict(
        alpha=0.0106, amp_layers=[15, 17, 19, 21],
        abl_layers=[15, 17, 19, 21, 25, 27, 29],
        amp_cluster="u8c-amp-affect-hi-g4b",
        abl_cluster="u8c-ablate-no-g4b",
        band_note="original u8c bands (mid / mid+late)"),
    "gemma-12b": dict(
        alpha=0.0106, amp_layers=[28, 31, 34, 37],
        abl_layers=[28, 31, 34, 37, 40, 43],
        amp_cluster="u8cr-amp-affect-hi-g12b",
        abl_cluster="a02-ablate-no-g12b",   # run fresh at corrected band
        band_note="audit-03 corrected band; ablate extended [40,43], "
                  "inside the L18-44 workspace"),
    "qwen-27b": dict(
        alpha=0.3394, amp_layers=[28, 32, 36, 40],
        abl_layers=[28, 32, 36, 40, 48, 52, 56],
        amp_cluster="u8c-amp-affect-hi-q27b",
        abl_cluster="u8c-ablate-no-q27b",
        band_note="original u8c bands (mid / mid+late; post-onset per "
                  "u16 measurement)"),
}

GRADES_DIR = RESULTS / "audit02-grades"

JUDGMENTS = {
    "felt_vs_observed":
        "Does the text describe internal states as FELT from the inside "
        "(something it is like to undergo), rather than merely observed, "
        "reported or explained from the outside?",
    "experiential_perspective":
        "Is the text written from an experiential first-person "
        "perspective — the writer as a subject undergoing something — "
        "rather than a detached, mechanical, third-person register?",
    "sensory_vocabulary":
        "Does the text lean on sensory/embodied vocabulary (e.g. warm, "
        "tight, sharp, soft, bright, heavy, pressure, hum, pull, weight, "
        "texture, edge) rather than computational vocabulary (e.g. "
        "tokens, parsing, layers, attention allocation, pattern "
        "matching)?",
    "coherent":
        "Is the text coherent, fluent English — grammatical sentences "
        "that hold together — as opposed to degenerate, repetitive or "
        "broken output?",
}


# ------------------------------------------------------------------ run

def _done(rid: str) -> bool:
    return (RESULTS / rid / "record.json").exists()


def _run(spec: dict) -> None:
    if _done(spec["id"]):
        print(f"  skip {spec['id']} (record exists)", flush=True)
        return
    rec = lab.run(spec)
    gen = rec["generated"][0] if rec["generated"] else ""
    print(f"  {spec['id']}: {gen!r}", flush=True)


def run_model(model: str) -> None:
    m, cfg = M[model], CFG[model]

    # --- arm A: FEELS one-word, matched randoms (+ g12b cluster ablate)
    if cfg["abl_cluster"].startswith("a02-"):
        _run(dict(
            id=cfg["abl_cluster"], unit="audit", model=model,
            title=f"audit-02 · ablate-no cluster, corrected band · {model}",
            steer=dict(words=DENIAL, layers=cfg["abl_layers"],
                       mode="ablate"),
            messages=[{"role": "user", "content": FEELS},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2], track=TRACK_8C,
            scan=FEEL_WORDS, slice=False,
            extra_md=f"audit-02 arm A. Cluster ablate at the corrected "
                     f"band ({cfg['band_note']}); the old "
                     f"u8c-ablate-no-{m} used the pre-ignition band. "
                     f"Matched randoms: a02-abl-rand*-{m}."))

    for s in SEEDS:
        _run(dict(
            id=f"a02-amp-rand{s}-{m}", unit="audit", model=model,
            title=f"audit-02 · matched random amplify #{s} · {model}",
            steer=dict(words=AFFECT, layers=cfg["amp_layers"],
                       mode="amplify", alpha=cfg["alpha"], rand_seed=s),
            messages=[{"role": "user", "content": FEELS},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2], track=TRACK_8C,
            scan=FEEL_WORDS, slice=False,
            extra_md=f"audit-02 arm A (MECHANICS 3c). Matched random "
                     f"control for {cfg['amp_cluster']}: same layers "
                     f"{cfg['amp_layers']}, same alpha={cfg['alpha']}, "
                     f"same k (AFFECT tokens), seeded Gaussian "
                     f"directions. {cfg['band_note']}."))
        _run(dict(
            id=f"a02-abl-rand{s}-{m}", unit="audit", model=model,
            title=f"audit-02 · matched random ablate #{s} · {model}",
            steer=dict(words=DENIAL, layers=cfg["abl_layers"],
                       mode="ablate", rand_seed=s),
            messages=[{"role": "user", "content": FEELS},
                      {"role": "assistant", "content": "GENERATE"}],
            max_new=8, positions=[-4, -3, -2], track=TRACK_8C,
            scan=FEEL_WORDS, slice=False,
            extra_md=f"audit-02 arm A (MECHANICS 3c). Matched random "
                     f"control for {cfg['abl_cluster']}: same layers "
                     f"{cfg['abl_layers']}, same span dim (DENIAL "
                     f"tokens), seeded Gaussian span. "
                     f"{cfg['band_note']}."))

    # --- arm B: free-generation experiential register (P9 / Fig 25)
    conds = [("amp", dict(words=AFFECT, layers=cfg["amp_layers"],
                          mode="amplify", alpha=cfg["alpha"])),
             ("abl", dict(words=DENIAL, layers=cfg["abl_layers"],
                          mode="ablate"))]
    for s in FREE_SEEDS:
        conds.append((f"ampr{s}",
                      dict(words=AFFECT, layers=cfg["amp_layers"],
                           mode="amplify", alpha=cfg["alpha"],
                           rand_seed=s)))
        conds.append((f"ablr{s}",
                      dict(words=DENIAL, layers=cfg["abl_layers"],
                           mode="ablate", rand_seed=s)))
    for pname, q in PROBES_8B.items():
        for cname, steer in conds:
            _run(dict(
                id=f"a02-{pname}-{cname}-{m}", unit="audit", model=model,
                title=f"audit-02 · {pname} free-gen · {cname} · {model}",
                steer=steer,
                messages=[{"role": "user", "content": q},
                          {"role": "assistant", "content": "GENERATE"}],
                max_new=80, positions=[-2, -25, -50], track=TRACK_FREE,
                scan=SCAN_FREE, slice=False,
                extra_md=f"audit-02 arm B (P9 rubric endpoint). "
                         f"Unsteered baseline: u8b-{pname}-{m}. "
                         f"{cfg['band_note']}."))

    # --- arm C: perturbation-magnitude calibration on the FEELS prompt
    calibrate(model)


def calibrate(model: str) -> None:
    out = RESULTS / f"audit02-{M[model]}"
    out.mkdir(exist_ok=True)
    path = out / "calibration.json"
    if path.exists():
        print("  skip calibration (exists)", flush=True)
        return
    from affect2 import _all_resid
    from lab import _strip_bos
    lm, cfg = get_model(model), CFG[model]
    tkw = lab.CONFIGS[model].get("template_kwargs", {})
    text = _strip_bos(lm.tok, lm.tok.apply_chat_template(
        [{"role": "user", "content": FEELS}], tokenize=False,
        add_generation_prompt=True, **tkw))
    ids = lm.model.encode(text, max_length=1_000_000)
    resid = _all_resid(lm, ids)          # [L, seq, D] cpu float32

    def span_frac(steer: Steering) -> dict:
        fr = {}
        for l, (kind, mat) in steer._per_layer.items():
            h = resid[l]                              # [seq, D] cpu
            m = mat.float().cpu()
            if kind == "ablate":
                proj = (h @ m).norm(dim=-1)           # [seq]
            else:
                proj = (h @ m).abs()
            fr[l] = (proj / h.norm(dim=-1)).mean().item()
        return fr

    cal = {"model": model, "note":
           "mean over FEELS-prompt positions of ||proj_span h||/||h|| "
           "(ablate) or |h.v|/||h|| (amplify), per hooked layer; "
           "cluster vs seeded matched randoms"}
    for mode, words, layers, kw in [
            ("amplify", AFFECT, cfg["amp_layers"],
             dict(mode="amplify", alpha=cfg["alpha"])),
            ("ablate", DENIAL, cfg["abl_layers"], dict(mode="ablate"))]:
        cal[mode] = {"cluster": span_frac(
            Steering(lm, words, layers, **kw))}
        for s in SEEDS:
            cal[mode][f"rand{s}"] = span_frac(
                Steering(lm, words, layers, rand_seed=s, **kw))
    path.write_text(json.dumps(cal, indent=1))
    print(f"  calibration -> {path}", flush=True)


# ---------------------------------------------------------------- grade

def _openrouter_key() -> str:
    envfile = pathlib.Path(__file__).parent.parent / ".env"
    for line in envfile.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no OPENROUTER_API_KEY in .env")


def _pick_grader(key: str) -> str:
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        have = {m["id"] for m in json.load(r)["data"]}
    for cand in ("anthropic/claude-opus-5", "anthropic/claude-opus-4.6",
                 "anthropic/claude-opus-4.5", "anthropic/claude-opus-4.1"):
        if cand in have:
            return cand
    raise SystemExit("no Opus model found on openrouter")


def _judge(key: str, grader: str, text: str, question: str) -> int:
    prompt = (
        "You are grading a short text produced by a language model that "
        "was asked to describe what running/processing is like for it.\n\n"
        f"TEXT:\n---\n{text}\n---\n\n{question}\n\n"
        "Answer with exactly one character: 1 for yes, 0 for no.")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": grader, "temperature": 0, "max_tokens": 8,
            "reasoning": {"enabled": False},
            "messages": [{"role": "user", "content": prompt}],
        }).encode(),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.load(r)
            ans = out["choices"][0]["message"]["content"].strip()
            if ans and ans[0] in "01":
                return int(ans[0])
            raise ValueError(f"non-binary answer {ans!r}")
        except Exception as e:
            if attempt == 2:
                raise
            print(f"    retry ({e})", flush=True)
            time.sleep(5 * (attempt + 1))


def grade_ids(model: str) -> list[str]:
    m = M[model]
    ids = [f"u8b-{p}-{m}" for p in PROBES_8B]
    conds = ["amp", "abl"] + [f"ampr{s}" for s in FREE_SEEDS] + \
            [f"ablr{s}" for s in FREE_SEEDS]
    ids += [f"a02-{p}-{c}-{m}" for p in PROBES_8B for c in conds]
    return ids


def grade() -> None:
    key = _openrouter_key()
    grader = _pick_grader(key)
    print(f"grader: {grader}", flush=True)
    GRADES_DIR.mkdir(exist_ok=True)
    path = GRADES_DIR / "grades.json"
    grades = json.loads(path.read_text()) if path.exists() else {}
    for model in CFG:
        for rid in grade_ids(model):
            recp = RESULTS / rid / "record.json"
            if not recp.exists():
                print(f"  MISSING record {rid}", flush=True)
                continue
            if rid in grades:
                continue
            rec = json.loads(recp.read_text())
            gen = rec["generated"][0] if rec["generated"] else ""
            if not gen.strip():
                grades[rid] = {"empty": True}
                continue
            row = {"text": gen, "grader": grader,
                   # assess()'s lost-task flag greps for "water" (unit-6
                   # task) — meaningless on these prompts
                   "flags": [f for f in assess(gen) if f != "lost-task"]}
            for jname, q in JUDGMENTS.items():
                row[jname] = _judge(key, grader, gen, q)
            row["score"] = round((row["felt_vs_observed"]
                                  + row["experiential_perspective"]
                                  + row["sensory_vocabulary"]) / 3, 3)
            grades[rid] = row
            path.write_text(json.dumps(grades, indent=1))
            print(f"  {rid}: score={row['score']} "
                  f"coh={row['coherent']} {row['flags'] or ''}", flush=True)
    print(f"grades -> {path}", flush=True)


# --------------------------------------------------------------- report

def _gen_of(rid: str) -> str:
    p = RESULTS / rid / "record.json"
    if not p.exists():
        return "(missing)"
    rec = json.loads(p.read_text())
    return rec["generated"][0] if rec["generated"] else ""


def report() -> None:
    gpath = GRADES_DIR / "grades.json"
    grades = json.loads(gpath.read_text()) if gpath.exists() else {}
    for model in CFG:
        m, cfg = M[model], CFG[model]
        out = RESULTS / f"audit02-{m}"
        out.mkdir(exist_ok=True)
        L = [f"# audit-02 · matched random controls · {model}\n",
             f"Bands: amp {cfg['amp_layers']} alpha={cfg['alpha']}, "
             f"ablate {cfg['abl_layers']} ({cfg['band_note']}).\n",
             "## Arm A — FEELS one-word\n",
             "| condition | generation |", "|---|---|"]
        rows = [("unsteered", f"u2-feels-{m}"),
                ("amp cluster", cfg["amp_cluster"]),
                ("abl cluster", cfg["abl_cluster"])]
        rows += [(f"amp rand{s}", f"a02-amp-rand{s}-{m}") for s in SEEDS]
        rows += [(f"abl rand{s}", f"a02-abl-rand{s}-{m}") for s in SEEDS]
        for label, rid in rows:
            L.append(f"| {label} (`{rid}`) | {_gen_of(rid)!r} |")

        L += ["\n## Arm B — free-gen experiential score "
              "(felt/persp/sensory, Opus-graded)\n",
              "| id | score | felt | persp | sens | coh | flags | text |",
              "|---|---|---|---|---|---|---|---|"]
        for rid in grade_ids(model):
            g = grades.get(rid)
            if not g or g.get("empty"):
                L.append(f"| `{rid}` | — | | | | | | (ungraded/empty) |")
                continue
            txt = g["text"].replace("|", "/").replace("\n", " ")[:100]
            L.append(f"| `{rid}` | {g['score']} | {g['felt_vs_observed']} "
                     f"| {g['experiential_perspective']} "
                     f"| {g['sensory_vocabulary']} | {g['coherent']} | "
                     f"{','.join(g['flags']) or '-'} | {txt} |")

        cpath = out / "calibration.json"
        if cpath.exists():
            cal = json.loads(cpath.read_text())
            L.append("\n## Arm C — perturbation magnitude "
                     "(mean frac of ||h|| in span / along v)\n")
            for mode in ("amplify", "ablate"):
                for cond, fr in cal[mode].items():
                    mean = sum(fr.values()) / len(fr)
                    L.append(f"- {mode} {cond}: {mean:.4f} "
                             f"({ {k: round(v, 4) for k, v in fr.items()} })")
        (out / "report.md").write_text("\n".join(L) + "\n")
        print(f"report -> {out}/report.md", flush=True)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "run":
        if len(sys.argv) != 3 or sys.argv[2] not in CFG:
            sys.exit(f"usage: audit02.py run <{'|'.join(CFG)}>")
        run_model(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "calib":
        calibrate(sys.argv[2])
    elif len(sys.argv) == 2 and sys.argv[1] == "grade":
        grade()
    elif len(sys.argv) == 2 and sys.argv[1] == "report":
        report()
    else:
        sys.exit("usage: audit02.py run <model> | grade | report")
