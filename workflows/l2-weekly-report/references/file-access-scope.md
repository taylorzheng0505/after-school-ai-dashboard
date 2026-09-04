# File access scope — weekly report v1.6

Use a strict allowlist. Do not recursively scan the student workspace.

## Allowed sources
1. Stable profile documents for the current student when needed.
2. `daily-data.json` files belonging to the current student and requested week.
3. Only when a requested day's `daily-data.json` is unavailable, the corresponding daily HTML for that exact date may be used as a compatibility fallback.
4. Explicit supplemental weekly facts supplied by the supervisor when a daily record omitted a required item.

## Required behavior
- Determine the week first; filter by filename/date before opening content.
- Prefer `daily-data.json` over daily HTML. Do not open both when the JSON is complete.
- Derive wrong-question/dictation records and evidence paths from daily data.
- Derive long-cycle task progress from daily data.
- Never parse weekly information by scanning raw homework folders.

## Forbidden sources by default
Do not scan raw homework/worksheet/test folders. Do not scan the standalone wrong-question library. Do not scan monthly reports or unrelated weeks. Do not re-crop original worksheets.

If a required day is missing or ambiguous, ask for that day or its attendance status instead of broadening the search.
