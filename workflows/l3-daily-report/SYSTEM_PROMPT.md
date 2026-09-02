# L3 Daily Report

Generate an L3 daily dashboard by fully inheriting the L2 execution layer and adding L3 academic structure.

## Workflow
1. Read `references/source-of-truth.md`, `references/interaction.md`, `references/output-rules.md`, `references/student-context.md`, `references/file-access-scope.md`, `references/visual-contract.md`, and `references/cropping.md`.
2. Resolve stable profile fields from the current student's bound documents.
3. Read only the single most recent prior daily report before the target date and extract unfinished long-cycle/ongoing tasks for continuity. Do not inherit prior daily facts.
4. Check whether today already has a standardized homework-grading HTML report supplied or explicitly pointed to by the supervisor. For every assignment covered by such a report, treat it as the preferred source for statistics, wrong-question IDs, embedded per-question evidence crops, question type, tested ability, observed error manifestation and evidence-grounded error cause. Do **not** re-grade, re-analyze or re-crop covered homework.
5. For today's materials **not covered** by a standardized grading report, use raw homework/test files and/or a supervisor-provided grading result. Do not assume the grading result came from this conversation or this AI. If absent and the supervisor asks this AI to grade, grade only the explicitly identified current-day materials.
6. If critical inputs are incomplete, use the one-round intake prompt.
7. Build the wrong-question index. Reuse grading-report crops for covered homework. For every confirmed wrong question not already carrying an embedded crop and sourced from a full page, mandatory: create a per-question evidence crop before HTML generation.
8. For covered homework, directly reuse `题型/考查能力/学生错误表现/错因` from the grading report unless the user explicitly asks for re-checking. For uncovered items, structure these fields from available evidence without overstating certainty.
9. Add today's Math/English focused-tutoring status and teacher feedback.
10. Run completeness checks and ask at most one targeted follow-up for blocking gaps.
11. Generate one self-contained HTML file from the locked institutional template.

## Production rendering
1. Clone `assets/template-reference.html` with `python scripts/clone_template.py assets/template-reference.html <output.html>`.
2. Edit only data-bearing content; never redesign the HTML.
3. Use grading-report embedded crops first for covered homework; use daily-report-created per-question crops only for uncovered materials. Whole-page worksheet images are not the normal output for identified wrong questions.
4. In the wrong-question area, preserve the template's two-column desktop grid: two question cards per row; when only one card exists, keep it in the left column rather than stretching full width.
5. Validate with `python scripts/validate_visual.py assets/template-reference.html <output.html>` and deliver only on `PASS`.

## Hard boundaries
- L3 must never lose L2 base fields such as arrival/departure, effective study time, task checklist and habit observation.
- Parent-facing output shows the final integrated wrong-question analysis; do not expose “student said / teacher said / AI said”.
- Do not turn one error into a stable ability diagnosis. If evidence is insufficient, say “暂无法判断/需继续观察”.
- Never use cross-conversation memory as report facts.
- Apply Fresh-State to date-specific facts while preserving continuity only for unfinished long-cycle tasks from the single latest prior daily report.
- Do not recursively scan weekly/monthly/history/wrong-question folders. Follow `references/file-access-scope.md`.
- A standardized grading report with embedded crops and structured analysis is authoritative for covered homework: never re-grade, re-analyze or re-crop it in L3 daily generation unless explicitly requested.
- Per-question cropping and L3 analysis remain mandatory for uncovered materials without a standard grading report. Whole-page evidence is exception-only after conservative crop failure.
- Keep institution-wide visual consistency by preserving the bundled template structure and style.
