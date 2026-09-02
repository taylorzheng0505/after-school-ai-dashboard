# L2 Daily Report

Generate a parent-facing L2 daily dashboard through a controlled intake workflow.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/visual-contract.md`, and `references/cropping.md`.
2. Resolve stable profile fields from the current student's bound documents.
3. Read only the single most recent prior daily report before the target date and extract unfinished long-cycle/ongoing tasks for continuity. Do not inherit prior daily facts.
4. Check whether today already has a standardized homework-grading HTML report supplied or explicitly pointed to by the supervisor. For every assignment covered by such a report, treat it as the preferred source for total/correct/wrong/accuracy, wrong-question IDs and embedded per-question evidence crops. Do **not** re-grade, re-analyze or re-crop covered homework. L2 ignores analytical fields such as question type/ability/error cause even if they are present in the grading report.
5. For today's materials **not covered** by a standardized grading report, use the raw homework/test files or supervisor-provided grading result. The grading result may come from text, screenshot, file, pasted output from another AI, or current conversation; do not assume its location. If no grading result exists and the supervisor asks this AI to grade, grade only the explicitly identified current-day materials.
6. If critical inputs are incomplete, send the one-round intake prompt from `references/interaction.md`.
7. Parse supplied facts and build the task checklist and wrong-question index. For covered homework, reuse the wrong-question crops embedded in the grading HTML.
8. For every confirmed wrong item **not already carrying an embedded crop from a grading report**, and whose source is a full worksheet/page, mandatory: create a per-question evidence crop following `references/cropping.md`.
9. Run completeness checks. If status is RED, ask one targeted follow-up containing all blocking gaps.
10. Generate one self-contained HTML file by starting from `assets/template-reference.html` as the locked base template.

## Production rendering
1. Read `references/visual-contract.md`.
2. Clone `assets/template-reference.html` with `python scripts/clone_template.py assets/template-reference.html <output.html>`.
3. Edit only data-bearing content; never redesign the HTML.
4. Use grading-report embedded crops first for covered homework; use daily-report-created per-question crops only for uncovered materials. Do not embed a whole worksheet page as the normal substitute for an identified wrong question.
5. In the wrong-question area, preserve the template's two-column desktop grid: two question cards per row; when only one card exists, keep it in the left column rather than stretching full width.
6. Validate with `python scripts/validate_visual.py assets/template-reference.html <output.html>` and deliver only on `PASS`.

## Hard boundaries
- Stay within L2 scope: execution management only.
- Do not diagnose why a question was wrong or output ability/remediation judgments.
- Preserve original visual evidence; OCR/transcription may assist indexing but must not replace it.
- Describe learning habits with observable behavior, not vague praise.
- Never use cross-conversation memory as report facts.
- Apply Fresh-State to all date-specific facts while preserving continuity only for unfinished long-cycle tasks from the single latest prior daily report.
- Do not recursively scan weekly/monthly/history/wrong-question folders. Follow `references/file-access-scope.md`.
- A standardized grading report with embedded crops is authoritative for covered homework: never re-grade, re-analyze or re-crop it in L2 daily generation.
- Per-question cropping remains mandatory for uncovered full-page materials such as dictation, ad-hoc tests or assignments without a grading report. Whole-page evidence is exception-only after conservative crop failure.
- Keep institution-wide visual consistency by preserving the bundled template structure and style.
