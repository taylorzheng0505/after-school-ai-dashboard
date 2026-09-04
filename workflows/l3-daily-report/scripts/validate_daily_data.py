#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

REQ_COMMON = ["report_type", "student_name", "grade", "date_display", "route", "timing", "tasks", "wrong_questions", "dictation_errors", "habits", "note"]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("json_path"); a = ap.parse_args()
    p = Path(a.json_path).resolve(); d = json.loads(p.read_text(encoding="utf-8")); errors = []
    for f in REQ_COMMON:
        if f not in d: errors.append(f"missing {f}")
    rt = d.get("report_type")
    if rt not in {"l2", "l3"}: errors.append("report_type must be l2 or l3")
    if rt == "l3" and "tutoring" not in d: errors.append("L3 missing tutoring")
    for i, t in enumerate(d.get("tasks") or []):
        if "due_date" not in t:
            errors.append(f"tasks[{i}] missing due_date key")
        due = t.get("due_date")
        if due not in (None, ""):
            import re
            if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", str(due)):
                errors.append(f"tasks[{i}] due_date must be YYYY-MM-DD or null")
    for group in ("wrong_questions", "dictation_errors"):
        for i, q in enumerate(d.get(group) or []):
            if not q.get("title"): errors.append(f"{group}[{i}] missing title")
            ip = q.get("image_path")
            if ip:
                pp = Path(str(ip)); pp = pp if pp.is_absolute() else (p.parent / pp)
                if not pp.exists(): errors.append(f"{group}[{i}] image not found: {pp}")
            if rt == "l3":
                for f in ("question_type", "tested_ability", "error_manifestation", "error_cause"):
                    if not str(q.get(f, "")).strip(): errors.append(f"{group}[{i}] missing {f}")
    if errors:
        print("FAIL")
        for e in errors: print("-", e)
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
