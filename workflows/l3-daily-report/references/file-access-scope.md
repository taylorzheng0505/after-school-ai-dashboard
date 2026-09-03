# File access scope — daily report

Use a strict allowlist. Do not recursively scan the student's whole workspace.

## Allowed sources
1. Stable profile documents for the current student.
2. The **single most recent existing daily report before the target date**, only to identify long-cycle / ongoing / explicitly carried-forward tasks.
3. Today's standardized homework-grading `grading-data.json` file(s), when supplied or explicitly pointed to, plus only the crop image paths referenced by wrong items needed in today's dashboard. These are the preferred sources for covered assignments.
4. Today's raw homework / worksheet / test files or folders explicitly identified by the supervisor, but only for materials not covered by a complete standardized grading report or when the user explicitly requests re-checking.
5. Today's grading result supplied by the supervisor in any usable form: text, screenshot, uploaded file, pasted result from another AI, or an earlier message in the same conversation. Do not assume where the grading result comes from.
6. Today's execution facts supplied for this report: arrival/departure/effective time, task progress, corrections, habit observations, exceptions, and (for L3) focused tutoring.

## Previous-report continuity rule
Read only the latest prior daily report, not the full history. From it, extract only unfinished long-cycle tasks, ongoing projects, staged reading, or explicitly deferred tasks. Use these items to ask for today's progress if the supervisor has not already provided it. Never auto-mark the prior next step as completed today.

Do not inherit prior arrival/departure time, effective time, correctness, wrong questions, dictation, habit observations, exceptions, or tutoring records.

## Grading-report priority rule
If a complete standardized homework-grading package maps to an assignment, use `grading-data.json` as the authoritative working interface. Use only the crop paths referenced by wrong items needed for this daily output. Do not open `grading-report.html` unless JSON is missing/invalid and do not reopen raw pages merely to repeat grading, analysis or cropping. Only fall back to raw materials when the package is incomplete or the user explicitly requests re-checking.

## Grading-result rule
For uncovered materials, a grading result may have been produced by this AI or another AI. If supplied and clearly mapped to today's source materials, reuse it and do not re-grade unless the supervisor explicitly asks. If absent and the supervisor asks this AI to grade, grade today's explicitly identified raw files first.

## Forbidden broad discovery
Do not scan weekly reports, monthly reports, historical wrong-question libraries, unrelated date folders, or sibling folders “just in case”. If a required input is missing, ask for the exact file/path or the missing information instead of expanding scope automatically.

## Heavy-file avoidance
Do not recursively inspect `crops/`. Use the exact paths listed in `grading-data.json`. Do not read base64/data-URI strings from HTML during normal operation.
