#!/usr/bin/env python3
import argparse, base64, html, json, mimetypes, re
from pathlib import Path

def esc(v): return '' if v is None else html.escape(str(v))
def tag(text,kind='gray'): return f'<span class="tag {esc(kind)}">{esc(text)}</span>'
def data_uri(path_value,base_dir):
    if not path_value: return ''
    s=str(path_value); p=Path(s)
    if s.startswith('data:image/'): return s
    if not p.is_absolute(): p=(base_dir/p).resolve()
    if not p.exists(): raise FileNotFoundError(p)
    mime=mimetypes.guess_type(p.name)[0] or 'image/png'
    return f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode('ascii')

def rows_or_note(rows,cols,note): return ''.join(rows) if rows else f'<tr><td colspan="{cols}">{esc(note)}</td></tr>'

def deadline_label(x):
    due=x.get('due_date')
    if due:
        m=re.fullmatch(r'(20\d{2})-(\d{2})-(\d{2})',str(due))
        txt=f'{int(m.group(2))}/{int(m.group(3))}' if m else str(due)
    else:
        txt='未明确'
    state=x.get('deadline_state')
    if state=='overdue': return txt+'｜已逾期'
    if x.get('carryover_to_next_week'): return txt+'｜需延续'
    if state=='completed': return txt+'｜已完成'
    return txt
def status_kind(text):
    t=str(text or '')
    if any(k in t for k in ('改善','完成','稳定','提升')): return 'green'
    if any(k in t for k in ('突出','风险','未完成')): return 'red'
    return 'amber'

def evidence_card(x,base):
    src=data_uri(x.get('image_path'),base) if x.get('image_path') else ''
    img=f'<img alt="{esc(x.get("title") or "错题证据")}" src="{src}">' if src else '<div class="note">未提供可展示证据图。</div>'
    return f'<div class="evidence"><h3>{esc(x.get("title") or "错题")}</h3>{img}<div class="small">{esc(x.get("source") or "")}</div></div>'

def wrong_section(d,base,idx,analytical=False):
    wr=d.get('wrong_records') or []
    qs=[x for x in wr if x.get('kind')=='question']; ds=[x for x in wr if x.get('kind')=='dictation']
    def rec_table(items,is_dict=False):
        rows=[]
        for x in items:
            if analytical and not is_dict:
                detail='；'.join([y for y in [x.get('question_type'),x.get('tested_ability'),x.get('error_cause')] if y])
            elif analytical and is_dict:
                detail='；'.join([y for y in [x.get('tested_ability'),x.get('error_cause')] if y])
            else: detail=x.get('source') or ''
            state='已订正' if x.get('corrected') else '未记录订正'
            rows.append(f'<tr><td>{esc(x.get("date"))}</td><td class="subject">{esc(x.get("subject"))}</td><td>{esc(x.get("title"))}</td><td>{esc(detail)}</td><td>{esc(state)}</td></tr>')
        return '<table class="record-table"><thead><tr><th>日期</th><th>科目</th><th>错题</th><th>'+('结构化记录' if analytical else '来源')+'</th><th>订正</th></tr></thead><tbody>'+rows_or_note(rows,5,'本周无记录。')+'</tbody></table>'
    qtab='l3wq' if analytical else 'l2wq'; dtab='l3wd' if analytical else 'l2wd'
    evid=''.join(evidence_card(x,base) for x in (d.get('evidence') or []))
    evid_block=f'<h3 style="margin:18px 0 10px;font-size:16px">代表性原始证据</h3><div class="grid2">{evid}</div>' if evid else ''
    return (f'<section id="wrong"><h2>{idx:02d}｜本周错题与听写汇总</h2><p class="desc">完整记录来自本周日报；证据图直接复用日报已裁好的原始图片，不重新裁剪。</p>'
            f'<div class="tabs"><div class="tab-bar"><button class="tab-btn active" data-tab="{qtab}">题目错题 {tag(str(len(qs))+"题","red")}</button><button class="tab-btn" data-tab="{dtab}">听写错误 {tag(str(len(ds))+"项","amber")}</button></div>'
            f'<div class="tab-panel active" id="{qtab}">{rec_table(qs,False)}</div><div class="tab-panel" id="{dtab}">{rec_table(ds,True)}</div></div>{evid_block}</section>')

