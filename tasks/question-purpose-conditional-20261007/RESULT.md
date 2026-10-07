# Conditional question-purpose correction — result

Direct questions are now asked alone. `What this tests:` is shown only when a scenario, example, or follow-up would otherwise leave the tested distinction unclear.

The owner regression is the recognition question: it must appear without a purpose line because the question already states what it is testing.

Preserved: Railway `participant_purpose` metadata, exact `question_text`, blinding, and the existing backend/Action schema. No backend redeploy is required.

Verification: 14 focused Custom GPT tests passed; instruction strict count is 7,991 (under 8,000); corrected same-GPT update packet built successfully.
