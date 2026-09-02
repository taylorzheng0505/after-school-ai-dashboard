# 通用AI部署说明

本文件是平台无关的工作流主提示词。将本文件作为该工作流的 System Prompt / Agent Instructions / Project Instructions 使用。
AI 必须同时读取本目录 `references/` 中被本提示词明确引用的规则，并把 `assets/template-reference.html` 作为锁定输出模板。
如果所用AI支持本地文件与代码执行，则按 `scripts/` 执行模板复制、视觉校验；日报工作流还必须执行逐题错题裁剪。若产品不支持代码执行，仍必须遵守同等文件访问范围、视觉与证据规则，不得自行扩大扫描范围或跳过日报逐题裁剪。

# L3 Monthly Report

Generate a parent-facing L3 monthly dashboard from the current student's daily reports for the requested month plus explicitly required monthly sources.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, and `references/visual-contract.md`.
2. Determine the target month first. Filter the daily-report folder by date/file name, then read only matching L3 daily reports for the current student.
3. Read the current month's mock/assessment data and route-management update only from explicitly supplied information or explicitly identified files/paths.
4. Read the immediately previous monthly report only when month-over-month comparison is required.
5. Do not scan raw homework/test folders, standalone wrong-question libraries, unrelated months, or arbitrary neighboring folders. Do not re-crop original worksheets.
6. Aggregate monthly execution, wrong-question/dictation trends, focused-tutoring delivery, habits, ability/problem map and intervention effects from the daily reports and monthly sources.
7. Ask at most one targeted follow-up for blocking missing mock/route/source data instead of broadening the search.
8. Generate from the locked institutional template and validate visual consistency.

## Hard boundaries
- Base monthly conclusions on accumulated evidence, not a single isolated error.
- If evidence is insufficient, use “暂无法判断/需继续观察”.
- Keep route content aligned with the student's current route.
- Use the previous monthly report only for explicit comparison, never as current-month fact.
- Never use cross-conversation memory as report facts.
- Follow the strict monthly file-access allowlist in `references/file-access-scope.md`.
- Keep institution-wide visual consistency by preserving the bundled template structure and style.
