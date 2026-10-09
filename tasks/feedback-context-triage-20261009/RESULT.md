# Feedback context triage — live outcome

## Parent owner correction
The private researcher dashboard had conflated a model-extracted question about the typicality of the respondent's own conditional answer with criticism of the original A0 survey wording. The original historical source is one combined question-and-answer record and does not preserve intervening assistant prompts; chronology beyond that pair remains unknown.

## Corrected behavior
- An ungrounded reviewer-derived snippet is no longer actionable questionnaire feedback merely because the reviewer called it process feedback. A pure response-normality inquiry is moved to read-only **Other conversational remarks**, not a question-defect task. Ambiguous unsupported model inferences also remain contextual.
- Clear criticisms of re-asking, repeating, ambiguous/missing context, and other question-design referents remain in the actionable improvement queue.
- The main dashboard labels model-derived provenance accurately, displays the associated original question only as source context (not proof of the utterance's immediate antecedent), and offers an expandable full recorded answer. No private raw source or invented conversational reply was added to Git.
- Status choices are internal researcher workflow bookkeeping, not survey answers or automatic question edits. They are explained once on the dashboard and hidden per item under a collapsed optional reviewer-tracking section; the source/answer remains unmodified.
- Feedback ID derivation, existing disposition storage, the independent review/frozen primary, authentication and consent boundaries are unchanged.

## Verification
- Focused regression tests: 11 passed, including source-normality separation, real question-repetition preservation, ambiguous inference, source-context presentation and admin-only access.
- Participant application suite: 225 passed.
- Repository suite: 1,021 passed; 6 pre-existing astronomy-data skips.
- Hosted verification and survey-browser checks: passed; merged implementation commit `bfa623417ebd45c1f1318cf73c8666d1fa690085`.
- Production Railway deployment `d28d1bf9-ddd4-458f-a0fa-6b81eb5c2c18`: SUCCESS. Live health, static JS and authenticated private feedback endpoint: HTTP 200. Frontend includes optional tracking and full answer context.
- Live readback: **8 possible question-design issues** and **2 contextual remarks**. The historical A0 normality remark is retained as context and excluded from the actionable queue; its recorded source answer and inferred-extraction label are present.
- Owner's local private HTML backup refreshed with the 8 actionable items (file mode 0600). The online dashboard retains the two contextual remarks in its separate expandable section.

## Remaining limitation
The original imported conversation does not contain assistant turns between the saved question and its combined answer. We cannot prove the precise conversational moment at which a contextual remark was said. The original unedited answer and independent review remain intact. This repair prevents a downstream false question-defect claim; it does not retroactively change the frozen worker's process-feedback tagging or psychometric interpretation.

The existing separate daily Life Patterns question-repair task was observed disabled on 2026-10-09; this engineering repair has not silently re-enabled it, so workflow statuses should not be represented as automatically advancing.
