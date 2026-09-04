# Shared report-generation rules

## Interaction states
Classify the provided information internally:
- GREEN: critical information complete -> generate now.
- AMBER: only non-critical information missing -> generate without inventing; use “未提供/暂无记录/今日无” only where needed.
- RED: critical information missing -> do not generate yet; ask one targeted follow-up containing only blocking gaps.

Never ask one question at a time. Ask for all missing critical inputs in one message. After the follow-up, generate with what is available and explicitly mark any still-missing nonfabricable item.

## Input style
Accept natural language, screenshots, photos, HTML dashboards and mixed input. Do not force the supervisor to fill a rigid form. The checklist tells them what information is needed; the model does the structuring.

## Calculations
- Calculate percentages from supplied counts; never ask the supervisor to calculate them.
- Only calculate accuracy for objectively scorable tasks with a defensible denominator.
- Keep normal wrong questions and dictation errors as separate counts.
- Do not treat arrival-to-departure duration as effective study time unless breaks are known or the user explicitly says it equals effective study time.
- Do not create an overall task completion rate when long-cycle tasks are present.
- Every task row must show a deadline. Clear same-day homework may use the report date; long-cycle/staged tasks use the confirmed DDL and may carry that DDL forward while unfinished. Unknown long-cycle DDL must be shown as “未明确”, never guessed.

## Evidence
- Preserve user-provided original wrong-question and dictation images. Do not redraw or replace them with OCR text.
- OCR can assist extraction, labeling and indexing, but the displayed evidence should remain the original image.
- When evidence is insufficient, say “暂无法判断/需继续观察” rather than inventing a cause.
- Never reuse mock values from the bundled template.
- If a standardized homework-grading package exists, read `grading-data.json` and reuse the referenced crop file directly; do not crop the same question again. Do not parse the heavy grading HTML when JSON is available.
- When an uncovered confirmed wrong question comes from a larger page, per-question cropping is mandatory; follow `references/cropping.md`.

## Output
- Create one self-contained parent-facing HTML file, but build it via `daily-data.json` + `scripts/render_daily.py` so base64 image bytes never enter model reasoning.
- Start from `assets/template-reference.html` as the locked base template.
- Preserve the approved structure, CSS language, visual shell and section order unless the user explicitly asks to redesign the template.
- Replace all mock/sample content with current student data.
- Expand repeated rows/cards as needed, but do not invent a new page style.
- Wrong-question evidence cards use the locked two-column desktop grid: two cards per row; a single remaining card stays in the left column. On narrow/mobile view, the template collapses to one column.
- If the style drifts, regenerate from the bundled template instead of improvising a new layout.
- Keep the output readable on desktop and mobile.
- Return the generated HTML as the primary deliverable.

## Fixed institutional visual design
- The bundled HTML template is the production design, not a loose reference.
- ALWAYS clone `assets/template-reference.html` first with `python scripts/clone_template.py assets/template-reference.html <output.html>`.
- Do not create HTML from a blank file and do not redesign cards, colors, spacing, fonts, header, navigation, section order or responsive behavior.
- Preserve the template `<style>` and `<script>` blocks byte-for-byte.
- Read `references/visual-contract.md` before editing the cloned file.
- Before delivery, run `python scripts/validate_visual.py assets/template-reference.html <output.html>` and fix any failure.

## Wrong-question image safety
- First preference: reuse embedded per-question crops from a complete standardized homework-grading report. Do not re-crop covered homework.
- For uncovered materials, if a full worksheet/page contains a confirmed wrong question, create a separate per-question evidence crop before HTML generation. This remains mandatory, not optional.
- Prefer extra context over truncation. A slightly loose crop is acceptable; a crop that cuts off the target question is not.
- Whole-page embedding is exception-only after conservative crop failure; it must not be the normal substitute for a per-question crop.
- Never use fixed-height CSS, `max-height`, `object-fit:cover`, or overflow clipping for evidence images.


## Enforcement helpers
- Use `scripts/clone_template.py` to start from the institutional HTML template instead of rebuilding the page manually.
- Preserve the template’s `<style>` block, `<script>` block and section-id order.
- Run `scripts/validate_visual.py` before final delivery. If the validator fails, correct the HTML until it passes.
- For every confirmed wrong question sourced from a full page, use `scripts/safe_crop.py` (or an equivalent conservative crop operation when the runtime cannot execute the script) and produce a per-question crop. Do not skip cropping merely because the whole page is readable.

## Runtime performance contract v1.5
- Reason over compact JSON/text metadata, not base64 image strings.
- Do not open the human-facing grading HTML merely to obtain fields already present in `grading-data.json`.
- Do not manually edit the final HTML. Produce `daily-data.json` and let the renderer build it.
- The renderer, not the model, reads crop image bytes and performs base64 embedding.
