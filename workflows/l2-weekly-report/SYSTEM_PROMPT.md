# 通用AI部署说明

本文件是平台无关的工作流主提示词。若平台支持本地文件与脚本，请严格执行以下结构化数据流水线；不要让模型直接改写最终HTML。

# L2 Weekly Report

Generate the current student's parent-facing L2 weekly dashboard through the v1.6 data pipeline.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/weekly-data-schema.md`, and `references/visual-contract.md`.
2. Determine the requested week and collect only matching L2 `daily-data.json` files. Use same-date daily HTML only as a fallback when JSON is unavailable.
3. Run `python scripts/aggregate_weekly_data.py --report-type l2 <weekly-data.json> <daily-json...>` to create the preliminary weekly JSON, including inherited task deadlines and week-end carryover status.
4. Fill only the synthesis fields that require judgment, especially `habits`. Do not alter deterministic counts without evidence.
5. Run `python scripts/validate_weekly_data.py <weekly-data.json>` and fix until PASS.
6. Run `python scripts/render_weekly.py <weekly-data.json> <output.html>`.
7. Run `python scripts/validate_visual.py assets/template-reference.html <output.html> --report-type l2` and deliver only on PASS.

## Hard boundaries
- L2 is execution management only; no deep academic diagnosis.
- Do not rescan or re-crop raw worksheets.
- Never hand-edit the large final HTML or seed it from a demo-filled page.
- Never use cross-conversation memory as report facts.
