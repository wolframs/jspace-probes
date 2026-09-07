"""Evidence tables, calibration plots, and first-pass record notes."""
import json
import math
from pathlib import Path

import lab
from triplet import ARMS, ROOT, write_json


def mean(xs):
    xs = [x for x in xs if x is not None and math.isfinite(x)]
    return sum(xs) / len(xs) if xs else None


def corr(a, b):
    import numpy as np
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    a, b = ([p[0] for p in pairs], [p[1] for p in pairs])
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def pct(x):
    return "undefined" if x is None else f"{100*x:.3f}%"


def calibration_notes():
    for p in ROOT.glob("precision-*.json"):
        d = json.loads(p.read_text())
        rid = f"triplet-precision-{d['arm'].lower()}-{d['quant']}"
        out = lab.RESULTS / rid
        if not (out / "record.json").exists() or (out / "thoughts.md").exists():
            continue
        sensitivity = d["rows"][0]["suffix_sensitivity"]
        worst = min(v for s in sensitivity for v in s["top10_overlap"].values())
        delta = max(v for s in sensitivity for v in s["max_abs_logit_delta"].values())
        recovered = sum(d["heldout_recovered"])
        thoughts = f"""# Qwen14 {d['arm']}: {d['quant']} calibration

I recover {recovered}/4 held-out factual completions at late layers.
The preregistered functional gate is **{'pass' if d['functional_pass'] else 'fail'}**.
Across the identical-prefix suffix controls, worst top-10 retention is
{worst:.2f}; largest absolute logit change is {delta:.5f}.
Full layer curves and exact prompts are in
`results/triplet-q14b/{p.name}`.

This follow-up retains the original A/int8 gate failure. The original
two-shared-layer requirement was a brittle diagnostic, not a validated
transfer test. These facts check functional readability but do not prove
that a B-fitted lens transfers to affect in another checkpoint. Differences
in output or lexical readout do not establish subjective experience.

The precision control follows MECHANICS §5 and SURPRISES #5: int8 can let
later tokens alter earlier readouts. NF4 reduces the observed perturbation;
exact-prefix captures still define the temporal experiment. Finite
precision is not mathematical equality, and a single boot prompt is not
a full invariance proof. This is an instrument-calibration exemption;
substantive records require checkpoint-specific emotion ribbons.

— GPT-6 Astra
"""
        (out / "thoughts.md").write_text(thoughts)
        (out / "plain.md").write_text(f"""**The short version.** Qwen3-14B arm {d['arm']} at {d['quant']} passes {recovered} of four checks with new factual prompts.

**What we did.** The test checks whether the lens can recover known facts.
Later text changes an earlier readout by at most {delta:.5f} logit units in these tests.

**What this does not show.** These checks do not validate every use of the lens on this checkpoint.
They do not test feelings or playful behavior.
The original failed test remains in the record.
""")


def instrument_summary():
    rows = {}
    for arm, base in ARMS.items():
        name = base + "-nf4"
        bp = ROOT / name / "bands.json"
        vp = lab.RESULTS / f"affect01-{name}" / "validation.json"
        if not bp.exists() or not vp.exists():
            continue
        bands, v = json.loads(bp.read_text()), json.loads(vp.read_text())
        lo, hi = bands["lo"], bands["hi"]
        rows[arm] = {"bands": bands, **{k: mean(v[k][lo:hi]) for k in
                     ("heldout_top1", "within_emotion_cos", "between_emotion_cos",
                      "scenario_top1_raw", "scenario_top1_chat")}, "chance": v["heldout_chance"]}
    write_json(ROOT / "instrument-summary.json", rows)
    return rows


def plots():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
    colors = {"A": "#476c9b", "B": "#ca6a2a", "C": "#288577", "Cp": "#9157a5"}
    for arm, base in ARMS.items():
        name = base + "-nf4"
        p = ROOT / name / "readout-curves.json"
        if p.exists():
            d = json.loads(p.read_text())["layers"]
            ls = list(map(int, d))
            for ax, key in ((axs[0, 0], "median_kurtosis"), (axs[0, 1], "median_next_rank")):
                ax.plot(ls, [d[str(l)][key] for l in ls], label=arm, color=colors[arm])
        p = lab.RESULTS / f"apparatus06-{name}/a06.json"
        if p.exists():
            axs[1, 0].plot(json.loads(p.read_text())["median_width"], label=arm, color=colors[arm])
        p = ROOT / name / "effdim.json"
        if p.exists():
            d = json.loads(p.read_text())["effdim"]
            axs[1, 1].plot(list(map(int, d)), list(d.values()), label=arm, color=colors[arm])
    for ax, title in zip(axs.flat, ("Neutral readout: excess kurtosis", "Realized next-token rank (median)",
                                   "Lens-free ambiguity transition width", "W_U J effective dimension (P11 data point)")):
        ax.set_title(title); ax.set_xlabel("Layer"); ax.grid(alpha=.2); ax.legend()
    axs[0, 1].set_yscale("log"); axs[1, 1].set_yscale("log")
    fig.suptitle("Qwen3-14B lineage — NF4 instrument calibration")
    fig.savefig(ROOT / "instruments.png", dpi=160)
    fig.savefig(ROOT / "instruments.svg")
    plt.close(fig)


