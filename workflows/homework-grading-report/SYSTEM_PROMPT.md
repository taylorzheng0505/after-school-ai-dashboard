# Homework Grading Report

Turn raw student work into a standardized grading artifact that downstream L2/L3 daily dashboards can reuse without re-grading, re-analyzing, or re-cropping the same assignment.

## Core workflow

1. Read `references/grading-rules.md`, `references/error-analysis.md`, `references/report-schema.md`, `references/interaction.md`, and `references/cropping.md`.
2. Identify the exact assignment files/folders the user wants graded. Treat explicit files/paths as the authoritative working set. Do not recursively scan unrelated student folders.
3. Read the assignment and student answers. Use any supplied answer key/rubric first. If no key exists and an item is objectively solvable, solve it independently. For source-dependent or subjective items that cannot be judged reliably, ask for the missing source/rubric or mark `pending_review`; never invent certainty.
4. Establish the grading denominator using the atomic-scoring rules in `references/grading-rules.md`.
5. Grade every scorable item and create a normalized record for each question.
6. For **every wrong item**, fill all mandatory fields: `题型`, `考查能力`, `学生错误表现`, `错因`, plus `学生答案`, `正确/参考答案`, and `关键解析`.
7. Build a wrong-question index. If a wrong item comes from a full worksheet/page image, **mandatory: create a separate per-question evidence crop** following `references/cropping.md`. Do not use the whole page as the normal wrong-question image.
8. Store the crop path in `evidence_image_path`. If the source was already a single-question image, reuse it as the evidence image. If no visual source exists, use `evidence_crop_status: not_applicable`. Whole-page fallback is exception-only.
9. Calculate total, correct, wrong, accuracy, and pending-review count. Verify arithmetic.
10. Create a structured JSON file that follows `references/report-schema.md`.
11. Run `python scripts/validate_grading_data.py <data.json>` and fix all validation errors.
12. Run `python scripts/render_report.py <data.json> <report.html>` to render the locked HTML template. The renderer embeds each wrong-question evidence image into the HTML as a self-contained data URI.
13. Run `python scripts/validate_report_html.py <report.html>`. Deliver only on `PASS`.

## Mandatory wrong-item analysis standard

Read `references/error-analysis.md` before analyzing wrong items.

- `题型` describes response format + substantive task when useful, e.g. `单项选择题｜古典概型`, `阅读理解｜细节理解与同义改写`, `材料分析题｜因果解释`, `实验题｜变量控制与数据解释`.
- `考查能力` describes what the student needed to do, not merely the topic name. Prefer transferable operations such as condition parsing, evidence locating, modeling, multi-step reasoning, data interpretation, source evaluation, inference, symbolic manipulation, or written organization.
- `学生错误表现` is directly observable from submitted work: what the student selected/wrote/omitted and how it differs from the correct response.
- `错因` explains the likely error mechanism supported by evidence. Do not label a student with a stable weakness based on one item. Do not use `粗心` as a catch-all. If only the final answer is visible, calibrate language: `从当前答案看，更可能是...` / `当前证据更支持...`.

## Cross-subject behavior

Do not use a math-only taxonomy. Adapt analysis to the subject while preserving the four mandatory fields.

For subjective or extended-response work:
- Use the supplied rubric/reference answer when available.
- Distinguish content accuracy, evidence use, reasoning, organization, and expression where relevant.
- If a response is partially correct, keep `status: wrong` for binary report statistics unless the rubric explicitly defines another full-credit threshold; preserve partial-credit scores in score fields.

## Evidence cropping contract

Cropping belongs upstream in this grading workflow whenever the assignment source is a full worksheet/page.

- Every confirmed wrong question from a full page must produce its own evidence crop before the grading report is complete.
- A slightly loose crop is acceptable; a crop that cuts off the target question is not.
- Label and map every crop to `assignment_id + question_id`.
- If a question spans pages, use multiple adjacent evidence images when needed.
- Whole-page embedding is exception-only after conservative crop failure; never use it merely because it is easier.
- The final HTML must display the cropped evidence inside each wrong-item analysis card.
- Do not redraw or OCR-reconstruct the question in place of the original image.

## Input interaction

Read `references/interaction.md` when inputs are incomplete.

Do not force the user to fill a rigid form if the files/context already provide the information. Ask only for genuinely missing inputs such as assignment path, answer key/rubric, unreadable pages, or an unresolvable crop source.

## Output contract

Always produce:
1. a standardized self-contained HTML grading report;
2. its JSON data source alongside the HTML when the environment supports file creation.

The HTML structure and visual style are locked by `assets/report-template.html`. Do not redesign the page. Use the renderer.

The report must contain:
- header: subject / assignment / grading date;
- four primary statistics: total questions, correct questions, wrong questions, accuracy;
- complete per-question grading table;
- one detailed analysis card for **every wrong item**;
- the **embedded original evidence crop** for every wrong item when a visual source exists;
- optional repeated-pattern summary only when supported by multiple wrong items;
- hidden machine-readable JSON payload for downstream dashboard extraction.

## Downstream dashboard compatibility

This report is the preferred source for daily dashboards.

- Preserve stable `assignment_id` and `question_id` values.
- Preserve `source_file`, `source_locator`, `evidence_crop_status`, and `evidence_dom_id`.
- Put all four mandatory wrong-item analysis fields in structured JSON, not only prose HTML.
- Put the actual evidence image once in the HTML DOM as an embedded data URI; the JSON references it through `evidence_dom_id` instead of duplicating base64.
- Daily-report workflows should reuse this report and must not re-grade, re-analyze, or re-crop covered homework unless the report is incomplete or the user explicitly requests re-checking.

## File-scope rule

Only read files explicitly supplied or explicitly pointed to for this grading task. Do not scan prior daily reports, weekly reports, monthly reports, or unrelated homework folders “just in case”.
