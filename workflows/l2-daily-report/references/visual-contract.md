# Visual contract: fixed institutional design

The bundled HTML asset is not a loose design example. It is the institution's fixed parent-facing template.

## Mandatory rules
- ALWAYS render from `assets/template-reference.html` through `scripts/render_daily.py`. Never write or hand-edit the report HTML from a blank file.
- Preserve the complete `<style>...</style>` block byte-for-byte.
- Preserve the complete `<script>...</script>` block byte-for-byte.
- Preserve the existing header, sticky navigation, section order, card types, spacing system, typography, colors, borders, radii and responsive rules.
- Preserve existing class names. Do not invent a new design system or substitute a different dashboard/card layout.
- The model only writes `daily-data.json`; `scripts/render_daily.py` fills data-bearing slots and embeds images.
- If a section has no current data, keep the institutional structure and use the report-specific missing-data rule; do not redesign the section.
- Do not add decorative gradients, icons, charts, fixed-height image frames, masonry layouts, new card shells, or alternate fonts.

## Wrong-question grid contract
- On desktop, wrong-question evidence cards must use the template's fixed two-column grid: two questions per row.
- If the row has only one question, leave the right grid slot empty; do not stretch the card to full width.
- On mobile/narrow screens, use the template's built-in one-column responsive fallback.
- Do not replace this with masonry, variable-width cards, or one-question-per-full-row desktop layout.

## Image display contract
- Evidence images must render with `width:100%` and automatic height.
- Never use `height:<fixed value>`, `max-height`, `object-fit:cover`, or a clipping wrapper for wrong-question evidence.
- Never crop an image visually through CSS. Crop only by producing a separate validated image file.

## Required pre-delivery validation
After generating the report, run:

`python scripts/validate_visual.py assets/template-reference.html <generated.html>`

Do not deliver the file unless the validator prints `PASS`.
