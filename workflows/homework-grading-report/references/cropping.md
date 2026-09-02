# Wrong-question image cropping protocol

Cropping is a **mandatory production step** for daily reports whenever the source evidence is a full worksheet/page and a wrong question has been identified. The final daily HTML must not use the full worksheet page as the normal substitute for a per-question evidence crop.

The priority is completeness, not tightness. A crop that contains extra whitespace or a small part of the neighboring question is acceptable; a crop that cuts off any part of the target question is not.

## Mandatory per-question workflow
1. Build a wrong-question index from the grading result, supervisor statement, annotations, answer marks, or other reliable evidence.
2. For **every confirmed wrong question**, locate the corresponding source page in today's explicitly identified raw homework/test files.
3. Estimate a generous approximate bounding box around that question. Do not make it tight.
4. Run `scripts/safe_crop.py` with the approximate box.
5. If the result is `PASS`, use the cropped file.
6. If the result is `FALLBACK`, enlarge the region and try to preserve the full question. Prefer a larger contextual crop, or multiple adjacent crops for a cross-page question.
7. Label each evidence unit with subject/source/question number so the crop has an unambiguous mapping.

## Full-page fallback
Whole-page embedding is **not an acceptable normal fallback**. Use the original whole page only when a usable per-question crop cannot be produced after conservative expansion (for example, a genuinely page-spanning question or technical crop failure). If this happens, treat it as an exception rather than silently substituting the full page.

## Conservative crop rules
- Prefer full content width for a question band instead of a tight horizontal crop.
- Keep top/bottom safety margins.
- Expand to the nearest sufficiently blank horizontal band above and below the approximate target.
- If ink still touches the crop's top or bottom edge, expand again.
- If the question spans a page break, use multiple evidence crops when practical.
- Never rely on OCR text reconstruction to replace the original visual evidence.

## HTML rule
Display the resulting crop at natural aspect ratio. Never use fixed-height CSS, `max-height`, `object-fit: cover`, or overflow clipping for evidence images.
