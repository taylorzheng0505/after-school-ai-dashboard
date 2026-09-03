# Daily Data Schema v1.5

The AI reasoning stage must output a small JSON data file. Do not write or manipulate base64 image strings. The renderer reads image paths and embeds the bytes into the final self-contained HTML.

```json
{
  "report_version": "1.5",
  "report_type": "l2",
  "student_name": "Alex",
  "grade": "G5",
  "date_display": "2026年9月3日 星期四",
  "route": {"label": "转轨中", "note": "当前：传统课程体系｜目标：国际学校路线"},
  "timing": {"arrival": "16:12", "departure": "19:28", "effective": "2h31min"},
  "counts": {"wrong_questions": 2, "dictation_errors": 1},
  "tasks": [
    {"status":"done","subject":"Math","task":"Homework P16 T1-T10","result_kind":"scored","result_text":"8 / 10（80%）","note":"全部完成；2题错误，已订正。","long_cycle":false}
  ],
  "wrong_questions": [
    {"title":"Math｜Q3","source":"Homework 1｜Q3","image_path":"crops/math-q3.png","answered":true,"corrected":true}
  ],
  "dictation_errors": [],
  "habits": [{"label":"自主启动","text":"核对任务清单后5分钟内开始第一项任务。"}],
  "note": "今日执行备注。"
}
```

For L3, set `report_type: l3`, add `counts.tutoring_sessions`, add `question_type`, `tested_ability`, `error_manifestation`, `error_cause` to each wrong-question/dictation record, and include:

```json
"tutoring": [
  {"title":"English｜今日 1次 · 30min","completed":true,"feedback":"老师课后反馈……"},
  {"title":"Math｜今日无专项辅导","completed":false,"feedback":"本周按排期在其他服务日完成。"}
]
```

## Image rule
- `image_path` is a filesystem path or relative path to the existing crop.
- Never put `data:image/...;base64,...` into the JSON.
- When a standard grading `grading-data.json` exists, copy/reuse its `evidence_image_path` into `image_path`. Do not read the human-facing grading HTML just to retrieve the image.
- For uncovered materials, create a crop first and then reference its path.
