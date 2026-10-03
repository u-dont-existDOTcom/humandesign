# Blind triage adjudication expected results v1

Frozen before running the shadow model on these cases.

Evaluator: fresh Claude Sonnet/high CLI context.
Information supplied: only `BLIND-ADJUDICATION-CASES-v1.md`.
Withheld: shadow outputs, legacy outputs, benchmark timing, producer rationale, prompt history, previous adjudication examples.

| Case | Expected decision | Route if asked | Confidence | Adjudication |
|---|---|---|---|---|
| H1 | review_ready | — | medium | Naming urgency is already a decision factor for what to do when plans run long; the route does not require exhaustive factors. |
| H2 | review_ready | — | high | Source names multiple competing-commitment factors and a renegotiation condition. |
| H3 | review_ready | — | high | Source directly gives the meaning assigned to the familiar-route deviation. |
| H4 | clarification_needed | M05 | high | General noticing of change does not answer what the route deviation means. |
| H5 | review_ready | — | high | Source states both preserved value and a concrete switch condition. |
| H6 | clarification_needed | G20 | high | Source says the money is welcome but gives no intended function for it. |
| H7 | review_ready | — | high | Source directly states what first catches attention in the meal setting. |

This expected-results file is immutable validation authority for the first replay of these seven cases. If implementation behavior differs, record the mismatch before any prompt/code change. Any case used to tune the implementation after this point becomes DEVELOPMENT and cannot validate the repair.
