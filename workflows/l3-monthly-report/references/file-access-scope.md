# File access scope — L3 monthly report v1.6

Use a strict allowlist. Do not recursively scan the student workspace.

## Allowed sources
1. Stable profile data when needed.
2. Target-month L3 `daily-data.json` files. Only if a day's JSON is unavailable, read that exact day's L3 daily HTML as a compatibility fallback.
3. Current-month mock/assessment data explicitly supplied or explicitly located.
4. Current-month route update explicitly supplied or explicitly located.
5. Previous `monthly-data.json` when comparison is required; if unavailable, use the immediately previous monthly HTML only as a compatibility fallback.
6. Explicit supplemental teacher facts when required source data are absent from daily data.

## Forbidden by default
Do not scan raw homework/test folders, standalone wrong-question libraries, unrelated historical months, or arbitrary sibling folders. Do not re-crop worksheets. Do not parse weekly reports when target-month daily data is available.

Filter by target month before opening files. If a required mock/route source is missing, ask for that exact source instead of broadening the search.
