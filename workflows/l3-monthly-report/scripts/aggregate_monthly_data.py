#!/usr/bin/env python3
import argparse, json, re
from collections import defaultdict
from datetime import date
from pathlib import Path

def parse_minutes(s):
    if s is None:return 0
    s=str(s).strip().lower().replace('小时','h').replace('分钟','m').replace('min','m')
    h=re.search(r'(\d+)\s*h',s); m=re.search(r'(\d+)\s*m',s)
    if h or m:return (int(h.group(1)) if h else 0)*60+(int(m.group(1)) if m else 0)
    return int(s) if s.isdigit() else 0

def fmt_minutes(n):
    n=int(n or 0); return f'{n//60}h{n%60:02d}m' if n>=60 else f'{n}m'

def parse_date_text(s):
    m=re.search(r'(20\d{2})[年\-/](\d{1,2})[月\-/](\d{1,2})',str(s or ''))
    if not m:return None
    try:return date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
    except ValueError:return None

def parse_score(text):
    m=re.search(r'(\d+)\s*/\s*(\d+)',str(text or ''))
    if not m:return None
    c,t=int(m.group(1)),int(m.group(2))
    return (c,t) if t>0 and 0<=c<=t else None

def subj(x):
    if x.get('subject'):return str(x['subject']).strip()
    return re.split(r'[｜|:：]',str(x.get('title') or x.get('source') or ''),maxsplit=1)[0].strip() or '其他'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_json'); ap.add_argument('daily_json',nargs='+'); ap.add_argument('--previous-data'); a=ap.parse_args()
    docs=[]
    for f in a.daily_json:
        p=Path(f).resolve(); d=json.loads(p.read_text(encoding='utf-8'))
        if d.get('report_type')!='l3': raise SystemExit(f'not L3 daily data: {p}')
        docs.append((p,d))
    docs.sort(key=lambda x:parse_date_text(x[1].get('date_display')) or date.min)
    students={str(d.get('student_name','')).strip() for _,d in docs}; grades={str(d.get('grade','')).strip() for _,d in docs}
    if len(students-{''})>1:raise SystemExit(f'mixed students: {students}')
    if len(grades-{''})>1:raise SystemExit(f'mixed grades: {grades}')
    dates=[parse_date_text(d.get('date_display')) for _,d in docs]; dates=[x for x in dates if x]
    if dates:
        y,m=dates[0].year,dates[0].month
        if any(x.year!=y or x.month!=m for x in dates): raise SystemExit('daily files span multiple months')
        month_display=f'{y}年{m}月'
        weeks=len({x.isocalendar()[:2] for x in dates})
    else: month_display='本月'; weeks=0
    total_min=sum(parse_minutes((d.get('timing') or {}).get('effective')) for _,d in docs)
    subject_stats=defaultdict(lambda:[0,0]); wrong=[]; habit_raw=[]; sessions=[]
    for p,d in docs:
        dt=parse_date_text(d.get('date_display')); ds=f'{dt.month}/{dt.day}' if dt else str(d.get('date_display') or '')
        for t in d.get('tasks') or []:
            if t.get('result_kind')=='scored':
                sc=parse_score(t.get('result_text'))
                if sc:
                    c,total=sc; subject_stats[str(t.get('subject') or '其他')][0]+=total; subject_stats[str(t.get('subject') or '其他')][1]+=c
        for kind,key in [('question','wrong_questions'),('dictation','dictation_errors')]:
            for q in d.get(key) or []:
                rec=dict(q); rec['kind']=kind; rec['date']=ds; rec['subject']=subj(q); wrong.append(rec)
        for h in d.get('habits') or []: habit_raw.append({'date':ds,'label':h.get('label'),'text':h.get('text')})
        for s in d.get('tutoring') or []:
            if not s.get('completed'):continue
            title=str(s.get('title') or ''); subject='Math' if title.lower().startswith('math') else ('English' if title.lower().startswith('english') else title.split('｜')[0].strip())
            sessions.append({'date':ds,'subject':subject,'minutes':30,'content':s.get('content') or title,'feedback':s.get('feedback') or ''})
    subjects=[]
    for subject,(checked,correct) in subject_stats.items():
        subjects.append({'subject':subject,'checked':checked,'correct':correct,'wrong':checked-correct,'accuracy':round(correct*100/checked,1) if checked else None})
    subjects.sort(key=lambda x:x['subject'])
    q=sum(1 for x in wrong if x.get('kind')=='question'); de=sum(1 for x in wrong if x.get('kind')=='dictation')
    counts=defaultdict(int)
    for s in sessions:counts[s['subject']]+=1
    previous=None
    if a.previous_data:
        previous=json.loads(Path(a.previous_data).read_text(encoding='utf-8'))
    out={
      'report_version':'1.6','report_type':'l3_monthly','student_name':next(iter(students-{''}),''),'grade':next(iter(grades-{''}),''),'month_display':month_display,
      'route':dict(docs[-1][1].get('route') or {}),'overview':{'attendance_days':len(docs),'effective_minutes':total_min,'effective_display':fmt_minutes(total_min),'wrong_questions':q,'dictation_errors':de},
      'subjects':subjects,'comparison':{'first_month':previous is None,'previous_month_label':''},'trend_rows':[],
      'tutoring':{'service_weeks':weeks,'math':{'required':weeks*2,'delivered':counts.get('Math',0),'status':'全部完成' if counts.get('Math',0)==weeks*2 and weeks else '未完成','focus':''},'english':{'required':weeks*2,'delivered':counts.get('English',0),'status':'全部完成' if counts.get('English',0)==weeks*2 and weeks else '未完成','focus':''}},
      'ability_map':[],'deep_analysis':[],'interventions':[],
      'mock':{'status':'not_provided','note':'','tests':[]},'habits':[],'route_summary':'','route_modules':[],'next_month_focus':[],'parent_communication_focus':'',
      '_analysis_inputs':{'wrong_records':wrong,'habit_observations':habit_raw,'tutoring_sessions':sessions,'previous_month_data':previous}
    }
    Path(a.output_json).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8'); print(a.output_json)
if __name__=='__main__':main()
