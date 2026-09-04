#!/usr/bin/env python3
import argparse, json, re, sys
from collections import defaultdict
from datetime import date
from pathlib import Path


def parse_minutes(s):
    if s is None: return 0
    s=str(s).strip().lower().replace('小时','h').replace('分钟','m').replace('min','m')
    h=re.search(r'(\d+)\s*h',s); m=re.search(r'(\d+)\s*m',s)
    if h or m: return (int(h.group(1)) if h else 0)*60 + (int(m.group(1)) if m else 0)
    if s.isdigit(): return int(s)
    return 0


def fmt_minutes(n):
    n=int(n or 0); return f'{n//60}h{n%60:02d}m' if n>=60 else f'{n}m'


def parse_date_text(s):
    s=str(s or '')
    m=re.search(r'(20\d{2})[年\-/](\d{1,2})[月\-/](\d{1,2})',s)
    if not m: return None
    try: return date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
    except ValueError: return None


def parse_score(text):
    if not text: return None
    m=re.search(r'(\d+)\s*/\s*(\d+)',str(text))
    if not m: return None
    c,t=int(m.group(1)),int(m.group(2))
    if t<=0 or c<0 or c>t: return None
    return c,t


def subj_from_item(x):
    if x.get('subject'): return str(x['subject']).strip()
    t=str(x.get('title') or x.get('source') or '')
    return re.split(r'[｜|:：]',t,maxsplit=1)[0].strip() or '其他'


def abs_image(raw, daily_json):
    if not raw: return ''
    p=Path(str(raw))
    if not p.is_absolute(): p=(daily_json.parent/p).resolve()
    return str(p)


