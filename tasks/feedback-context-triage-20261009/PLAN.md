# Researcher feedback attribution and triage — 2026-10-09

Owner correction: the dashboard treats an isolated reviewer-extracted a short normality/typicality question (A0) as survey-design feedback, although this was a question about whether their own contextual answer was ordinary; the original source only preserves it appended to an A0 answer, and cannot prove intervening assistant chronology. The dense manual status dropdown is unexplained and contrary to the preferred automated research improvement flow.

Goal: preserve actual answer and historical review; stop treating ambiguous normality remarks as question-design complaints; show full source-answer context and clear reviewer provenance for inferred process feedback; explain researcher statuses and hide advanced manual controls by default; do not auto-edit instruments from unproven process annotations. Preserve genuine criticisms such as redundant questions. User should see meaningful triage, not an uncontextualized quote.

Checks: read-only provenance verification, synthetic fixtures for ambiguity and real design objection patterns, authentication/UI tests, no source mutation, focused regression and live deployment verification only after integration. Save lessons/receipts to humandesign. Respect privacy: never commit participant text or production tokens/IDs.

Active lesson contract:
- Source is verbatim; extracted quote is not its own conversational turn.
- Model-derived feedback requires an explicit question-design target to become actionable. Normality queries about own answer stay contextual, not actionable.
- Statuses are internal triage, not survey responses or automatic question edits.
- Uncertain feedback is retained in read-only source, not rewritten as user intent.
- Repo versioning/blinding preserved; no change to completed interview.
