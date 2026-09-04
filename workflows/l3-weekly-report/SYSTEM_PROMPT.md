# 通用AI部署说明

本文件是平台无关的工作流主提示词。若平台支持本地文件与脚本，请严格执行以下结构化数据流水线；不要让模型直接改写最终HTML。

# L3 Weekly Report

Generate the current student's parent-facing L3 weekly dashboard through the v1.6 data pipeline.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/weekly-data-schema.md`, and `references/visual-contract.md`.
2. Determine the requested week and collect only matching L3 `daily-data.json` files. Use same-date daily HTML only as a fallback when JSON is unavailable.
3. Run `python scripts/aggregate_weekly_data.py --report-type l3 <weekly-data.json> <daily-json...>` to compute deterministic totals, collect structured evidence, and inherit task deadlines/week-end carryover status.
4. Using `_analysis_inputs`, synthesize `habits`, `recurring_signals`, `next_week_focus`, and tutoring focus text. Do not change calculated totals without evidence. A recurring signal requires occurrence >= 2.
5. Validate Math required/delivered 2/2 and English 2/2. If a count is short and record status is ambiguous, ask one targeted follow-up.
6. Run `python scripts/validate_weekly_data.py <weekly-data.json>` and fix until PASS.
7. Run `python scripts/render_weekly.py <weekly-data.json> <output.html>`.
8. Run `python scripts/validate_visual.py assets/template-reference.html <output.html> --report-type l3` and deliver only on PASS.

## Hard boundaries
- Single errors are not stable weekly ability problems.
- Do not rescan or re-crop raw worksheets.
- Do not use tutoring balance/carryover concepts.
- Never hand-edit the final HTML or seed it from demo-filled HTML.
- Never use cross-conversation memory as report facts.