def render_habits(habits,idx):
    cards=[]
    for h in habits:
        text=esc(h.get('observed') or h.get('text') or '')
        if h.get('next_focus'): text += f'<span class="small">下周关注：{esc(h.get("next_focus"))}</span>'
        cards.append(f'<div class="habit"><b>{esc(h.get("label"))}</b><span>{text}</span></div>')
    return f'<section id="habit"><h2>{idx:02d}｜本周学习过程与习惯观察</h2><p class="desc">基于本周日报中的可观察行为进行汇总，不使用“认真/努力”等泛化评价。</p><div class="habit-grid">{"".join(cards) or "<div class=\"note\">本周暂无可汇总的习惯记录。</div>"}</div></section>'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('json_path'); ap.add_argument('output_html'); ap.add_argument('--template',default=str(Path(__file__).resolve().parents[1]/'assets'/'template-reference.html')); a=ap.parse_args()
    jp=Path(a.json_path).resolve(); d=json.loads(jp.read_text(encoding='utf-8')); base=jp.parent; rt=d.get('report_type')
    if rt not in {'l2','l3'}: raise SystemExit('report_type must be l2 or l3')
    template=Path(a.template).read_text(encoding='utf-8'); route=d.get('route') or {}; ov=d.get('overview') or {}
    title='L3 学业管理周看板' if rt=='l3' else 'L2 学习执行周看板'
    subtitle='｜'.join([x for x in [d.get('student_name'),d.get('grade'),d.get('period_display')] if x])
    pills=[f"到校 {ov.get('attendance_days',0)}天",f"累计有效学习 {ov.get('effective_display','')}",f"题目错题 {ov.get('wrong_questions',0)}题",f"听写错误 {ov.get('dictation_errors',0)}项"]
    if ov.get('closure_text'): pills.append(str(ov.get('closure_text')))
    if rt=='l3':
        tut=d.get('tutoring') or {}; pills.append(f"专项辅导 Math {((tut.get('math') or {}).get('delivered',0))}/2｜English {((tut.get('english') or {}).get('delivered',0))}/2")
    header=(f'<header><div class="wrap"><h1>{title}</h1><div class="sub">{esc(subtitle)}</div><div class="route-strip"><b>当前升学路线</b><span class="route-badge">{esc(route.get("label") or "未提供")}</span><span class="route-note">{esc(route.get("note") or "")}</span></div><div class="meta">'+''.join(f'<span class="pill">{esc(x)}</span>' for x in pills)+'</div></div></header>')
    nav_l2=[('overview','本周概览'),('daily','每日执行'),('subject','分科核对'),('ongoing','持续任务'),('wrong','错题汇总'),('habit','习惯观察')]
    nav_l3=[('overview','本周概览'),('daily','每日执行'),('subject','分科核对'),('ongoing','持续任务'),('sessions','专项辅导'),('wrong','错题汇总'),('analysis','错题分析'),('habit','习惯观察')]
    nav='<nav><div class="wrap">'+''.join(f'<a href="#{i}">{t}</a>' for i,t in (nav_l3 if rt=='l3' else nav_l2))+'</div></nav>'
    stats=[('到校天数',ov.get('attendance_days',0),'本周'),('有效学习时长',ov.get('effective_display',''),'累计'),('题目错题',ov.get('wrong_questions',0),'来自日报'),('听写错误',ov.get('dictation_errors',0),'来自日报')]
    main='<section id="overview"><h2>01｜本周学习执行概览</h2><div class="stats">'+''.join(f'<div class="stat"><div class="l">{esc(k)}</div><div class="v">{esc(v)}</div><div class="s">{esc(s)}</div></div>' for k,v,s in stats)+'</div></section>'
    rows=[f'<tr><td><b>{esc(x.get("date"))}</b></td><td>{esc(x.get("main_tasks"))}</td><td>{esc(x.get("ongoing"))}</td><td>{esc(x.get("effective"))}</td></tr>' for x in d.get('daily_breakdown') or []]
    main+='<section id="daily"><h2>02｜每日任务执行回顾</h2><p class="desc">长周期Project、阅读等任务保留每天推进与顺延信息。</p><table><thead><tr><th>日期</th><th>当天主要任务</th><th>持续推进 / 顺延事项</th><th>有效学习</th></tr></thead><tbody>'+rows_or_note(rows,4,'本周暂无日报记录。')+'</tbody></table></section>'
    rows=[]
    for x in d.get('subjects') or []:
        acc='—' if x.get('accuracy') is None else f"{float(x.get('accuracy')):.1f}%"
        rows.append(f'<tr><td class="subject">{esc(x.get("subject"))}</td><td>{esc(x.get("checked"))}</td><td>{esc(x.get("correct"))}</td><td>{esc(x.get("wrong"))}</td><td><b>{esc(acc)}</b></td><td>{esc(x.get("correction_text"))}</td></tr>')
    main+='<section id="subject"><h2>03｜本周分科客观核对数据</h2><p class="desc">只统计有明确标准答案和分母的客观核对任务；开放任务不强行计入正确率。</p><table><thead><tr><th>科目</th><th>可核对题数</th><th>初次正确</th><th>错题</th><th>本周正确率</th><th>订正</th></tr></thead><tbody>'+rows_or_note(rows,6,'本周暂无可客观核对数据。')+'</tbody></table></section>'
    orows=[]
    for x in d.get('ongoing_tasks') or []:
        st='已完成' if str(x.get('status'))=='done' else ('需延续到下周' if x.get('carryover_to_next_week') else str(x.get('status') or '进行中'))
        orows.append(f'<tr><td class="subject">{esc(x.get("subject"))}</td><td>{esc(x.get("task"))}</td><td>{esc(deadline_label(x))}</td><td>{esc(x.get("progress"))}</td><td>{esc(st)}</td><td>{esc(x.get("next_step") or ("下周继续推进" if x.get("carryover_to_next_week") else "按计划推进"))}</td></tr>')
    main+='<section id="ongoing"><h2>04｜持续任务与截止日期</h2><p class="desc">同步日报中的任务DDL；周末仍未完成的任务明确标记是否延续到下周，已逾期任务单独提示。</p><table><thead><tr><th>科目</th><th>任务</th><th>截止日期</th><th>本周进度</th><th>周末状态</th><th>后续</th></tr></thead><tbody>'+rows_or_note(orows,6,'本周无持续任务或跨周待办。')+'</tbody></table></section>'
    if rt=='l2':
        main+=wrong_section(d,base,5,False)+render_habits(d.get('habits') or [],6)
    else:
        tut=d.get('tutoring') or {}; cards=[]
        for key,label in [('math','Math'),('english','English')]:
            x=tut.get(key) or {}; kind='green' if x.get('delivered')==x.get('required') else 'red'
            cards.append(f'<div class="session-card"><h3>{label}</h3><div class="session-kpis"><div class="session-kpi"><div class="n">{esc(x.get("required",2))}</div><div class="t">本周应上</div></div><div class="session-kpi"><div class="n">{esc(x.get("delivered",0))}</div><div class="t">本周已上</div></div><div class="session-kpi"><div class="n">{tag(x.get("status") or "未完成",kind)}</div><div class="t">交付状态</div></div></div><div class="feedback"><b>本周重点：</b>{esc(x.get("focus") or "暂无总结")}</div></div>')
        srows=[f'<tr><td>{esc(x.get("date"))}</td><td class="subject">{esc(x.get("subject"))}</td><td>{esc(x.get("minutes"))}min</td><td>{esc(x.get("content"))}</td><td>{esc(x.get("feedback"))}</td></tr>' for x in tut.get('sessions') or []]
        main+='<section id="sessions"><h2>05｜本周数学 / 英语专项辅导</h2><p class="desc">每周Math 2次 + English 2次，每次30分钟；按当周实际完成情况展示。</p><div class="session-grid">'+''.join(cards)+'</div><h3 style="margin:18px 0 10px;font-size:16px">本周课次记录</h3><table><thead><tr><th>日期</th><th>科目</th><th>时长</th><th>主要内容</th><th>教师反馈</th></tr></thead><tbody>'+rows_or_note(srows,5,'本周暂无专项辅导记录。')+'</tbody></table></section>'
        main+=wrong_section(d,base,6,True)
        sigrows=[]
        for x in d.get('recurring_signals') or []:
            sigrows.append(f'<tr><td class="subject">{esc(x.get("subject"))}</td><td><b>{esc(x.get("issue"))}</b></td><td>{esc(x.get("occurrence"))}次</td><td>{esc(x.get("manifestation"))}</td><td>{esc(x.get("observation"))}</td></tr>')
        foc=''.join(f'<div class="focus-item"><b>下周重点 {i+1}</b>{esc(x)}</div>' for i,x in enumerate(d.get('next_week_focus') or []))
        main+='<section id="analysis"><h2>07｜本周错题初步分析</h2><p class="desc">只把本周重复出现的信号纳入分析；单次错误不升级为稳定能力问题。</p><table><thead><tr><th>科目</th><th>重复问题</th><th>出现</th><th>主要表现</th><th>本周观察</th></tr></thead><tbody>'+rows_or_note(sigrows,5,'本周暂无达到重复阈值的问题。')+'</tbody></table><h3 style="margin:18px 0 10px;font-size:16px">下周关注重点</h3><div class="focus-list">'+(foc or '<div class="note">暂无新增重点。</div>')+'</div></section>'+render_habits(d.get('habits') or [],8)
    main+=f'<div class="footer">{esc(d.get("footer") or "机构学习管理周看板")}</div>'
    out=template.replace('__HEADER__',header).replace('__NAV__',nav).replace('__MAIN__',main)
    Path(a.output_html).write_text(out,encoding='utf-8')
if __name__=='__main__': main()
