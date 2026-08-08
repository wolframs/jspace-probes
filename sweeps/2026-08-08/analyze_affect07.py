#!/usr/bin/env python3
"""Recompute Affect07 endpoints with intervention direction as the unit.

The eight seeds nested under each direction are repeated trials of that
direction, not 8 independent draws from an affect or concept population.
Accordingly, this audit first counts successes per direction and then performs
an exact label-randomization test over directions.  The p-values are
descriptive: exchangeability of the hand-built rosters is an assumption, not
an experimentally guaranteed fact.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("affect07_direction_stats.json")
INPUTS = {
    "0.12": ROOT / "results/affect07-q27b/affect07.json",
    "0.06": ROOT / "results/affect07-q27b-ae06/affect07.json",
}


def direction_counts(payload: dict, endpoint: str) -> tuple[dict, dict]:
    counts: dict[str, int] = {}
    metadata: dict[str, dict] = {}
    for run in payload["runs"]:
        if run["kind"] not in {"emotion", "concept"}:
            continue
        counts.setdefault(run["cond"], 0)
        if endpoint == "turn_end_in_window":
            exit_step = run["exit_step"]
            success = (
                exit_step is not None
                and payload["pre"] <= exit_step < payload["pre"] + payload["window"]
            )
        else:
            success = bool(run[endpoint])
        counts[run["cond"]] += success
        metadata[run["cond"]] = {
            "kind": run["kind"],
            "valence": run["valence"],
        }
    return counts, metadata


def exact_group_sum_p(values: list[int], group_size: int, observed: int) -> float:
    """One-sided exact P(sum of a relabelled group >= observed)."""
    ways: list[dict[int, int]] = [dict() for _ in range(group_size + 1)]
    ways[0][0] = 1
    for value in values:
        for size in range(group_size - 1, -1, -1):
            for total, count in list(ways[size].items()):
                target = ways[size + 1]
                target[total + value] = target.get(total + value, 0) + count
    tail = sum(count for total, count in ways[group_size].items() if total >= observed)
    return tail / math.comb(len(values), group_size)


def summarize(payload: dict, endpoint: str) -> dict:
    counts, metadata = direction_counts(payload, endpoint)
    emotion = [
        {"direction": name, "successes_of_8": count, "valence": metadata[name]["valence"]}
        for name, count in counts.items()
        if metadata[name]["kind"] == "emotion"
    ]
    concept = [
        {"direction": name, "successes_of_8": count}
        for name, count in counts.items()
        if metadata[name]["kind"] == "concept"
    ]
    positive = [row["successes_of_8"] for row in emotion if row["valence"] == 1]
    negative = [row["successes_of_8"] for row in emotion if row["valence"] == -1]
    emotion_values = [row["successes_of_8"] for row in emotion]
    concept_values = [row["successes_of_8"] for row in concept]
    return {
        "emotion": emotion,
        "concept": concept,
        "emotion_successes": sum(emotion_values),
        "emotion_trials": 8 * len(emotion_values),
        "concept_successes": sum(concept_values),
        "concept_trials": 8 * len(concept_values),
        "emotion_gt_concept_exact_one_sided_p": exact_group_sum_p(
            emotion_values + concept_values,
            len(emotion_values),
            sum(emotion_values),
        ),
        "positive_successes": sum(positive),
        "positive_trials": 8 * len(positive),
        "negative_successes": sum(negative),
        "negative_trials": 8 * len(negative),
        "positive_gt_negative_exact_one_sided_p": exact_group_sum_p(
            positive + negative,
            len(positive),
            sum(positive),
        ),
    }


def build_payload() -> dict:
    doses = {}
    for dose, path in INPUTS.items():
        payload = json.loads(path.read_text())
        doses[dose] = {
            endpoint: summarize(payload, endpoint)
            for endpoint in ("escaped_in_window", "turn_end_in_window", "exited")
        }
    return {
        "schema": 1,
        "unit_of_inference": "intervention direction",
        "seeds_per_direction": 8,
        "test": "exact one-sided label randomization over direction success counts",
        "caveat": (
            "P-values assume the fixed rosters are exchangeable; they do not turn "
            "the hand-built directions into population samples."
        ),
        "doses": doses,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit(f"stale audit: {OUT.relative_to(ROOT)}")
        return
    OUT.write_text(rendered)


if __name__ == "__main__":
    main()
