---
name: l2-daily-report
description: 生成课后托管 L2 学习执行日看板。用户提出“生成L2日报/日看板/今天托管反馈”等请求时使用。读取当前学生稳定档案与最近一份历史日报中的未完成长期任务；若当天已有标准作业批改 `grading-data.json`，优先直接复用其中的统计、错题编号和已裁剪证据图，不重新批改/分析/裁剪；没有标准批改报告的材料（如听写、临时小测、单题记录）仍由日报自行识别并裁剪。按固定机构HTML模板生成，错题卡桌面端固定两题一行。最多定向追问一次，严格保持L2边界，不输出错因诊断或专项教学建议。
---

# L2 Daily Report

Generate a parent-facing L2 daily dashboard through a controlled intake workflow.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/visual-contract.md`, and `references/cropping.md`.
2. Resolve stable profile fields from the current student's bound documents.
3. Read only the single most recent prior daily report before the target date and extract unfinished long-cycle/ongoing tasks **and their latest confirmed deadlines** for continuity. Do not inherit unrelated prior daily facts.
4. Check whether today already has a standardized homework-grading `grading-data.json` package supplied or explicitly pointed to by the supervisor. For every assignment covered by such a report, treat it as the preferred source for total/correct/wrong/accuracy, wrong-question IDs and referenced per-question crop paths. Do **not** re-grade, re-analyze or re-crop covered homework. L2 ignores analytical fields such as question type/ability/error cause even if they are present in the grading report.
5. For today's materials **not covered** by a standardized grading report, use the raw homework/test files or supervisor-provided grading result. The grading result may come from text, screenshot, file, pasted output from another AI, or current conversation; do not assume its location. If no grading result exists and the supervisor asks this AI to grade, grade only the explicitly identified current-day materials.
6. If critical inputs are incomplete, send the one-round intake prompt from `references/interaction.md`.
7. Parse supplied facts and build the task checklist with a deadline for every task, plus the wrong-question index. For covered homework, reuse the wrong-question crop paths referenced in grading-data.json.
8. For every confirmed wrong item **not already carrying a referenced crop from a grading report**, and whose source is a full worksheet/page, mandatory: create a per-question evidence crop following `references/cropping.md`.
9. Run completeness checks. If status is RED, ask one targeted follow-up containing all blocking gaps.
10. Generate one self-contained HTML file through the locked renderer; do not hand-edit the full HTML.

## Production rendering
1. Build a **small `daily-data.json`** following `references/daily-data-schema.md`. Never place base64 image strings in this JSON.
2. For homework covered by `grading-data.json`, reuse its counts, wrong-item fields and `evidence_image_path` values. **Do not read `grading-report.html` when the JSON is available.**
3. For uncovered materials, create any mandatory evidence crop first, then reference its file path from `daily-data.json`.
4. Run `python scripts/validate_daily_data.py daily-data.json`. Fix all errors.
5. Run `python scripts/render_daily.py daily-data.json <output.html>`. The renderer reads image files directly and embeds them into the final self-contained HTML; the model must not manually copy, decode, inspect or rewrite base64 image strings.
6. Preserve the locked two-column desktop wrong-question grid through the renderer. A single card remains in the left column.
7. Run `python scripts/validate_visual.py assets/template-reference.html <output.html>` and deliver only on `PASS`.

## Hard boundaries
- When a standard grading package exists, **read `grading-data.json` first and only use the specific crop paths referenced for this daily output. Do not parse the human-facing `grading-report.html` unless the JSON is missing or invalid.**
- Never load or manipulate base64 image payloads during reasoning. Image embedding is a deterministic renderer step.
- Stay within L2 scope: execution management only.
- Do not diagnose why a question was wrong or output ability/remediation judgments.
- Preserve original visual evidence; OCR/transcription may assist indexing but must not replace it.
- Describe learning habits with observable behavior, not vague praise.
- Never use cross-conversation memory as report facts.
- Apply Fresh-State to all date-specific facts while preserving continuity only for unfinished long-cycle tasks from the single latest prior daily report.
- **Deadline rule:** every task must carry `due_date`. Clear same-day homework may default to the report date; active long-cycle/staged tasks must preserve their actual confirmed DDL from the source/prior daily. If still unknown after one material follow-up, show “未明确” rather than inventing a date.
- Do not recursively scan weekly/monthly/history/wrong-question folders. Follow `references/file-access-scope.md`.
- A standardized grading report with referenced crops is authoritative for covered homework: never re-grade, re-analyze or re-crop it in L2 daily generation.
- Per-question cropping remains mandatory for uncovered full-page materials such as dictation, ad-hoc tests or assignments without a grading report. Whole-page evidence is exception-only after conservative crop failure.
- Keep institution-wide visual consistency by preserving the bundled template structure and style.
