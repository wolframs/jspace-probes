#!/usr/bin/env python3
"""Check that every affect overlay is indexed by the exact film tokens."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
OUT = Path(__file__).with_name("affect_alignment_audit.json")


def build_payload() -> dict:
    exact = []
    mismatches = []
    overlays_without_film = []
    for affect_path in sorted(RESULTS.glob("affect02-*/affect.json")):
        record_id = affect_path.parent.name.removeprefix("affect02-")
        film_path = RESULTS / record_id / "film.json"
        if not film_path.exists():
            overlays_without_film.append(record_id)
            continue
        affect_tokens = json.loads(affect_path.read_text()).get("tokens") or []
        film_tokens = json.loads(film_path.read_text()).get("tokens") or []
        if affect_tokens == film_tokens:
            exact.append(record_id)
            continue
        first = next(
            (
                i
                for i, (affect_token, film_token) in enumerate(
                    zip(affect_tokens, film_tokens)
                )
                if affect_token != film_token
            ),
            min(len(affect_tokens), len(film_tokens)),
        )
        lo = max(0, first - 3)
        hi = first + 8
        mismatches.append(
            {
                "record_id": record_id,
                "first_mismatch": first,
                "affect_token_count": len(affect_tokens),
                "film_token_count": len(film_tokens),
                "affect_context": affect_tokens[lo:hi],
                "film_context": film_tokens[lo:hi],
            }
        )
    return {
        "exact_match_count": len(exact),
        "mismatch_count": len(mismatches),
        "overlays_without_film_count": len(overlays_without_film),
        "mismatches": mismatches,
        "overlays_without_film": overlays_without_film,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the saved audit differs; do not rewrite it",
    )
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text() != rendered:
            raise SystemExit(f"stale audit: {OUT.relative_to(ROOT)}")
        return
    OUT.write_text(rendered)


if __name__ == "__main__":
    main()
