#!/usr/bin/env python3
import argparse, json, math, sys
from pathlib import Path

REQ=['report_type','student_name','grade','period_display','route','overview','daily_breakdown','subjects','wrong_records','evidence','habits']
FORBIDDEN_WORDS=('结转','余额','累计剩余','上周结转','课次余额')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('json_path'); a=ap.parse_args()
    p=Path(a.json_path).resolve(); d=json.loads(p.read_text(encoding='utf-8')); e=[]
    for f in REQ:
        if f not in d: e.append(f'missing {f}')
    rt=d.get('report_type')
    if rt not in {'l2','l3'}: e.append('report_type must be l2 or l3')
    ov=d.get('overview') or {}
    wr=d.get('wrong_records') or []
    q=sum(1 for x in wr if x.get('kind')=='question'); de=sum(1 for x in wr if x.get('kind')=='dictation')
    if ov.get('wrong_questions')!=q: e.append(f'overview wrong_questions={ov.get("wrong_questions")} but records={q}')
    if ov.get('dictation_errors')!=de: e.append(f'overview dictation_errors={ov.get("dictation_errors")} but records={de}')
    for i,s in enumerate(d.get('subjects') or []):
        try:
            checked=int(s.get('checked',0)); correct=int(s.get('correct',0)); wrong=int(s.get('wrong',0))
            if checked!=correct+wrong: e.append(f'subjects[{i}] checked != correct + wrong')
            if checked:
                calc=correct*100/checked; got=float(s.get('accuracy'))
                if abs(calc-got)>0.11: e.append(f'subjects[{i}] accuracy mismatch: {got} vs {calc:.1f}')
        except Exception: e.append(f'subjects[{i}] invalid numeric fields')
    for i,x in enumerate(d.get('evidence') or []):
        ip=x.get('image_path')
        if ip:
            pp=Path(str(ip)); pp=pp if pp.is_absolute() else (p.parent/pp).resolve()
            if not pp.exists(): e.append(f'evidence[{i}] image not found: {pp}')
            if str(ip).startswith('data:image/'): e.append(f'evidence[{i}] image_path must not be base64')
    for i,x in enumerate(d.get('ongoing_tasks') or []):
        if 'due_date' not in x: e.append(f'ongoing_tasks[{i}] missing due_date key')
        due=x.get('due_date')
        if due not in (None,''):
            import re
            if not re.fullmatch(r'20\d{2}-\d{2}-\d{2}',str(due)): e.append(f'ongoing_tasks[{i}] due_date must be YYYY-MM-DD or null')
        if 'carryover_to_next_week' not in x: e.append(f'ongoing_tasks[{i}] missing carryover_to_next_week')
        if x.get('deadline_state') not in {'completed','due_this_week','due_next_week','due_later','overdue','unknown'}:
            e.append(f'ongoing_tasks[{i}] invalid deadline_state')
    if not (d.get('habits') or []): e.append('habits must contain weekly synthesized observations')
    if rt=='l3':
        tut=d.get('tutoring') or {}
        for key in ('math','english'):
            x=tut.get(key) or {}
            if x.get('required')!=2: e.append(f'tutoring.{key}.required must be 2')
            if int(x.get('delivered',0))<0: e.append(f'tutoring.{key}.delivered invalid')
        for i,x in enumerate(d.get('recurring_signals') or []):
            try:
                if int(x.get('occurrence',0))<2: e.append(f'recurring_signals[{i}].occurrence must be >= 2')
            except Exception: e.append(f'recurring_signals[{i}].occurrence invalid')
        if not d.get('next_week_focus'): e.append('L3 next_week_focus is required')
    blob=json.dumps(d,ensure_ascii=False)
    for w in FORBIDDEN_WORDS:
        if w in blob: e.append(f'forbidden carryover/balance wording found: {w}')
    if e:
        print('FAIL'); [print('-',x) for x in e]; sys.exit(1)
    print('PASS')
if __name__=='__main__': main()
