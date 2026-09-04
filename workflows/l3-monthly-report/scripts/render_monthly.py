#!/usr/bin/env python3
import argparse,html,json
from pathlib import Path

def esc(v):return '' if v is None else html.escape(str(v))
def tag(text,kind='gray'):return f'<span class="tag {esc(kind)}">{esc(text)}</span>'
def rows_or_note(rows,cols,note):return ''.join(rows) if rows else f'<tr><td colspan="{cols}">{esc(note)}</td></tr>'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('json_path');ap.add_argument('output_html');ap.add_argument('--template',default=str(Path(__file__).resolve().parents[1]/'assets'/'template-reference.html'));a=ap.parse_args()
    d=json.loads(Path(a.json_path).read_text(encoding='utf-8'));template=Path(a.template).read_text(encoding='utf-8');route=d.get('route') or {};ov=d.get('overview') or {};tut=d.get('tutoring') or {};mock=d.get('mock') or {}
    subtitle='｜'.join([x for x in [d.get('student_name'),d.get('grade'),d.get('month_display')] if x])
    total_del=int((tut.get('math') or {}).get('delivered',0))+int((tut.get('english') or {}).get('delivered',0));total_req=int((tut.get('math') or {}).get('required',0))+int((tut.get('english') or {}).get('required',0))
    mock_text='月度模拟测试 '+('已完成' if mock.get('status')=='completed' else ('未完成' if mock.get('status')=='not_completed' else '未提供'))
    pills=[f"到校 {ov.get('attendance_days',0)}天",f"有效学习 {ov.get('effective_display','')}",f"专项辅导 {total_del}/{total_req}",mock_text]
    header=f'<header><div class="wrap"><h1>L3 学业管理月度报告</h1><div class="sub">{esc(subtitle)}</div><div class="route-strip"><b>当前升学路线</b><span class="route-badge">{esc(route.get("label") or "未提供")}</span><span class="route-note">{esc(route.get("note") or "")}</span></div><div class="meta">'+''.join(f'<span class="pill">{esc(x)}</span>' for x in pills)+'</div></div></header>'
    navitems=[('overview','月度概览'),('trend','环比趋势'),('sessions','专项辅导'),('wrong','错题分析'),('intervention','干预效果'),('mock','模拟测试'),('habit','学习习惯'),('route','路线管理'),('next','下月重点')]
    nav='<nav><div class="wrap">'+''.join(f'<a href="#{i}">{t}</a>' for i,t in navitems)+'</div></nav>'
    stats=[('到校',f"{ov.get('attendance_days',0)}天"),('有效学习',ov.get('effective_display','')),('题目错题',ov.get('wrong_questions',0)),('听写错误',f"{ov.get('dictation_errors',0)}项")]
    main='<section id="overview"><h2>01｜本月学习执行概览</h2><div class="stats">'+''.join(f'<div class="stat"><div class="l">{esc(k)}</div><div class="v">{esc(v)}</div></div>' for k,v in stats)+'</div></section>'
    # Trend
    tr=[]
    for x in d.get('trend_rows') or []:
        kind=x.get('trend_kind') or 'watch';cls='trend-good' if kind=='good' else ('trend-bad' if kind=='bad' else 'trend-watch')
        tr.append(f'<tr><td>{esc(x.get("metric"))}</td><td>{esc(x.get("previous"))}</td><td>{esc(x.get("current"))}</td><td>{esc(x.get("change"))}</td><td class="{cls}">{esc(x.get("trend"))}</td></tr>')
    comp=d.get('comparison') or {};desc='首次月报，本月不做上月环比。' if comp.get('first_month') else f"与{esc(comp.get('previous_month_label') or '上月')}对比。"
    main+='<section id="trend"><h2>02｜与上月对比｜学习趋势</h2><p class="desc">'+desc+'</p><table><thead><tr><th>指标</th><th>上月</th><th>本月</th><th>变化</th><th>趋势</th></tr></thead><tbody>'+rows_or_note(tr,5,'暂无可直接比较的同口径数据。')+'</tbody></table></section>'
    # Sessions
    cards=[]
    for key,label in [('math','Math'),('english','English')]:
        x=tut.get(key) or {};kind='green' if x.get('delivered')==x.get('required') else 'red'
        cards.append(f'<div class="session-card"><h3>{label}</h3><div class="session-kpis"><div class="session-kpi"><div class="n">{esc(x.get("required",0))}</div><div class="t">本月应上</div></div><div class="session-kpi"><div class="n">{esc(x.get("delivered",0))}</div><div class="t">本月已上</div></div><div class="session-kpi"><div class="n">{tag(x.get("status") or "未完成",kind)}</div><div class="t">完成状态</div></div></div><div class="feedback"><b>本月重点：</b>{esc(x.get("focus") or "暂无总结")}</div></div>')
    main+=f'<section id="sessions"><h2>03｜本月数学 / 英语专项辅导</h2><p class="desc">按{esc(tut.get("service_weeks",0))}个服务周统计；每周Math 2次 + English 2次，每次30分钟。</p><div class="session-grid">{"".join(cards)}</div></section>'
    # Ability map + deep analysis
    rows=[]
    for x in d.get('ability_map') or []:
        k=x.get('status_kind') or 'watch';cls='status-good' if k=='good' else ('status-alert' if k=='alert' else 'status-watch');prev='—' if x.get('previous_occurrence') in (None,'') else f"{esc(x.get('previous_occurrence'))}次"
        rows.append(f'<tr><td><b>{esc(x.get("subject"))}｜{esc(x.get("issue"))}</b></td><td>{esc(x.get("occurrence"))}次</td><td>{prev}</td><td><span class="{cls}">{esc(x.get("status"))}</span></td><td>{esc(x.get("judgment"))}</td></tr>')
    deep=[]
    for x in d.get('deep_analysis') or []:
        deep.append(f'<div class="analysis-card"><h3>{esc(x.get("title"))}</h3><div class="problem-chain"><div class="label">本月表现</div><div>{esc(x.get("performance"))}</div><div class="label">错误链</div><div>{esc(x.get("error_chain"))}</div><div class="label">当前判断</div><div>{esc(x.get("judgment"))}</div><div class="label">教学动作</div><div>{esc(x.get("teaching_action"))}</div></div></div>')
    main+='<section id="wrong"><h2>04｜本月错题分析｜能力问题地图</h2><p class="desc">只纳入整月重复出现、跨任务出现或具备充分证据的问题；单次错误不升级为能力问题。</p><table><thead><tr><th>能力 / 问题</th><th>本月出现</th><th>上月</th><th>状态</th><th>当前判断</th></tr></thead><tbody>'+rows_or_note(rows,5,'本月暂无达到稳定重复阈值的问题。')+'</tbody></table><h3 style="margin:20px 0 10px;font-size:17px">重点问题深度分析</h3><div class="analysis-grid">'+(''.join(deep) or '<div class="note">当前证据不足以形成更深层问题链分析。</div>')+'</div></section>'
    # Intervention
    rows=[]
    for x in d.get('interventions') or []:
        k=x.get('status_kind') or 'watch';cls='status-good' if k=='good' else ('status-alert' if k=='alert' else 'status-watch')
        rows.append(f'<tr><td>{esc(x.get("focus"))}</td><td>{esc(x.get("action"))}</td><td>{esc(x.get("previous"))}</td><td>{esc(x.get("current"))}</td><td><span class="{cls}">{esc(x.get("status"))}</span>｜{esc(x.get("next_step"))}</td></tr>')
    main+='<section id="intervention"><h2>05｜教学动作与干预效果追踪</h2><table><thead><tr><th>上阶段重点</th><th>采取的教学动作</th><th>前期表现</th><th>本月表现</th><th>状态 / 下一步</th></tr></thead><tbody>'+rows_or_note(rows,5,'当前暂无足够的前后对比证据形成干预效果判断。')+'</tbody></table></section>'
    # Mock
    rows=[f'<tr><td>{esc(x.get("name"))}</td><td>{esc(x.get("date"))}</td><td>{esc(x.get("score"))}</td><td>{esc(x.get("subscores"))}</td><td>{esc(x.get("alignment"))}</td></tr>' for x in mock.get('tests') or []]
    note=mock.get('note') or ('本月月度模拟测试未完成。' if mock.get('status')=='not_completed' else '本月月测数据未提供。')
    main+='<section id="mock"><h2>06｜月度模拟测试</h2><p class="desc">只使用本月实际提供的模拟测试/月测数据，不从日常作业推测成绩。</p><table><thead><tr><th>测试</th><th>日期</th><th>成绩</th><th>分项表现</th><th>与日常记录的对应</th></tr></thead><tbody>'+rows_or_note(rows,5,note)+'</tbody></table></section>'
    # Habits
    rows=[f'<tr><td>{esc(x.get("dimension"))}</td><td>{esc(x.get("change"))}</td><td>{esc(x.get("next_focus"))}</td></tr>' for x in d.get('habits') or []]
    main+='<section id="habit"><h2>07｜本月学习过程与习惯变化</h2><p class="desc">由本月到校日的可观察行为汇总，不使用泛化评价。</p><table><thead><tr><th>维度</th><th>本月可观察变化</th><th>下月关注</th></tr></thead><tbody>'+rows_or_note(rows,3,'本月暂无可汇总的习惯记录。')+'</tbody></table></section>'
    # Route
    mods=[]
    for mod in d.get('route_modules') or []:
        rows=[f'<tr><td>{esc(x.get("item"))}</td><td>{esc(x.get("status"))}</td><td>{esc(x.get("change_risk"))}</td><td>{esc(x.get("next_action"))}</td></tr>' for x in mod.get('rows') or []]
        mods.append(f'<div class="route-module"><h3>{esc(mod.get("title"))}</h3><div class="inner"><table><thead><tr><th>项目</th><th>本月状态</th><th>变化 / 风险</th><th>下月动作</th></tr></thead><tbody>{rows_or_note(rows,4,"暂无记录")}</tbody></table></div></div>')
    main+='<section id="route"><h2>08｜路线管理与升学节点追踪</h2><div class="callout" style="margin-bottom:14px"><b>当前状态：</b>'+esc(d.get('route_summary') or route.get('note') or '暂无更新')+'</div><div class="route-grid">'+''.join(mods)+'</div></section>'
    # Next
    lis=''.join(f'<li>{esc(x)}</li>' for x in d.get('next_month_focus') or [])
    main+='<section id="next"><h2>09｜下月重点 & 家长沟通</h2><div class="grid2"><div class="card"><h3 style="margin-top:0">下月重点</h3><ol>'+lis+'</ol></div><div class="card"><h3 style="margin-top:0">本月家长沟通重点</h3><p>'+esc(d.get('parent_communication_focus'))+'</p></div></div></section><div class="footer">'+esc(d.get('footer') or '机构学习管理月度报告')+'</div>'
    out=template.replace('__HEADER__',header).replace('__NAV__',nav).replace('__MAIN__',main);Path(a.output_html).write_text(out,encoding='utf-8')
if __name__=='__main__':main()
