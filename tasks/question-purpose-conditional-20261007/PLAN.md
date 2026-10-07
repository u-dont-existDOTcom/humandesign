# Conditional question-purpose explanations — 2026-10-07

## Owner correction
The prior rule over-explains direct questions. Purpose text is useful only when a scenario, example, or follow-up does not make clear what person-level tendency/distinction is being tested. A direct question must not be preceded by a near-synonymous `What this tests:` line.

## Required behavior
- Keep Railway `participant_purpose` metadata available as an explanatory aid.
- Ask direct/self-explanatory questions alone.
- Show `What this tests:` only when the question/context would otherwise leave the purpose unclear.
- Never use the purpose line merely to paraphrase the question.
- Preserve exact `question_text`, blinding, and no-scoring/no-chart-target rules.

## Owner regression
This must be asked alone, with no purpose line:

> Apart from its practical benefits, how important is recognition from other people to you?

The redundant line to suppress is: `What this tests: how intrinsically rewarding other people’s recognition is to you when practical benefits are removed.`

## Scope
Custom GPT presentation only. Backend purpose metadata and live Action schema remain valid; no Railway or local-reviewer redeploy is required.
