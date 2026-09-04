# Weekly report generation rules v1.6

## Data-driven production
- The model must produce/edit `weekly-data.json`, not hand-edit final HTML.
- Run `aggregate_weekly_data.py` first to compute deterministic totals and collect daily records.
- Use AI judgment only to synthesize the fields that cannot be calculated mechanically, such as weekly habit summaries and (for L3) recurring signals / next-week focus.
- Run `validate_weekly_data.py` before rendering.
- Run `render_weekly.py` to generate final HTML.
- Run `validate_visual.py` before delivery.

## Calculations
- Do not ask the supervisor to total hours, question counts, accuracy, or session counts when source daily data contains them.
- Only objective scorable tasks contribute to subject accuracy.
- Keep normal wrong questions and dictation errors separate.
- Long-cycle tasks never create a misleading overall task-completion rate.
- Inherit task deadlines from daily data. The weekly ongoing/carryover table must show each task's deadline and latest status. Any unresolved item at week end is explicitly marked as continuing into next week; overdue items are labeled as overdue rather than silently rolled forward.

## Evidence
- Reuse evidence image paths already present in daily data.
- Never re-scan or re-crop raw worksheets for weekly reports.
- Never put base64 strings inside `weekly-data.json`; only the renderer embeds image bytes into final HTML.

## L2 boundary
- L2 summarizes execution facts, objective statistics, errors and habits only.
- Do not add question-type/ability/error-cause diagnosis to parent-facing L2 weekly output.

## L3 boundary
- Recurring signals require at least 2 occurrences in the week.
- Single isolated errors remain records but are not promoted into stable problems.
- Validate Math 2 sessions and English 2 sessions for the week.
- Do not create balance/carryover fields or language.

## Output
- The template is a clean visual shell with placeholders only. It contains no demo student data.
- The model must not manually rewrite the HTML. The renderer fills the shell from validated JSON.
- Return one parent-facing self-contained HTML as the primary deliverable; evidence images are embedded by the renderer.
