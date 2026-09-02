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
- When a confirmed wrong question comes from a larger page, per-question cropping is mandatory; follow `references/cropping.md`.

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

## Wrong-question image safety
- If a full worksheet/page contains a confirmed wrong question, create a separate per-question evidence crop before HTML generation. This is mandatory, not optional.
- Prefer extra context over truncation. A slightly loose crop is acceptable; a crop that cuts off the target question is not.
- Whole-page embedding is exception-only after conservative crop failure; it must not be the normal substitute for a per-question crop.
- Never use fixed-height CSS, `max-height`, `object-fit:cover`, or overflow clipping for evidence images.


## Enforcement helpers
- Use `scripts/clone_template.py` to start from the institutional HTML template instead of rebuilding the page manually.
- Preserve the template’s `<style>` block, `<script>` block and section-id order.
- Run `scripts/validate_visual.py` before final delivery. If the validator fails, correct the HTML until it passes.
- For every confirmed wrong question sourced from a full page, use `scripts/safe_crop.py` (or an equivalent conservative crop operation when the runtime cannot execute the script) and produce a per-question crop. Do not skip cropping merely because the whole page is readable.

## Weekly/monthly evidence rule
Weekly and monthly workflows must reuse wrong-question evidence already recorded in daily reports. They must not rescan raw worksheets, scan the standalone wrong-question library, or recrop original homework/test pages.


## 标准作业批改报告复用
- 当日报输入中已有标准作业批改HTML，日报必须优先读取其中的结构化批改数据与逐题证据裁图。
- 已被标准批改报告覆盖的作业，不得在日报阶段重复批改、重复错题分析或重复裁剪。
- L2只消费客观统计、错题编号/来源、裁图和订正状态；L3可进一步消费题型、考查能力、错误表现与错因。
- 没有标准批改报告的材料继续走日报原有裁图/记录流程。
- 日报错题卡桌面端采用固定两列网格；单个卡片保持左列，不拉伸整行。
