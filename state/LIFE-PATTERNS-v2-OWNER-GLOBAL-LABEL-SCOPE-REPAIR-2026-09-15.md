# Life Patterns v2 — owner global-label scope repair — 2026-09-15

## Owner finding

A broad self-description can be semantically wider than the first subdomain the interview happens to investigate. In the owner test, a general claim of being "balanced" was narrowed into mood/emotional steadiness because that was the evidence collected first. The owner explicitly corrected that the interviewer should ask whether the claimed balance also extends across materially different domains rather than silently equating the broad label with mood.

Illustrative owner direction: when someone says they are balanced in general, ask whether that means mainly emotional steadiness or also appears across domains such as work/life, practical/spiritual priorities, functional/emotional life, relationships, or competing demands. The examples are illustrative, not a fixed literal script.

## Failure mechanism

**Scope collapse from evidence availability.**

The reasoning path was vulnerable to treating the first well-evidenced subdomain as the meaning of a broader participant claim. That creates two symmetric errors:

1. silently narrowing a global claim to one observed domain; or
2. silently generalizing one observed domain back to the global claim.

Both lose participant meaning and reduce discriminating value for later personality / astrology / Human Design analysis.

## Repair

A new target-blind global-label scope guard is active in:

`src/hdmatch/api/life_patterns_v2_owner_scope.py`

The deployment wrapper now serves the recoverability interview through this scope-aware model.

The guard applies to normal planning, refinement, and initial focus triage. When the participant's label is broad but evidence is materially narrower, the interviewer must treat scope as unresolved and decision-changing before surfacing/finalizing a formulation, unless the participant already explicitly settled the scope.

The question should:

- ask only one scope-discriminating question;
- make the contrast concrete with a few non-exhaustive domain examples;
- allow "mostly just this domain", cross-domain, context-dependent, or uncertain answers;
- avoid assuming that every listed domain is balanced;
- avoid turning the examples into another checklist;
- prioritize scope over another observer-view question when the participant has just said the synthesis is too narrow;
- not re-ask once scope is settled.

This is a semantic-scope repair, not a return to fixed episode quotas or exhaustive interrogation.

## Mission Control capture

The owner also explicitly requested that the accumulated logic corrections be preserved for Mission Control, including exact corrections when safely publishable. A privacy-bounded exact-text record was created on the isolated universal-architecture branch:

`feedback/mission-control-logic-corrections-20260915`

Artifact:

`feedback/mission-control/SDF-20260915-LIFE-PATTERNS-OWNER-LOGIC-CORRECTIONS-001.json`

Its truth state is `CAPTURED_BRANCH_ONLY` until accepted into the canonical universal architecture branch.

## Verification boundary

Focused regression coverage is in:

`tests/unit/test_life_patterns_v2_owner_scope.py`

The decisive product check remains owner consumer-seam behavior: a broad label such as "balanced in general" followed by evidence limited to mood should trigger a cross-domain scope question before the system settles on a mood-only or person-wide synthesis.
