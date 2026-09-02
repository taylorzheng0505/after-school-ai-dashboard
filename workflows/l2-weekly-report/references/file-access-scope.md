# File access scope — weekly report

Use a strict allowlist. Do not recursively scan the student's whole workspace.

## Allowed sources
1. Stable profile documents for the current student when needed.
2. Daily reports belonging to the current student whose dates fall inside the requested reporting week.
3. Explicit supplemental weekly facts supplied by the supervisor when a daily report omitted a required item.

## Required behavior
- Filter by date/file name first, then read only matching daily reports.
- Derive wrong-question and dictation summaries from the daily reports.
- Derive long-cycle task progress from the daily reports.

## Forbidden sources by default
Do not scan raw homework/worksheet/test folders. Do not scan the standalone wrong-question library. Do not scan monthly reports or unrelated weeks. Do not re-crop original worksheets for a weekly report.

If a required day is missing or ambiguous, ask for the missing daily report or the attendance status instead of broadening the search.
