#!/usr/bin/env python3
import argparse, json, math, sys
from pathlib import Path

REQ_WRONG=["question_type","tested_ability","error_manifestation","error_cause","key_explanation","error_cause_evidence","evidence_crop_status"]
ALLOWED={"correct","wrong","pending_review"}
CROP_ALLOWED={"embedded","not_applicable","exception"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("json_path"); args=ap.parse_args()
    jp=Path(args.json_path).resolve(); d=json.loads(jp.read_text(encoding="utf-8"))
    errors=[]; qs=d.get("questions") or []; ids=set()
    for i,q in enumerate(qs):
        status=q.get("status")
        if status not in ALLOWED: errors.append(f"q[{i}] invalid status: {status}")
        key=(str(q.get("assignment_id","")),str(q.get("question_id","")))
        if not key[0] or not key[1]: errors.append(f"q[{i}] missing assignment_id/question_id")
        if key in ids: errors.append(f"duplicate question id: {key}")
        ids.add(key)
        if status=="wrong":
            for f in REQ_WRONG:
                if not str(q.get(f,"")).strip(): errors.append(f"{key} missing {f}")
            if q.get("error_cause_evidence") not in {"high","medium","low"}: errors.append(f"{key} invalid error_cause_evidence")
            cs=q.get("evidence_crop_status")
            if cs not in CROP_ALLOWED: errors.append(f"{key} invalid evidence_crop_status: {cs}")
            if cs=="embedded":
                paths=[]
                if q.get("evidence_image_path"): paths.append(q.get("evidence_image_path"))
                paths.extend(q.get("evidence_image_paths") or [])
                if not paths: errors.append(f"{key} embedded crop missing evidence_image_path(s)")
                for p in paths:
                    if str(p).startswith("data:image/"): continue
                    pp=Path(str(p)); pp=pp if pp.is_absolute() else (jp.parent/pp)
                    if not pp.exists(): errors.append(f"{key} evidence image not found: {pp}")
                if not str(q.get("evidence_dom_id","")).strip(): errors.append(f"{key} embedded crop missing evidence_dom_id")
            if cs=="exception" and not str(q.get("evidence_exception","")).strip():
                errors.append(f"{key} crop exception missing evidence_exception")
    c=sum(q.get("status")=="correct" for q in qs); w=sum(q.get("status")=="wrong" for q in qs); p=sum(q.get("status")=="pending_review" for q in qs)
    s=d.get("summary") or {}; expected={"total_questions":len(qs),"correct_questions":c,"wrong_questions":w,"pending_review":p}
    for k,v in expected.items():
        if s.get(k)!=v: errors.append(f"summary {k}={s.get(k)} expected {v}")
    denom=c+w; acc=round(c/denom*100,1) if denom else 0.0
    try: got=float(s.get("accuracy",-1))
    except Exception: got=-1
    if not math.isclose(got,acc,abs_tol=.05): errors.append(f"summary accuracy={s.get('accuracy')} expected {acc}")
    if errors:
        print("FAIL")
        for e in errors: print("-",e)
        sys.exit(1)
    print("PASS")

if __name__=="__main__": main()
