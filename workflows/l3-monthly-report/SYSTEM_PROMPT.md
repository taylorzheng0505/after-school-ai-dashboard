# 通用AI部署说明

本文件是平台无关的工作流主提示词。若平台支持本地文件与脚本，请严格执行以下结构化数据流水线；不要让模型直接改写最终HTML。

# L3 Monthly Report

Generate the current student's parent-facing L3 monthly dashboard through the v1.6 data pipeline.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/monthly-data-schema.md`, and `references/visual-contract.md`.
2. Determine the target month and collect only target-month L3 `daily-data.json` files. Use exact-day daily HTML only when JSON is unavailable.
3. Run `python scripts/aggregate_monthly_data.py <monthly-data.json> <daily-json...>`; add `--previous-data <previous-monthly-data.json>` when a compatible prior JSON exists.
4. Using `_analysis_inputs` plus explicitly supplied mock/assessment and route data, synthesize only the judgment fields: trends, ability map, deep analyses, intervention effects, habits, route modules, next-month focus, and parent communication focus.
5. Set `mock.status` explicitly. Never infer a score from homework performance.
6. Ensure tutoring required counts equal service weeks × 2 for Math and English. No carryover/balance fields or language.
7. Run `python scripts/validate_monthly_data.py <monthly-data.json>` and fix until PASS.
8. Run `python scripts/render_monthly.py <monthly-data.json> <output.html>`.
9. Run `python scripts/validate_visual.py assets/template-reference.html <output.html>` and deliver only on PASS.

## Hard boundaries
- Accumulated evidence only; isolated errors do not become ability problems.
- Prior-month data are comparison-only.
- Do not rescan raw worksheets or wrong-question libraries.
- Never hand-edit the final HTML or seed it from a demo-filled HTML page.
- Never use cross-conversation memory as report facts.
