#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("html_path"); args=ap.parse_args()
    txt=Path(args.html_path).read_text(encoding="utf-8")
    required=["逐题批改结果","错题详细分析","总题目数","正确题数","错误题数","正确率",'id="grading-data"']
    missing=[x for x in required if x not in txt]
    placeholders=re.findall(r"__[A-Z_]+__",txt)
    errors=[]
    if missing: errors.append(f"missing: {missing}")
    if placeholders: errors.append(f"unresolved placeholders: {placeholders}")
    m=re.search(r'<script type="application/json" id="grading-data">(.*?)</script>',txt,re.S)
    if not m:
        errors.append("grading-data payload missing")
    else:
        try:
            data=json.loads(m.group(1).replace("<\\/","</"))
            wrongs=[q for q in data.get("questions",[]) if q.get("status")=="wrong"]
            cards=len(re.findall(r'class="error-card"',txt))
            if cards!=len(wrongs): errors.append(f"error-card count={cards} expected={len(wrongs)}")
            for q in wrongs:
                if q.get("evidence_crop_status")=="embedded":
                    dom=q.get("evidence_dom_id")
                    if not dom or f'id="{dom}"' not in txt: errors.append(f"embedded crop missing in HTML for {q.get('assignment_id')}-{q.get('question_id')}")
                    elif 'data-evidence-role="wrong-question-crop"' not in txt: errors.append("wrong-question crop role missing")
        except Exception as e:
            errors.append(f"invalid grading-data payload: {e}")
    if errors:
        print("FAIL")
        for e in errors: print("-",e)
        sys.exit(1)
    print("PASS")

if __name__=="__main__": main()
