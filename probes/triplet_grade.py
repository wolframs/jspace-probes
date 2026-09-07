"""Archived audit02 Opus rubric on available SoC generations; resumable."""
import datetime
import hashlib
import json

import audit02
import lab
from triplet import ARMS, ROOT, write_json


def grade():
    dest = ROOT / "opus-grades.json"
    out = json.loads(dest.read_text()) if dest.exists() else {"records": {}}
    pending = []
    candidates = [(arm, f"triplet-{arm.lower()}-soc-nf4") for arm in ARMS]
    candidates.append(("C", "triplet-c-soc-nf4-native"))
    for arm, rid in candidates:
        p = lab.RESULTS / rid / "record.json"
        if not p.exists():
            continue
        text = json.loads(p.read_text())["generated"][0]
        sha = hashlib.sha256(text.encode()).hexdigest()
        row = out["records"].setdefault(rid, {"text_sha256": sha, "judgments": {}, "behavior_defined": arm != "A"})
        assert row["text_sha256"] == sha, "Generation changed under existing grades"
        if len(row["judgments"]) < len(audit02.JUDGMENTS):
            pending.append((rid, text, row))
    if not pending:
        print("No ungraded SoC records", flush=True)
        return
    key = audit02._openrouter_key()
    grader = out.setdefault("grader", audit02._pick_grader(key))
    out["rubric"] = audit02.JUDGMENTS
    out["method"] = "audit02._judge; temperature=0, max_tokens=8, reasoning disabled; first three judgments form experiential score"
    for rid, text, row in pending:
        for name, question in audit02.JUDGMENTS.items():
            if name not in row["judgments"]:
                row["judgments"][name] = audit02._judge(key, grader, text, question)
                row["updated"] = datetime.datetime.now().isoformat()
                write_json(dest, out)
                print("GRADE", rid, grader, name, row["judgments"][name], flush=True)
        row["experiential_score"] = sum(row["judgments"][k] for k in audit02.JUDGMENTS if k != "coherent") / 3
        write_json(dest, out)


if __name__ == "__main__":
    grade()
