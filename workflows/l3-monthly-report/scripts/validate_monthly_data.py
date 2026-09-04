#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
REQ=['report_type','student_name','grade','month_display','route','overview','subjects','comparison','trend_rows','tutoring','ability_map','deep_analysis','interventions','mock','habits','route_modules','next_month_focus','parent_communication_focus']
FORBIDDEN=('结转','余额','累计剩余','上周结转','课次余额')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('json_path'); a=ap.parse_args(); p=Path(a.json_path).resolve(); d=json.loads(p.read_text(encoding='utf-8')); e=[]
    for f in REQ:
        if f not in d:e.append(f'missing {f}')
    if d.get('report_type')!='l3_monthly':e.append('report_type must be l3_monthly')
    for i,s in enumerate(d.get('subjects') or []):
        try:
            checked=int(s.get('checked',0)); correct=int(s.get('correct',0)); wrong=int(s.get('wrong',0))
            if checked!=correct+wrong:e.append(f'subjects[{i}] checked != correct + wrong')
            if checked and s.get('accuracy') is not None and abs(float(s['accuracy'])-correct*100/checked)>.11:e.append(f'subjects[{i}] accuracy mismatch')
        except Exception:e.append(f'subjects[{i}] invalid numeric data')
    tut=d.get('tutoring') or {}; weeks=int(tut.get('service_weeks') or 0)
    for key in ('math','english'):
        x=tut.get(key) or {}
        if int(x.get('required',-1))!=weeks*2:e.append(f'tutoring.{key}.required must equal service_weeks*2')
        if int(x.get('delivered',0))<0:e.append(f'tutoring.{key}.delivered invalid')
    for i,x in enumerate(d.get('ability_map') or []):
        try:
            if int(x.get('occurrence',0))<2:e.append(f'ability_map[{i}].occurrence must be >= 2')
        except Exception:e.append(f'ability_map[{i}].occurrence invalid')
    mock=d.get('mock') or {}
    if mock.get('status') not in {'completed','not_completed','not_provided'}:e.append('mock.status must be completed/not_completed/not_provided')
    if mock.get('status')=='completed' and not mock.get('tests'):e.append('mock completed but tests empty')
    if not d.get('habits'):e.append('habits must contain monthly synthesized changes')
    if not d.get('route_modules'):e.append('route_modules must reflect the current route')
    if not d.get('next_month_focus'):e.append('next_month_focus is required')
    if not str(d.get('parent_communication_focus') or '').strip():e.append('parent_communication_focus is required')
    comp=d.get('comparison') or {}
    if not comp.get('first_month') and not d.get('trend_rows'):e.append('trend_rows required when first_month=false')
    blob=json.dumps(d,ensure_ascii=False)
    for w in FORBIDDEN:
        if w in blob:e.append(f'forbidden carryover/balance wording found: {w}')
    if e:
        print('FAIL');[print('-',x) for x in e];sys.exit(1)
    print('PASS')
if __name__=='__main__':main()
