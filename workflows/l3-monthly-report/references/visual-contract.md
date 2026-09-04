# Visual contract v1.6

The institutional template is a clean visual shell, not a demo report.

## Required
- Preserve the bundled `<style>` and `<script>` blocks byte-for-byte.
- Preserve the fixed section order for this report type.
- Do not hand-edit the final HTML. Generate it only through the bundled renderer from validated JSON.
- Repeated rows/cards may expand only through renderer loops.
- Evidence images, when used, must preserve natural aspect ratio; never crop them again with CSS.
- Final HTML may embed image bytes so the family receives a self-contained file. Base64 must be introduced only by the renderer, never stored in weekly/monthly JSON.

## Forbidden
- Reintroducing demo/sample student text into the template.
- Adding alternate styles, new color systems, or custom layout variants.
- `object-fit: cover`, image `max-height`, or overflow-based evidence cropping outside the locked style.
- Direct LLM rewriting of the full HTML.