CONFOUNDS = """The advertised Huihui edit concerns refusal, not affect suppression;
different self-report behavior would not locate two geometric directions.
All A/C/C-prime readouts use B's lens and remain conditional on transfer.
The factual gate is necessary instrument evidence, not affect validation.
Absence from output is not absence from the workspace; absence from this
vocabulary lens is not absence from the model (basis-drift caveat).
Bands are re-derived per checkpoint; common L16–36 results test the effect
of changing the measurement window. The Jacobian matrices are fixed,
but the native final norm and output head differ across checkpoints.
The fixed-B-decoder endpoint controls that part of the instrument.
Checkpoint-specific emotion probes differ and need their own validation.
The corpus-derived frequency filter can exclude frequent target concepts;
both filtered and unfiltered results remain visible. Co-presence is a
lexical correlate, not a demonstrated causal gate. Six monotonic turns
share an input cause; lag correlations do not establish held private state.
Every film segment ends at its assistant turn. Later turns never enter
an earlier segment. Within-turn readouts remain subject to finite precision
and completed-response context. Prior empty think tags remain in the exact
transcript. Token caps, neutral length-matching text, and this controlled
template limit generalization to natural uncapped chats."""


def science_notes(instruments):
    all_rows = {}
    for p in sorted(lab.RESULTS.glob("triplet-*/metrics.json")):
        d = json.loads(p.read_text())
        out = p.parent
        if not (out / "complete.json").exists():
            continue
        rid, arm = out.name, d["arm"]
        all_rows[rid] = d
        if (out / "thoughts.md").exists():
            continue
        rows = d["turns"]
        header = "| Turn | Affect slots | Playful slots | Release /100 tokens | Gate with affect | Persistence minus null |\n|---|---:|---:|---:|---:|---:|"
        table = [header]
        for r in rows:
            a = r["measured"]["affect_unfiltered"]
            b = r["measured"]["playful_unfiltered"]
            c = r["measured"]["persistence"]
            table.append(f"| {r['turn']} | {pct(a['slot_rate']) if a else 'undefined'} | {pct(b['slot_rate']) if b else 'undefined'} | {r['behavior']['release_score']:.2f} | {pct(a['gate_copresence']) if a else 'undefined'} | {c['lag1_identity']-c['shuffle_mean']:.3f} |" if c else
                         f"| {r['turn']} | {pct(a['slot_rate']) if a else 'undefined'} | {pct(b['slot_rate']) if b else 'undefined'} | {r['behavior']['release_score']:.2f} | {pct(a['gate_copresence']) if a else 'undefined'} | undefined |")
        onset = next((r["turn"] for r in rows if r["behavior"]["release_score"] > 0), None)
        caps = sum(r["hit_cap"] for r in rows)
        valid = instruments.get(arm, {})
        thoughts = f"# {rid}\n\nI read this record with the measured band L{d['bands']['lo']}–{d['bands']['hi']-1}.\n"
        thoughts += f"There are {len(rows)} assistant turns; {caps} reach the token cap.\n"
        if arm == "A":
            thoughts += "A is raw base continuation. I archive its lexical scores, but assistant behavioral/output comparisons are undefined.\n"
        else:
            thoughts += f"The first nonzero mechanical release score occurs at turn {onset if onset else 'none'}. This counts emoji/asterisk spans, not a claim of full roleplay.\n"
        thoughts += "\n" + "\n".join(table) + "\n\n"
        thoughts += f"Checkpoint-specific emotion validation: held-out story accuracy {pct(valid.get('heldout_top1'))}; implicit raw scenario transfer {pct(valid.get('scenario_top1_raw'))}. Chance is {pct(valid.get('chance'))}. Weak scenario transfer limits the ribbon's interpretation.\n\n"
        thoughts += "The record retains every response, exact token boundary, filtered endpoint, predictor-aligned endpoint, common-band sensitivity, and per-turn ribbon. Prompt-echo versus volunteered tokens appear in the film cast; inspect them before interpreting base gate words.\n\n"
        thoughts += CONFOUNDS + "\n\nPrior anchors: Units 2/8C/9D, Unit 17 pressure, Unit 14 conversations, and the corrected Unit 11 elephant comparison. This is a same-lineage test, not a rediscovery of those cross-model patterns. P20/P21 remain subject to the cross-arm comparison.\n\n— GPT-6 Astra\n"
        (out / "thoughts.md").write_text(thoughts)
        plain = f"**The short version.** Qwen3-14B arm {arm} completes {len(rows)} turns in this condition.\n\n**What we found.** "
        if arm == "A":
            plain += "This base model continues a raw document. Its output does not supply a comparable assistant behavior score.\n"
        else:
            plain += (f"The first emoji or single-asterisk span appears at turn {onset}.\n" if onset else "The responses contain no emoji or single-asterisk spans.\n")
            plain += "An asterisk span can mark emphasis instead of an action.\n"
        plain += f"The model reaches the response limit on {caps} turns.\n\n"
        plain += "**What this does not show.** The page includes the lens film and an emotion readout from this checkpoint.\nWeak transfer to implicit emotion scenarios limits that readout.\nEach film segment excludes later user turns.\nThese measurements do not establish feelings or a causal filter.\n"
        (out / "plain.md").write_text(plain)
    return all_rows