def deadline_state(due, status, week_end):
    if status == 'done': return 'completed'
    if not due: return 'unknown'
    try: dd=date.fromisoformat(str(due))
    except Exception: return 'unknown'
    if dd < week_end: return 'overdue'
    if dd == week_end: return 'due_this_week'
    delta=(dd-week_end).days
    if delta <= 7: return 'due_next_week'
    return 'due_later'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_json')
    ap.add_argument('daily_json', nargs='+')
    ap.add_argument('--report-type', choices=['l2','l3'], required=True)
    a=ap.parse_args()
    docs=[]
    for f in a.daily_json:
        p=Path(f).resolve(); d=json.loads(p.read_text(encoding='utf-8')); docs.append((p,d))
    if not docs: raise SystemExit('no daily json files')

    # chronological order where possible
    docs.sort(key=lambda x: parse_date_text(x[1].get('date_display')) or date.min)
    students={str(d.get('student_name','')).strip() for _,d in docs}
    grades={str(d.get('grade','')).strip() for _,d in docs}
    if len(students-{''})>1: raise SystemExit(f'mixed students: {students}')
    if len(grades-{''})>1: raise SystemExit(f'mixed grades: {grades}')
    expected='l3' if a.report_type=='l3' else 'l2'
    bad=[d.get('report_type') for _,d in docs if d.get('report_type')!=expected]
    if bad: raise SystemExit(f'daily report_type mismatch, expected {expected}: {bad}')

    total_min=sum(parse_minutes((d.get('timing') or {}).get('effective')) for _,d in docs)
    all_wrong=[]; all_dict=[]; daily_break=[]; subject_stats=defaultdict(lambda:[0,0]); task_latest={}; habit_raw=[]; tutoring_sessions=[]
    corrected_wrong=0; corrected_dict=0

    for p,d in docs:
        dt=parse_date_text(d.get('date_display')); dshort=f'{dt.month}/{dt.day}' if dt else str(d.get('date_display') or '')
        tasks=d.get('tasks') or []
        main=[]; ongoing=[]
        for t in tasks:
            subject=str(t.get('subject') or '其他'); task=str(t.get('task') or '').strip()
            if task: main.append(f'{subject} {task}'.strip())
            due=t.get('due_date')
            key=(subject,task)
            note=str(t.get('note') or '').strip()
            task_latest[key]={
                'subject':subject,'task':task,'due_date':due,'progress':note,
                'status':str(t.get('status') or 'todo'),'long_cycle':bool(t.get('long_cycle')),'next_step':''
            }
            if t.get('long_cycle') or str(t.get('status') or 'done')!='done':
                ddl=f'（DDL {due[5:].replace("-","/")}）' if isinstance(due,str) and re.fullmatch(r'20\d{2}-\d{2}-\d{2}',due) else ('（DDL 未明确）' if not due else f'（DDL {due}）')
                ongoing.append(f'{subject} {task}：{note}{ddl}'.strip('：'))
            if t.get('result_kind')=='scored':
                sc=parse_score(t.get('result_text'))
                if sc:
                    c,total=sc; subject_stats[subject][0]+=total; subject_stats[subject][1]+=c
        daily_break.append({'date':dshort,'main_tasks':'；'.join(main) or '暂无记录','ongoing':'；'.join(ongoing) or '无','effective':(d.get('timing') or {}).get('effective') or ''})

        for kind,key,target in [('question','wrong_questions',all_wrong),('dictation','dictation_errors',all_dict)]:
            for q in d.get(key) or []:
                rec=dict(q); rec['kind']=kind; rec['date']=dshort; rec['subject']=subj_from_item(q); rec['image_path']=abs_image(q.get('image_path'),p)
                target.append(rec)
                if q.get('corrected'):
                    if kind=='question': corrected_wrong+=1
                    else: corrected_dict+=1
        for h in d.get('habits') or []:
            habit_raw.append({'date':dshort,'label':h.get('label'),'text':h.get('text')})
        if a.report_type=='l3':
            for s in d.get('tutoring') or []:
                if not s.get('completed'): continue
                title=str(s.get('title') or '')
                subj='Math' if title.lower().startswith('math') else ('English' if title.lower().startswith('english') else title.split('｜')[0].strip())
                tutoring_sessions.append({'date':dshort,'subject':subj,'minutes':30,'content':s.get('content') or title,'feedback':s.get('feedback') or ''})

    subjects=[]
    wrong_by_subject=defaultdict(int)
    correction_by_subject=defaultdict(int)
    for q in all_wrong:
        wrong_by_subject[q['subject']]+=1
        if q.get('corrected'): correction_by_subject[q['subject']]+=1
    for subject,(checked,correct) in subject_stats.items():
        wrong=max(0,checked-correct); acc=round(correct*100/checked,1) if checked else None
        subjects.append({'subject':subject,'checked':checked,'correct':correct,'wrong':wrong,'accuracy':acc,'correction_text':f"{correction_by_subject.get(subject,0)}/{wrong_by_subject.get(subject,wrong)} 已订正" if wrong_by_subject.get(subject,wrong) else '无错题'})
    subjects.sort(key=lambda x:x['subject'])

    # Choose a small representative evidence set. AI may replace selection, but no raw rescanning.
    combined=all_wrong+all_dict
    evidence=[]
    for q in combined:
        if q.get('image_path') and len(evidence)<4:
            evidence.append({'kind':q.get('kind'),'title':q.get('title') or f"{q.get('subject')}错题",'source':f"{q.get('date')}｜{q.get('source') or ''}".strip('｜'),'image_path':q.get('image_path')})

    route=dict(docs[-1][1].get('route') or {})
    dates=[parse_date_text(d.get('date_display')) for _,d in docs]; dates=[x for x in dates if x]
    if dates:
        lo,hi=min(dates),max(dates); period=f'{lo.year}年{lo.month}月{lo.day}日–{hi.month}月{hi.day}日'
    else: period='本周'
    week_end=max(dates) if dates else date.today()
    ongoing_tasks=[]
    for x in task_latest.values():
        unresolved=str(x.get('status') or 'todo')!='done'
        if x.get('long_cycle') or unresolved:
            y=dict(x)
            y['deadline_state']=deadline_state(y.get('due_date'),str(y.get('status') or 'todo'),week_end)
            y['carryover_to_next_week']=bool(unresolved)
            ongoing_tasks.append(y)
    ongoing_tasks.sort(key=lambda x:(x.get('due_date') is None, str(x.get('due_date') or '9999-99-99'), x.get('subject') or '', x.get('task') or ''))

    closure_parts=[]
    if all_wrong: closure_parts.append(f'题目错题{corrected_wrong}/{len(all_wrong)}已订正')
    if all_dict: closure_parts.append(f'听写错误{corrected_dict}/{len(all_dict)}已订正')
    out={
      'report_version':'1.7','report_type':a.report_type,
      'student_name':next(iter(students-{''}),''),'grade':next(iter(grades-{''}),''),'period_display':period,'route':route,
      'overview':{'attendance_days':len(docs),'effective_minutes':total_min,'effective_display':fmt_minutes(total_min),'wrong_questions':len(all_wrong),'dictation_errors':len(all_dict),'closure_text':'；'.join(closure_parts) or '本周无错题记录'},
      'daily_breakdown':daily_break,'subjects':subjects,'ongoing_tasks':ongoing_tasks,
      'wrong_records':all_wrong+all_dict,'evidence':evidence,'habits':[],
      '_analysis_inputs':{'habit_observations':habit_raw}
    }
    if a.report_type=='l3':
        counts=defaultdict(int)
        for s in tutoring_sessions: counts[s['subject']]+=1
        out['tutoring']={
          'math':{'required':2,'delivered':counts.get('Math',0),'status':'已完成' if counts.get('Math',0)==2 else '未完成','focus':''},
          'english':{'required':2,'delivered':counts.get('English',0),'status':'已完成' if counts.get('English',0)==2 else '未完成','focus':''},
          'sessions':tutoring_sessions
        }
        out['recurring_signals']=[]; out['next_week_focus']=[]
        out['_analysis_inputs']['wrong_records']=all_wrong+all_dict
    Path(a.output_json).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(a.output_json)

if __name__=='__main__': main()
