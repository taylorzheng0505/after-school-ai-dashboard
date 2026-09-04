---
name: l3-daily-report
description: 生成课后托管 L3 学业管理日看板。用户提出“生成L3日报/日看板/今天L3反馈”等请求时使用。完整继承L2执行层并读取最近一份历史日报中的未完成长期任务；若当天已有标准作业批改 `grading-data.json`，优先直接复用其中的统计、逐题裁剪图、题型、考查能力、错误表现和错因，不重新批改/分析/裁剪；没有标准批改报告的材料仍由日报自行分析与裁剪，并记录当天Math/English专项辅导。按固定机构HTML模板生成，错题卡桌面端固定两题一行。
---

# L3 Daily Report

Generate an L3 daily dashboard by fully inheriting the L2 execution layer and adding L3 academic structure.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/visual-contract.md`, and `references/cropping.md`.
2. Resolve stable profile fields from the current student's bound documents.
3. Read only the single most recent prior daily report before the target date and extract unfinished long-cycle/ongoing tasks **and their latest confirmed deadlines** for continuity. Do not inherit unrelated prior daily facts.
4. Check whether today already has a standardized homework-grading `grading-data.json` package supplied or explicitly pointed to by the supervisor. For every assignment covered by such a report, treat it as the preferred source for statistics, wrong-question IDs, referenced per-question crop paths, question type, tested ability, observed error manifestation and evidence-grounded error cause. Do **not** re-grade, re-analyze or re-crop covered homework.
5. For today's materials **not covered** by a standardized grading report, use raw homework/test files and/or a supervisor-provided grading result. Do not assume the grading result came from this conversation or this AI. If absent and the supervisor asks this AI to grade, grade only the explicitly identified current-day materials.
6. If critical inputs are incomplete, use the one-round intake prompt.
7. Build the task checklist with a deadline for every task, then build the wrong-question index. Reuse the crop paths referenced by grading-data.json for covered homework. For every confirmed wrong question not already carrying a referenced crop and sourced from a full page, mandatory: create a per-question evidence crop before HTML generation.
8. For covered homework, directly reuse `题型/考查能力/学生错误表现/错因` from grading-data.json unless the user explicitly asks for re-checking. For uncovered items, structure these fields from available evidence without overstating certainty.
9. Add today's Math/English focused-tutoring status and teacher feedback.
10. Run completeness checks and ask at most one targeted follow-up for blocking gaps.
11. Generate one self-contained HTML file through the locked renderer; do not hand-edit the full HTML.

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
- L3 must never lose L2 base fields such as arrival/departure, effective study time, task checklist and habit observation.
- Parent-facing output shows the final integrated wrong-question analysis; do not expose “student said / teacher said / AI said”.
- Do not turn one error into a stable ability diagnosis. If evidence is insufficient, say “暂无法判断/需继续观察”.
- Never use cross-conversation memory as report facts.
- Apply Fresh-State to date-specific facts while preserving continuity only for unfinished long-cycle tasks from the single latest prior daily report.
- **Deadline rule:** every task must carry `due_date`. Clear same-day homework may default to the report date; active long-cycle/staged tasks must preserve their actual confirmed DDL from the source/prior daily. If still unknown after one material follow-up, show “未明确” rather than inventing a date.
- Do not recursively scan weekly/monthly/history/wrong-question folders. Follow `references/file-access-scope.md`.
- A standardized grading report with referenced crops and structured analysis is authoritative for covered homework: never re-grade, re-analyze or re-crop it in L3 daily generation unless explicitly requested.
- Per-question cropping and L3 analysis remain mandatory for uncovered materials without a standard grading report. Whole-page evidence is exception-only after conservative crop failure.
- Keep institution-wide visual consistency by preserving the bundled template structure and style.
