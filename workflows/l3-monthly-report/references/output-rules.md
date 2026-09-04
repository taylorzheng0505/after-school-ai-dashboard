# L3 monthly report generation rules v1.6

## Data-driven production
- The model must produce/edit `monthly-data.json`, not hand-edit final HTML.
- Run `aggregate_monthly_data.py` first to compute deterministic totals from target-month daily JSON files.
- Use AI judgment only for `trend_rows`, `ability_map`, `deep_analysis`, `interventions`, `habits`, `route_modules`, `next_month_focus`, and parent communication summary.
- Use explicitly supplied mock/route/prior-month data. Never infer missing scores or route events.
- Run `validate_monthly_data.py`, then `render_monthly.py`, then `validate_visual.py`.

## Evidence strength
- One isolated error cannot enter the monthly ability map.
- Repeated problems require accumulated evidence; `ability_map[].occurrence >= 2`.
- Intervention effects require before/after evidence. If insufficient, say so.
- Previous-month data are for explicit comparison only, never current-month facts.

## Tutoring
- Required sessions = service weeks × 2 for Math and × 2 for English.
- Display only required/delivered/status/focus. Do not use balance or carryover concepts.

## Output
- The template is a clean visual shell with no student/demo data.
- The model does not manually edit final HTML. The renderer generates it from validated JSON.
- Return one self-contained parent-facing HTML.
