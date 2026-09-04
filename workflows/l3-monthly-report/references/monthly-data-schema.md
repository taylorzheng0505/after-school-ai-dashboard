# Monthly Data Schema v1.6

The L3 monthly report is data-driven. The AI must work on `monthly-data.json`, not hand-edit the final HTML.

The deterministic aggregator first creates a preliminary JSON from the target month's L3 `daily-data.json` files. The AI then adds only the monthly judgment fields that require synthesis, using explicitly supplied mock/assessment data, route updates, and previous-month data when available.

```json
{
  "report_version":"1.6",
  "report_type":"l3_monthly",
  "student_name":"Alex",
  "grade":"G5",
  "month_display":"2026年9月",
  "route":{"label":"转轨中","note":"当前：传统课程体系｜目标：国际学校路线"},
  "overview":{"attendance_days":20,"effective_minutes":2852,"effective_display":"47h32m","wrong_questions":49,"dictation_errors":9},
  "subjects":[{"subject":"Math","checked":120,"correct":105,"wrong":15,"accuracy":87.5}],
  "comparison":{"first_month":false,"previous_month_label":"8月"},
  "trend_rows":[{"metric":"Math客观题错题率","previous":"16.8%","current":"12.6%","change":"-4.2pct","trend":"↓ 改善","trend_kind":"good"}],
  "tutoring":{
    "service_weeks":4,
    "math":{"required":8,"delivered":8,"status":"全部完成","focus":"英文应用题条件拆解"},
    "english":{"required":8,"delivered":8,"status":"全部完成","focus":"Inference与长句理解"}
  },
  "ability_map":[{"subject":"English","issue":"Inference","occurrence":6,"previous_occurrence":5,"status":"持续关注","status_kind":"watch","judgment":"推断强度仍偏高"}],
  "deep_analysis":[{"title":"重点问题 01｜English Inference","performance":"...","error_chain":"...","judgment":"...","teaching_action":"..."}],
  "interventions":[{"focus":"信息定位与改写识别","action":"同义改写训练","previous":"12次相关错误","current":"8次","status":"改善中","status_kind":"good","next_step":"继续巩固"}],
  "mock":{"status":"completed","note":"","tests":[{"name":"9月阶段模拟测试","date":"9/28","score":"84 / 100","subscores":"Math 86｜English 82","alignment":"与日常错题趋势一致"}]},
  "habits":[{"dimension":"自主启动","change":"20天中16天在5分钟内启动；较上月提升。","next_focus":"继续减少二次提醒。"}],
  "route_summary":"转轨中｜当前传统课程体系在读 → 目标国际学校路线。",
  "route_modules":[{"title":"国内线模块","rows":[{"item":"校内同步进度","status":"稳定","change_risk":"总体稳定","next_action":"保持"}]}],
  "next_month_focus":["Math专项继续处理英文条件理解"],
  "parent_communication_focus":"本月沟通重点围绕整体趋势、重点问题、专项辅导和路线进度。"
}
```

## Machine-only aggregation fields
The preliminary aggregator may include `_analysis_inputs` with:
- `wrong_records`: all structured wrong-question/dictation records from the month's daily data;
- `habit_observations`: raw daily habit observations;
- `tutoring_sessions`: all completed Math/English targeted sessions;
- `previous_month_data`: previous `monthly-data.json` if explicitly supplied.

These are inputs for the AI to synthesize `trend_rows`, `ability_map`, `deep_analysis`, `interventions`, `habits`, and next-month focus. The renderer ignores `_analysis_inputs`.

## Rules
- `ability_map[].occurrence` must be >= 2. One isolated error cannot become a monthly ability problem.
- Intervention effect claims require before/after evidence. If evidence is insufficient, state that explicitly.
- `mock.status` must be explicit: `completed`, `not_completed`, or `not_provided`. Never infer a score.
- Route modules must match the current route. Transition students may have both domestic and international modules; pure-route students should not display irrelevant modules.
- No tutoring carryover/balance fields exist in this schema.
