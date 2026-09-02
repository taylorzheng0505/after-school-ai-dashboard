#!/usr/bin/env python3
import argparse, base64, html, json, mimetypes
from pathlib import Path


def esc(v):
    if v is None:
        return ""
    return html.escape(str(v))


def fmt_answer(v):
    if v is None or v == "":
        return "—"
    return esc(v)


def badge(status):
    return {
        "correct": '<span class="badge ok">正确</span>',
        "wrong": '<span class="badge bad">错误</span>',
        "pending_review": '<span class="badge pending">待复核</span>',
    }.get(status, esc(status))


def to_data_uri(path_value, base_dir):
    if not path_value:
        return None
    s = str(path_value)
    if s.startswith("data:image/"):
        return s
    p = Path(s)
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    if not p.exists():
        raise FileNotFoundError(f"evidence image not found: {p}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def evidence_html(q, base_dir):
    status = q.get("evidence_crop_status") or ""
    if status == "not_applicable":
        return '<div class="evidence-note">本题无可用原始视觉证据。</div>'
    paths = q.get("evidence_image_paths") or []
    if q.get("evidence_image_path"):
        paths = [q.get("evidence_image_path")] + list(paths)
    # de-duplicate preserving order
    seen = set(); clean=[]
    for p in paths:
        if p and str(p) not in seen:
            seen.add(str(p)); clean.append(p)
    if not clean:
        reason = esc(q.get("evidence_exception") or "未提供可嵌入的错题证据图")
        return f'<div class="evidence-note exception">证据图异常：{reason}</div>'
    assignment = str(q.get("assignment_id", ""))
    question = str(q.get("question_id", ""))
    base_dom = q.get("evidence_dom_id") or f"evidence-{assignment}-{question}"
    imgs=[]
    for i,p in enumerate(clean):
        src = to_data_uri(p, base_dir)
        dom = base_dom if len(clean)==1 else f"{base_dom}-{i+1}"
        imgs.append(
            f'<img id="{esc(dom)}" data-evidence-role="wrong-question-crop" '
            f'data-assignment-id="{esc(assignment)}" data-question-id="{esc(question)}" '
            f'alt="{esc(assignment)} {esc(question)} 原始错题裁图" src="{src}">'
        )
    return '<div class="wrong-evidence">' + ''.join(imgs) + '</div>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("output_html")
    ap.add_argument("--template", default=str(Path(__file__).resolve().parents[1] / "assets" / "report-template.html"))
    args = ap.parse_args()
    json_path = Path(args.json_path).resolve()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    t = Path(args.template).read_text(encoding="utf-8")
    s = data["summary"]
    meta=[]
    if data.get("student_name"): meta.append(esc(data["student_name"]))
    if data.get("grade"): meta.append(esc(data["grade"]))
    if data.get("assignment_title"): meta.append(esc(data["assignment_title"]))
    header=f'''<div class="header"><h1>{esc(data.get("subject") or "作业")}批改报告</h1><div class="subtitle">{' · '.join(meta) if meta else '逐题批改与错题分析'}</div><div class="date">批改日期：{esc(data.get("grading_date") or '')}</div></div>'''
    stats=f'''<div class="stats"><div class="stat total"><div class="n">{s['total_questions']}</div><div class="l">总题目数</div></div><div class="stat correct"><div class="n">{s['correct_questions']}</div><div class="l">正确题数</div></div><div class="stat wrong"><div class="n">{s['wrong_questions']}</div><div class="l">错误题数</div></div><div class="stat rate"><div class="n">{s['accuracy']:.1f}%</div><div class="l">正确率</div></div></div>'''
    rows=[]
    for q in data["questions"]:
        qid=f"{q.get('assignment_id','')}-{q.get('question_id','')}".strip("-")
        source=q.get("source_locator") or q.get("source_file") or ""
        rows.append(f"<tr><td>{esc(qid)}</td><td>{esc(source)}</td><td>{fmt_answer(q.get('student_answer'))}</td><td>{fmt_answer(q.get('correct_answer'))}</td><td>{badge(q.get('status'))}</td></tr>")
    pending=s.get("pending_review",0)
    note=f'<div class="note">另有 {pending} 题待复核；正确率分母不含待复核题。</div>' if pending else ''
    question_table=f'''<div class="section"><div class="section-title">一、逐题批改结果</div><table><thead><tr><th>题号</th><th>题目来源</th><th>学生答案</th><th>正确/参考答案</th><th>判定</th></tr></thead><tbody>{''.join(rows)}</tbody></table>{note}</div>'''
    cards=[]
    wrongs=[q for q in data["questions"] if q.get("status")=="wrong"]
    for i,q in enumerate(wrongs,1):
        assignment=str(q.get('assignment_id',''))
        question=str(q.get('question_id',''))
        qid=f"{assignment}-{question}".strip("-")
        source=q.get("source_locator") or q.get("source_file") or ""
        ev=evidence_html(q, json_path.parent)
        cards.append(f'''<div class="error-card" data-assignment-id="{esc(assignment)}" data-question-id="{esc(question)}"><div class="error-head"><div class="qnum">{i}</div><div><div class="qtitle">{esc(qid)}｜{esc(q.get('question_type'))}</div><div class="qsource">{esc(source)}</div></div></div>{ev}<div class="detail-grid"><div class="detail"><div class="label">题型</div><div class="value">{esc(q.get('question_type'))}</div></div><div class="detail"><div class="label">考查能力</div><div class="value">{esc(q.get('tested_ability'))}</div></div><div class="detail"><div class="label">学生错误表现</div><div class="value red">{esc(q.get('error_manifestation'))}</div></div><div class="detail"><div class="label">正确/参考答案</div><div class="value green">{fmt_answer(q.get('correct_answer'))}</div></div><div class="detail full"><div class="label">错因</div><div class="value">{esc(q.get('error_cause'))}</div></div><div class="detail full"><div class="label">关键解析</div><div class="value">{esc(q.get('key_explanation'))}</div></div></div></div>''')
    error_details=f'''<div class="section"><div class="section-title">二、错题详细分析</div>{''.join(cards) if cards else '<div class="note">本次没有识别到错误题。</div>'}</div>'''
    patterns=data.get("pattern_summary") or []
    if patterns:
        phtml=''.join(f'<div class="pattern">{esc(p)}</div>' for p in patterns)
        pattern_summary=f'<div class="section"><div class="section-title">三、本次作业重复问题</div>{phtml}<div class="note">仅汇总本次作业中有重复证据的问题，不据单题形成长期能力诊断。</div></div>'
    else:
        pattern_summary=''

    # Hidden payload keeps analytical data but references DOM images instead of duplicating base64.
    payload_data=json.loads(json.dumps(data,ensure_ascii=False))
    for q in payload_data.get("questions",[]):
        q.pop("evidence_image_path",None)
        q.pop("evidence_image_paths",None)
    payload=json.dumps(payload_data,ensure_ascii=False).replace("</","<\\/")
    out=t.replace("__HEADER__",header).replace("__STATS__",stats).replace("__QUESTION_TABLE__",question_table).replace("__ERROR_DETAILS__",error_details).replace("__PATTERN_SUMMARY__",pattern_summary).replace("__DATA_JSON__",payload)
    Path(args.output_html).write_text(out,encoding="utf-8")

if __name__=="__main__":
    main()
