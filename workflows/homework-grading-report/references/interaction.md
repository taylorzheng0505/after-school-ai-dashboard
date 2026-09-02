# Interaction Protocol

## First response when the user asks for grading

If assignment files/paths are not already available, ask once for:
1. the homework/worksheet images, PDF, or exact local folder/path;
2. the subject and grade level only if they cannot be inferred;
3. the official answer key/rubric if one exists.

Tell the user that an answer key is optional for objectively solvable items, but required when a subjective task cannot be reliably graded without a rubric/source.

Do not ask the user to manually enumerate every question if the assignment files are readable.

## If files are unreadable or incomplete

Ask only for the affected page/question, not the whole assignment again.

## If grading evidence is insufficient

Use `pending_review` for the affected item and state exactly what is missing.

## If the user asks for the final report directly

Grade first, validate the structured data, then render the HTML. Do not expose long internal reasoning. Give the user the HTML file and, when useful, the JSON data file.

## Wrong-question crop inputs

When the assignment is supplied as full-page images/PDF pages, do not ask the user to crop wrong questions manually. After grading identifies the wrong-question index, locate each wrong question on its source page and crop it automatically.

Only ask for help when a wrong question cannot be mapped to a readable source page. Ask for the affected page/path, not the whole assignment again.
