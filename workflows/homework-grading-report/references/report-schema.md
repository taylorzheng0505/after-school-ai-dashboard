# Report Data Schema

Use one JSON object with this shape:

```json
{
  "report_version": "1.5",
  "student_name": "",
  "subject": "Math",
  "grade": "G10",
  "assignment_title": "Homework 1",
  "grading_date": "2026-09-02",
  "summary": {
    "total_questions": 10,
    "correct_questions": 8,
    "wrong_questions": 2,
    "pending_review": 0,
    "accuracy": 80.0
  },
  "questions": [
    {
      "assignment_id": "HW1",
      "question_id": "3",
      "source_file": "homework-page-1.jpg",
      "source_locator": "page 1 / question 3",
      "student_answer": "C (1/3)",
      "correct_answer": "B (2/3)",
      "status": "wrong",
      "score": null,
      "max_score": null,
      "question_type": "单项选择题｜几何概型",
      "tested_ability": "理解几何概型；用目标区间/总体区间建立概率比值",
      "error_manifestation": "选择C(1/3)，正确答案为B(2/3)",
      "error_cause": "从答案表现看，更可能是比值方向处理错误，将目标与总体的关系颠倒。",
      "error_cause_evidence": "medium",
      "key_explanation": "P=(1/3)/(1/2)=2/3",
      "evidence_image_path": "crops/HW1-q3.png",
      "evidence_crop_status": "embedded",
      "evidence_dom_id": "evidence-HW1-q3"
    }
  ],
  "pattern_summary": []
}
```

## Rules

- All questions must have `assignment_id`, `question_id`, `status`, `student_answer`, and `correct_answer` when available.
- Every `wrong` question must have non-empty `question_type`, `tested_ability`, `error_manifestation`, `error_cause`, `key_explanation`, and `error_cause_evidence`.
- `error_cause_evidence` must be `high`, `medium`, or `low` for wrong questions.
- Correct questions may leave wrong-analysis fields empty.
- For a wrong question with an original visual source, set:
  - `evidence_image_path`: path to the per-question crop or already-single-question source image;
  - `evidence_crop_status`: `embedded`;
  - `evidence_dom_id`: stable DOM id, preferably `evidence-{assignment_id}-{question_id}`.
- If no visual source exists, set `evidence_crop_status: not_applicable` and leave the image path empty.
- If conservative per-question cropping genuinely fails, set `evidence_crop_status: exception`, explain the reason in `evidence_exception`, and use the largest safe contextual image available. This is not a normal fallback.
- The renderer embeds the image into the HTML and removes `evidence_image_path` from the hidden downstream payload. The payload keeps `evidence_dom_id`, so downstream daily-report workflows can retrieve the image from the corresponding `<img>` element without duplicating base64.
- Use `pattern_summary` only for repeated patterns supported by at least two wrong items. Do not convert a single wrong item into a stable student diagnosis.


## Output package contract v1.5

For every grading run, write:

```text
<assignment-output>/
├── grading-data.json
├── grading-report.html
└── crops/
    ├── <assignment>-q03.png
    └── ...
```

- `grading-data.json` is the authoritative downstream interface for L2/L3 daily reports.
- Keep `evidence_image_path` / `evidence_image_paths` as relative filesystem paths to `crops/`; never put base64 in JSON.
- `grading-report.html` remains the human-facing self-contained report and may embed crop bytes as base64.
- Downstream daily workflows must not parse this heavy HTML when `grading-data.json` exists.
- Reuse the same crop image files downstream; do not create second copies merely for the daily report.
