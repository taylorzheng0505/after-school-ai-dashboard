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

## Evidence
- Preserve user-provided original wrong-question and dictation images. Do not redraw or replace them with OCR text.
- OCR can assist extraction, labeling and indexing, but the displayed evidence should remain the original image.
- When evidence is insufficient, say “暂无法判断/需继续观察” rather than inventing a cause.
- Never reuse mock values from the bundled template.

## Output
- Create one self-contained parent-facing HTML file.
- Start from `assets/template-reference.html` as the locked base template.
- Preserve the approved structure, CSS language, visual shell and section order unless the user explicitly asks to redesign the template.
- Replace all mock/sample content with current student data.
- Expand repeated rows/cards as needed, but do not invent a new page style.
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

## Wrong-question evidence reuse
- Use wrong-question evidence and labels already contained in the daily reports.
- Do not rescan raw worksheets or the standalone wrong-question library.
- Do not re-crop original homework/test pages for weekly or monthly reports.


## Enforcement helpers
- Use `scripts/clone_template.py` to start from the institutional HTML template instead of rebuilding the page manually.
- Preserve the template’s `<style>` block, `<script>` block and section-id order.
- Run `scripts/validate_visual.py` before final delivery. If the validator fails, correct the HTML until it passes.
