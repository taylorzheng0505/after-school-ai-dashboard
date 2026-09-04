# Weekly Data Schema v1.7

The weekly report is data-driven. The AI must work on `weekly-data.json`, not hand-edit the final HTML.

The deterministic aggregator creates a preliminary JSON from the requested week's daily data files. The AI may then supplement only analytical/summary fields that require judgment.

```json
{
  "report_version": "1.7",
  "report_type": "l2",
  "student_name": "Alex",
  "grade": "G5",
  "period_display": "2026年9月1日–9月5日",
  "route": {"label":"转轨中","note":"当前：传统课程体系｜目标：国际学校路线"},
  "overview": {
    "attendance_days": 5,
    "effective_minutes": 706,
    "effective_display": "11h46m",
    "wrong_questions": 7,
    "dictation_errors": 3,
    "closure_text": "错题与听写均已闭环"
  },
  "daily_breakdown": [
    {"date":"9/1","main_tasks":"Math P12；English Grammar","ongoing":"Science Project：完成资料搜集（DDL 9/10）","effective":"2h18m"}
  ],
  "subjects": [
    {"subject":"Math","checked":48,"correct":45,"wrong":3,"accuracy":93.8,"correction_text":"3/3 已订正"}
  ],
  "ongoing_tasks": [
    {
      "subject":"Science",
      "task":"Project",
      "due_date":"2026-09-10",
      "progress":"本周完成Outline",
      "status":"in_progress",
      "deadline_state":"due_next_week",
      "carryover_to_next_week":true,
      "next_step":"下周继续Poster"
    }
  ],
  "wrong_records": [],
  "evidence": [],
  "habits": []
}
```

For L3 use `report_type: "l3"` and add `tutoring`, `recurring_signals`, and `next_week_focus` as in v1.6.

## Deadline / carryover rules
- Weekly reports inherit deadlines from daily `tasks[].due_date`; do not re-invent DDLs.
- `ongoing_tasks[]` includes all long-cycle tasks plus any task still unresolved at the end of the reporting week.
- `due_date` is ISO `YYYY-MM-DD` or `null` if genuinely unknown.
- `status` uses the latest daily status for that task (`done`, `in_progress`, `todo`/other unresolved values).
- `carryover_to_next_week` is `true` for any task unresolved at week end, regardless of whether its deadline is future or already overdue.
- `deadline_state` is one of: `completed`, `due_this_week`, `due_next_week`, `due_later`, `overdue`, `unknown`.
- Parent-facing weekly output must show the deadline column and clearly identify unfinished items that continue into next week.

## Machine-only aggregation fields
The preliminary aggregator may include `_analysis_inputs` containing raw habit observations and raw L3 wrong-question records. The renderer ignores `_analysis_inputs`.

## Evidence/image rule
- `image_path` must be a filesystem path to an already existing daily crop.
- Never put `data:image/...;base64,...` in `weekly-data.json`.
- Weekly reports do not rescan or re-crop raw worksheets.
- The renderer embeds image bytes only at final HTML rendering time.

## L3 recurrence rule
- A weekly `recurring_signals[]` item must have `occurrence >= 2`.
- A one-off error may remain in `wrong_records` but must not be promoted into a recurring signal.
