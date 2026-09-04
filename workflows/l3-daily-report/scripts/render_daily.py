#!/usr/bin/env python3
import argparse, base64, html, json, mimetypes, re
from pathlib import Path


def esc(v):
    return "" if v is None else html.escape(str(v))


def data_uri(path_value, base_dir):
    if not path_value:
        return ""
    s = str(path_value)
    if s.startswith("data:image/"):
        return s
    p = Path(s)
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    if not p.exists():
        raise FileNotFoundError(f"image not found: {p}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def tag(text, kind="gray"):
    return f'<span class="tag {esc(kind)}">{esc(text)}</span>'


def due_display(task, report_date_text):
    due = task.get("due_date")
    if not due:
        return "未明确"
    due = str(due).strip()
    report_date = None
    m = re.search(r"(20\d{2})[年\-/](\d{1,2})[月\-/](\d{1,2})", str(report_date_text or ""))
    if m:
        report_date = f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    if due == report_date:
        return "当日"
    m2 = re.fullmatch(r"(20\d{2})-(\d{2})-(\d{2})", due)
    if m2:
        return f"{int(m2.group(2))}/{int(m2.group(3))}"
    return due


def render_tasks(tasks, report_date_text):
    rows = []
    for t in tasks:
        done = t.get("status", "done") == "done"
        mark, cls = ("✓", "done") if done else ("☐", "todo")
        if t.get("result_kind") == "na":
            result = tag(t.get("result_text") or "不适用", "gray")
        else:
            result = f'<b>{esc(t.get("result_text") or "")}</b>' if t.get("result_text") else "—"
        note = esc(t.get("note") or "")
        if t.get("long_cycle"):
            note = tag("长周期任务", "amber") + " " + note
        rows.append(
            f'<tr><td class="check {cls}">{mark}</td><td class="subject">{esc(t.get("subject"))}</td>'
            f'<td>{esc(t.get("task"))}</td><td>{esc(due_display(t, report_date_text))}</td><td>{result}</td><td>{note}</td></tr>'
        )
    return "".join(rows) if rows else '<tr><td colspan="6">今日暂无任务记录。</td></tr>'


def status_tags(item):
    parts = []
    if item.get("answered"):
        parts.append(tag("已答疑", "blue"))
    if item.get("corrected"):
        parts.append(tag("已订正", "green"))
    if item.get("status_text"):
        parts.append(tag(item.get("status_text"), item.get("status_kind") or "gray"))
    return "".join(parts)


def evidence_card(item, base_dir, analytical=False):
    src = data_uri(item.get("image_path"), base_dir) if item.get("image_path") else ""
    img = (
        f'<img alt="{esc(item.get("image_alt") or item.get("title") or "错题证据")}" src="{src}">'
        if src else '<div class="note">未提供可展示的原始证据图。</div>'
    )
    meta = ""
    if analytical:
        fields = [
            ("题型", item.get("question_type")),
            ("涉及能力", item.get("tested_ability")),
            ("错误表现", item.get("error_manifestation")),
            ("错因", item.get("error_cause")),
        ]
        meta = '<div class="error-meta">' + "".join(
            f'<div class="error-field"><b>{esc(k)}</b>{esc(v or "暂无法判断")}</div>' for k, v in fields
        ) + "</div>"
    else:
        source = item.get("source") or ""
        meta = f'<div class="small">来源：{esc(source)}</div>' if source else ""
    if item.get("result_text"):
        meta += f'<div class="small">{esc(item.get("result_text"))}</div>'
    st = status_tags(item)
    if st:
        meta += f'<div class="small">{st}</div>'
    return f'<div class="evidence"><h3>{esc(item.get("title") or "错题")}</h3>{img}{meta}</div>'


def render_wrong(data, base_dir, report_type):
    analytical = report_type == "l3"
    q = data.get("wrong_questions") or []
    d = data.get("dictation_errors") or []
    qcards = "".join(evidence_card(x, base_dir, analytical) for x in q) or '<div class="note">今日无题目错题。</div>'
    dcards = "".join(evidence_card(x, base_dir, analytical) for x in d) or '<div class="note">今日无听写错误。</div>'
    qtab = "l3dq" if analytical else "l2dq"
    dtab = "l3dd" if analytical else "l2dd"
    title = "02｜今日错题｜结构化记录" if analytical else "02｜今日错题"
    desc = (
        "每道错题使用独立证据裁图，并记录题型、涉及能力/知识点、错误表现与错因。桌面端固定两题一行，单题仅占左侧卡位。"
        if analytical else
        "题目错题与听写错误分开展示。每道错题使用独立证据裁图；桌面端固定两题一行，单题仅占左侧卡位。"
    )
    return (
        f'<section id="wrong"><h2>{title}</h2><p class="desc">{desc}</p><div class="tabs">'
        f'<div class="tab-bar"><button class="tab-btn active" data-tab="{qtab}">题目错题 {tag(str(len(q))+"题","red")}</button>'
        f'<button class="tab-btn" data-tab="{dtab}">听写错题 {tag(str(len(d))+"项","amber")}</button></div>'
        f'<div class="tab-panel active" id="{qtab}"><div class="wrong-card-grid">{qcards}</div></div>'
        f'<div class="tab-panel" id="{dtab}"><div class="wrong-card-grid">{dcards}</div></div></div></section>'
    )


def render_habits(habits, idx):
    cards = "".join(
        f'<div class="habit"><b>{esc(h.get("label"))}</b><span>{esc(h.get("text"))}</span></div>' for h in habits
    )
    return (
        f'<section id="habit"><h2>{idx:02d}｜学习过程与习惯</h2>'
        f'<p class="desc">只记录可观察行为，不用“认真、努力”等泛化评价。</p>'
        f'<div class="habit-grid">{cards}</div></section>'
    )


def render_lessons(lessons):
    cards = []
    for x in lessons:
        state = tag(
            x.get("tag_text") or ("已完成" if x.get("completed") else "今日未安排"),
            x.get("tag_kind") or ("green" if x.get("completed") else "gray"),
        )
        if x.get("completed"):
            state = tag("专项辅导", "violet") + state
        cards.append(
            f'<div class="lesson"><h3>{esc(x.get("title"))}</h3><div>{state}</div>'
            f'<div class="feedback">{esc(x.get("feedback") or "")}</div></div>'
        )
    return (
        '<section id="lesson"><h2>03｜数学 / 英语专项辅导</h2>'
        '<p class="desc">L3每周固定Math 2次 + English 2次，每次30分钟；日报只记录当天实际发生的专项辅导。</p>'
        f'<div class="grid2">{"".join(cards)}</div></section>'
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("output_html")
    ap.add_argument("--template", default=str(Path(__file__).resolve().parents[1] / "assets" / "template-reference.html"))
    args = ap.parse_args()

    jp = Path(args.json_path).resolve()
    data = json.loads(jp.read_text(encoding="utf-8"))
    base = jp.parent
    template = Path(args.template).read_text(encoding="utf-8")
    rt = data.get("report_type")
    if rt not in {"l2", "l3"}:
        raise SystemExit("report_type must be l2 or l3")

    route = data.get("route") or {}
    timing = data.get("timing") or {}
    counts = data.get("counts") or {}
    subtitle = "｜".join([x for x in [data.get("student_name"), data.get("grade"), data.get("date_display")] if x])
    pills = [
        f'到校 {timing.get("arrival","")}',
        f'离校 {timing.get("departure","")}',
        f'有效学习 {timing.get("effective","")}',
        f'题目错题 {counts.get("wrong_questions",len(data.get("wrong_questions") or []))}题',
        f'听写错误 {counts.get("dictation_errors",len(data.get("dictation_errors") or []))}项',
    ]
    if rt == "l3":
        pills.append(f'今日专项辅导 {counts.get("tutoring_sessions",0)}次·30min')

    title = "L3 学业管理日看板" if rt == "l3" else "L2 学习执行日看板"
    header = (
        f'<header><div class="wrap"><h1>{title}</h1><div class="sub">{esc(subtitle)}</div>'
        f'<div class="route-strip"><b>当前升学路线</b><span class="route-badge">{esc(route.get("label") or "未提供")}</span>'
        f'<span class="route-note">{esc(route.get("note") or "")}</span></div><div class="meta">'
        + "".join(f'<span class="pill">{esc(x)}</span>' for x in pills) + '</div></div></header>'
    )
    if rt == "l3":
        nav = '<nav><div class="wrap"><a href="#tasks">今日任务</a><a href="#wrong">今日错题</a><a href="#lesson">专项辅导</a><a href="#habit">学习过程与习惯</a><a href="#note">今日备注</a></div></nav>'
    else:
        nav = '<nav><div class="wrap"><a href="#tasks">今日任务</a><a href="#wrong">今日错题</a><a href="#habit">学习过程与习惯</a><a href="#note">今日备注</a></div></nav>'

    task_desc = "逐项记录当天任务执行结果；长周期任务单独展示当天推进情况。" if rt == "l3" else "逐项对应CJ/学校作业清单；完成后打勾。长周期任务单独展示当天推进情况与当前进度。"
    tasks = (
        f'<section id="tasks"><h2>01｜今日任务 Checklist</h2><p class="desc">{task_desc}</p><table><thead><tr>'
        '<th style="width:54px">状态</th><th style="width:90px">科目</th><th>具体任务</th>'
        '<th style="width:110px">截止日期</th><th style="width:145px">本次核对结果</th><th style="width:220px">完成情况 / 备注</th>'
        f'</tr></thead><tbody>{render_tasks(data.get("tasks") or [], data.get("date_display"))}</tbody></table></section>'
    )
    wrong = render_wrong(data, base, rt)
    if rt == "l3":
        main_content = tasks + wrong + render_lessons(data.get("tutoring") or []) + render_habits(data.get("habits") or [], 4)
        main_content += f'<section id="note"><h2>05｜今日执行备注</h2><div class="note">{esc(data.get("note") or "")}</div></section>'
    else:
        main_content = tasks + wrong + render_habits(data.get("habits") or [], 3)
        main_content += f'<section id="note"><h2>04｜今日执行备注</h2><div class="note">{esc(data.get("note") or "")}</div></section>'
    footer = f'<div class="footer">{esc(data.get("footer") or "机构学习管理看板")}</div>'
    out = template.replace("__HEADER__", header).replace("__NAV__", nav).replace("__MAIN__", main_content + footer)
    Path(args.output_html).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
