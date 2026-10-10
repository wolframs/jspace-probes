"""CPU-only website coverage inventory. Count saved evidence, not directories.

Standard records and sampled affect runs have different schemas and remain
separate counts. Only canonical affectXX JSON files with a `runs` array enter
the batch census. Reports, reanalyses, overlays, calibration arrays, judges,
and prefix scans do not add runs. Repeated seeds are runs, not independent
experiments. site.py regenerates this inventory and its reader-facing page.
"""

import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent


def inventory(index):
    results = ROOT / "results"
    batches = []
    for folder in sorted(results.glob("affect*")):
        if not folder.is_dir():
            continue
        sources = []
        model = None
        for path in sorted(folder.glob("affect*.json")):
            if not re.fullmatch(r"affect\d+(?:-(?:part\d+|[A-Z]))?\.json", path.name):
                continue
            data = json.loads(path.read_text())
            if not isinstance(data, dict) or not isinstance(data.get("runs"), list):
                continue
            if not all(isinstance(row, dict) for row in data["runs"]):
                raise ValueError(f"Invalid run array: {path}")
            model = data["model"]
            sources.append({"path": str(path.relative_to(ROOT)), "runs": len(data["runs"])})
        # Include the geometry analysis and instrument checks for navigation,
        # but never count their derived rows as newly generated runs.
        if sources or (folder / "plain.md").exists():
            batches.append({
                "id": folder.name, "model": model,
                "runs": sum(s["runs"] for s in sources), "sources": sources,
                "documents": [str((folder / name).relative_to(ROOT))
                              for name in ("plain.md", "report.md", "thoughts.md")
                              if (folder / name).exists()],
            })
    units = {str(e["unit"]) for e in index}
    return {
        "record_pages": len(index),
        "films": sum(bool(e.get("film")) for e in index),
        "plain_summaries": sum((results / e["id"] / "plain.md").exists() for e in index),
        "units": sum(u.isdigit() for u in units),
        "other_groups": sorted(u for u in units if not u.isdigit()),
        "models": dict(sorted(Counter(e["model"] for e in index).items())),
        "latest_record": max((e["created"][:10] for e in index), default=None),
        "affect_runs": sum(b["runs"] for b in batches),
        "batches": batches,
        "counting_rule": "Record pages and saved affect runs are separate. Affect runs count only canonical affectXX JSON runs arrays. Calibration arrays, reused analyses, overlays, prefix scans and judge calls are excluded. Seeds and conditions are not independent experiments.",
    }
