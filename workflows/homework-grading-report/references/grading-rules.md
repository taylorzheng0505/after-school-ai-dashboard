# Grading Rules

## 1. Unit of counting

Use one **independently scorable response unit** as one item.

- A numbered question with one answer = 1 item.
- Explicit subparts such as 3(a), 3(b), 3(c) = 3 items when each can be judged independently.
- Multiple blanks count separately only when the worksheet/rubric treats them as separate scored parts or they are independently labeled. Otherwise keep them under one question and record partial correctness in notes.
- A multi-select question is one item unless the rubric explicitly scores options independently.
- A long-response problem is one item unless the rubric separates scored subparts.

Never inflate the denominator simply because a question contains multiple reasoning steps.

## 2. Status

Use:
- `correct`: fully correct according to answer key/rubric.
- `wrong`: not fully correct. This includes partial-credit responses when binary correct/wrong reporting is required.
- `pending_review`: cannot be judged reliably from available evidence.

Do not force uncertain work into correct/wrong.

## 3. Statistics

- `total_questions` = all identified scorable items, including pending-review items.
- `correct_questions` = count of `correct`.
- `wrong_questions` = count of `wrong`.
- `pending_review` = count of `pending_review`.
- `accuracy` = correct / (correct + wrong) × 100 when at least one item is evaluable.
- Do not include pending-review items in the accuracy denominator.
- Round display accuracy to one decimal place unless the result is an exact integer and the template chooses to omit `.0`.

Always verify:
`total_questions = correct_questions + wrong_questions + pending_review`.

## 4. Answer source priority

1. User-provided official answer key or rubric.
2. Answer/reference material in the explicitly supplied working set.
3. Independent solving by the model when the item is objective and sufficiently visible.
4. `pending_review` if the answer cannot be established reliably.

Do not search unrelated files for answers.

## 5. Subjective work

When grading essays, short answers, history/science explanations, language writing, or other subjective responses:
- Prefer a rubric.
- If a reference answer exists, do not treat wording differences as wrong when the meaning satisfies the rubric.
- Explain why the response fails the criterion rather than only stating the preferred answer.
- Preserve rubric/score details when available.

## 6. Evidence and uncertainty

A wrong-cause analysis may be:
- `high` evidence: work/steps directly reveal the mechanism.
- `medium` evidence: answer pattern strongly supports a mechanism but steps are incomplete.
- `low` evidence: only the final answer is visible and several mechanisms remain plausible.

Low-evidence items still need an `error_cause`, but the wording must be calibrated and non-diagnostic.
