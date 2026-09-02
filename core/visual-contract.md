# Visual contract: fixed institutional design

The bundled HTML asset is not a loose design example. It is the institution's fixed parent-facing template.

## Mandatory rules
- ALWAYS start from `assets/template-reference.html`. Never write the report HTML from a blank file.
- Preserve the complete `<style>...</style>` block byte-for-byte.
- Preserve the complete `<script>...</script>` block byte-for-byte.
- Preserve the existing header, sticky navigation, section order, card types, spacing system, typography, colors, borders, radii and responsive rules.
- Preserve existing class names. Do not invent a new design system or substitute a different dashboard/card layout.
- Only replace data-bearing text, table rows, status tags, evidence images and other content slots required by current student data.
- If a section has no current data, keep the institutional structure and use the report-specific missing-data rule; do not redesign the section.
- Do not add decorative gradients, icons, charts, fixed-height image frames, masonry layouts, new card shells, or alternate fonts.

## Image display contract
- Evidence images must render with `width:100%` and automatic height.
- Never use `height:<fixed value>`, `max-height`, `object-fit:cover`, or a clipping wrapper for wrong-question evidence.
- Never crop an image visually through CSS. Crop only by producing a separate validated image file.

## Required pre-delivery validation
After generating the report, run:

`python scripts/validate_visual.py assets/template-reference.html <generated.html>`

Do not deliver the file unless the validator prints `PASS`.
