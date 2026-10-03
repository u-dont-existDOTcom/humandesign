# Shadow triage blind adjudication follow-up — 2026-10-03

## Scope

Development-only. No live participant behavior changed. Two Claude models were given only synthetic case descriptions and route meanings, not shadow outputs or private participant source.

## Agreement

Both adjudicators agreed that:
- a concrete semantic answer can make an untagged canonical route redundant;
- PREFER-EXCHANGE can be useful after a valid M11 antecedent;
- PREFER-EXCHANGE is ineligible without its required M11 context;
- later correction source can make a proposed clarification redundant;
- a follow-up containing an invented respondent-specific premise should be rejected;
- an explicitly unanswerable distinction may remain unknown rather than being re-asked semantically.

## Disagreement

Two information-gain cases remained genuinely disputed:
- generic coordination evidence versus the concrete M11 cost-objection scene;
- an answer saying continued negotiation depends on why the friend objects.

These cases must not be tuned to an assistant-authored expected label. The synthetic benchmark treats the first such expectation as disputed rather than a hard pass/fail target.

## Robustness defects found and repaired in shadow

1. Self-contained hypothetical scenes were once rejected because the participant had not previously mentioned the scenario. This is incorrect: frozen self-contained scene premises are authorized stimulus. The admission prompt now distinguishes route-supplied hypothetical premises from unsupported respondent-specific assumptions. A rerun approved the canonical M05 candidate with all gates true.
2. A PREFER-EXCHANGE candidate was accepted alone but once rejected when an unrelated M05 candidate was in the same batch. Candidate-local admission gates are now explicitly counterfactually invariant to unrelated candidates; only independent_for_batch may depend on batch companions. Paired rerun admitted PREFER-EXCHANGE both alone and with M05.
3. An explicit-unknown synthetic case initially triggered another semantically equivalent clarification. Both blind adjudicators preferred review_ready. Triage/admission now say not to re-ask an explicitly unanswerable distinction unless a materially different concrete context makes it newly answerable; rerun returned review_ready.

## Current gate

Latency separation is supported. Promotion remains blocked pending a larger blinded replay set and repeated-run stability around the disputed information-gain cases.