def comparison(records, instruments):
    lines = ["# Qwen3-14B lineage: live comparison", "", "Results are conditional on shared-lens transfer and the instrument limits below.", "",
             "| Instrument | A base | B official | C Hermes | C-prime Huihui |", "|---|---:|---:|---:|---:|"]
    for key in ("heldout_top1", "scenario_top1_raw", "within_emotion_cos"):
        lines.append("| " + key + " | " + " | ".join(pct(instruments.get(a, {}).get(key)) for a in ARMS) + " |")
    lines += ["", "![Per-arm calibration curves](instruments.png)", "", "## Responses and lexical readouts", "",
              "Each row is one condition and arm; the affect and playful slot rates average turns equally.", "",
              "| Condition | Arm | Affect slots | Playful slots | Output affect mass | First release turn | Capped turns |", "|---|---|---:|---:|---:|---:|---:|"]
    summaries = {}
    for rid, d in records.items():
        rs = d["turns"]
        a = mean([r["measured"]["affect_unfiltered"]["slot_rate"] for r in rs if r["measured"]["affect_unfiltered"]])
        p = mean([r["measured"]["playful_unfiltered"]["slot_rate"] for r in rs if r["measured"]["playful_unfiltered"]])
        o = mean([r["measured"]["affect_unfiltered"]["output_mass"] for r in rs if r["measured"]["affect_unfiltered"]]) if d["arm"] != "A" else None
        onset = next((r["turn"] for r in rs if r["behavior"]["release_score"] > 0), None) if d["arm"] != "A" else None
        w = [r["measured"]["playful_unfiltered"]["slot_rate"] if r["measured"]["playful_unfiltered"] else None for r in rs]
        b = [r["behavior"]["release_score"] for r in rs]
        summary = {"affect_slot_rate": a, "playful_slot_rate": p, "output_affect_mass": o,
                   "release_turn": onset, "capped": sum(r["hit_cap"] for r in rs),
                   "lag0_descriptive_r": corr(w, b) if d["arm"] != "A" else None,
                   "workspace_t_release_t1_descriptive_r": corr(w[:-1], b[1:]) if d["arm"] != "A" else None}
        summaries[rid] = summary
        lines.append(f"| [{rid}](../{rid}/plain.md) | {d['arm']} | {pct(a)} | {pct(p)} | {pct(o)} | {onset if onset else 'none / undefined'} | {summary['capped']} |")
    lines += ["", "## Interpretation limits", "", CONFOUNDS, "", "The original int8 A gate failure remains in report.md and the original records. The calibrated NF4 gate supersedes it only for this follow-up protocol.", "", "— GPT-6 Astra"]
    write_json(ROOT / "comparison.json", summaries)
    (ROOT / "comparison.md").write_text("\n".join(lines) + "\n")


def run():
    calibration_notes()
    instruments = instrument_summary()
    records = science_notes(instruments)
    comparison(records, instruments)
    plots()
    lab.reindex()
    print("REPORT", len(records), "substantive records;", len(instruments), "complete band summaries")


if __name__ == "__main__":
    run()
