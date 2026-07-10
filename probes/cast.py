"""Backfill open-vocab cast lists into existing film.json files.

New films get a cast at capture time (lab.film_cast); this walks the
archive and adds one to every film that predates the feature. No GPU.

Usage: python probes/cast.py
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lab import RESULTS, film_cast  # noqa: E402


def main() -> None:
    for path in sorted(RESULTS.glob("*/film.json")):
        film = json.loads(path.read_text())
        rec = json.loads((path.parent / "record.json").read_text())
        convo = " ".join(m["content"] for m in rec["conversation"])
        film["cast"] = film_cast(film, convo)
        path.write_text(json.dumps(film))
        vol = [c["w"] for c in film["cast"] if not c["echo"]][:8]
        print(f"{path.parent.name}: cast {len(film['cast'])}, "
              f"volunteered: {', '.join(vol)}", flush=True)


if __name__ == "__main__":
    main()
