#!/usr/bin/env python3
"""Build the frozen, prose-blind corpus manifest for the 2026-08-08 sweep.

This reads experiment artifacts only. It deliberately does not inspect any
thoughts, plain-language summaries, reports, board state, or handoff prose.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
OUT = Path(__file__).with_name("corpus_manifest.json")


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def normalized_family(record_id: str) -> str:
    """Return a deliberately conservative mechanical family suggestion."""
    stem = re.sub(r"-(?:g4b|g12b|q27b)$", "", record_id)
    stem = re.sub(r"-r[0-9]+$", "", stem)
    stem = re.sub(r"-(?:seed|s)[0-9]+$", "", stem)
    # Preserve dose labels: a dose series is one important adjudication family.
    stem = re.sub(r"-a[0-9]{3,4}$", "-aDOSE", stem)
    return stem


def intervention_summary(params: dict) -> dict | None:
    steer = params.get("steer")
    if not steer:
        return None
    arms = steer if isinstance(steer, list) else [steer]
    clean = []
    for arm in arms:
        if not isinstance(arm, dict):
            clean.append({"shape": type(arm).__name__})
            continue
        clean.append(
            {
                key: arm.get(key)
                for key in ("mode", "words", "layers", "alpha", "rand_seed")
                if key in arm
            }
        )
    return {"arms": clean, "multi": isinstance(steer, list)}


def review_lanes(unit: object, intervention: dict | None) -> list[str]:
    unit = str(unit)
    lanes = []
    if unit in {"0", "1", "2", "3", "4", "5", "6", "7", "14", "15", "16"}:
        lanes.append("foundational")
    if unit in {"5", "6", "8", "9", "11", "13", "18", "apparatus", "audit"} or intervention:
        lanes.append("causal")
    if unit in {"8", "10", "11", "12", "17", "18", "19", "20"}:
        lanes.append("affect")
    return lanes


def calibration_summary(record: dict) -> dict | None:
    rows = record.get("steer_calib")
    if not rows:
        return None
    values = [float(v) for row in rows for v in row.values()]
    return {
        "passes": len(rows),
        "cells": len(values),
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def build_payload() -> dict:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    records = []
    for path in sorted(RESULTS.glob("*/record.json")):
        record = json.loads(path.read_text())
        params = record.get("params") or {}
        model_meta = record.get("model") or {}
        model_name = model_meta.get("name") if isinstance(model_meta, dict) else model_meta
        record_id = record.get("id", path.parent.name)
        film_path = path.parent / "film.json"
        affect_path = RESULTS / f"affect02-{record_id}" / "affect.json"
        generated = record.get("generated")
        conversation = record.get("conversation")
        intervention = intervention_summary(params)
        records.append(
            {
                "id": record_id,
                "anonymous_id": digest(record_id)[:12],
                "mechanical_family": normalized_family(record_id),
                "unit": record.get("unit"),
                "model": model_name,
                "quant": model_meta.get("quant") if isinstance(model_meta, dict) else params.get("quant"),
                "created": record.get("created"),
                "prompt_hash": digest(conversation),
                "generation_hash": digest(generated),
                "generated_chars": len(generated or ""),
                "generated_tokens": max(0, len(record.get("tokens") or []) - params.get("prompt_tokens", 0)),
                "intervention": intervention,
                "review_lanes": review_lanes(record.get("unit"), intervention),
                "steer_calibration": calibration_summary(record),
                "has_film": film_path.exists(),
                "has_vanilla": record.get("vanilla") is not None,
                "has_affect": affect_path.exists(),
                "has_scan": bool(record.get("scan")),
                "has_readouts": bool(record.get("readouts")),
                "record_path": str(path.relative_to(ROOT)),
                "film_path": str(film_path.relative_to(ROOT)) if film_path.exists() else None,
                "affect_path": str(affect_path.relative_to(ROOT)) if affect_path.exists() else None,
            }
        )

    by_unit = Counter(str(row["unit"]) for row in records)
    by_model = Counter(str(row["model"]) for row in records)
    return {
        "schema": 1,
        "snapshot_commit": head,
        "record_count": len(records),
        "result_directory_count": sum(1 for p in RESULTS.iterdir() if p.is_dir()),
        "coverage": {
            "film": sum(row["has_film"] for row in records),
            "vanilla": sum(row["has_vanilla"] for row in records),
            "affect": sum(row["has_affect"] for row in records),
            "steered": sum(row["intervention"] is not None for row in records),
            "calibrated_steer": sum(row["steer_calibration"] is not None for row in records),
        },
        "counts_by_unit": dict(sorted(by_unit.items())),
        "counts_by_model": dict(sorted(by_model.items())),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the saved manifest differs; do not rewrite it",
    )
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit(f"stale manifest: {OUT.relative_to(ROOT)}")
        return
    OUT.write_text(rendered)


if __name__ == "__main__":
    main()
