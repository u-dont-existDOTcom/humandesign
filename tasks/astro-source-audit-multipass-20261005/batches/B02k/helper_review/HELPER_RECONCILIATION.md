# Helper reconciliation — changed items only

**H-A01 and H-A02 are resolved in the reviewed helper.** This is the requested bounded follow-up to source-A's frozen diagnosis, using the same source-first context. It is not a fresh-context independent full-source evaluation.

## H-A01 — aggregate coordinate guard

The helper now checks `0 <= position < 30` after summing complete DMS components and before subtracting the position from 30. The focused regression rejects both:

- `(Fraction(59, 2), 59, 0)`, which reproduced the original negative remainder;
- `(Fraction(59, 2), 30, 0)`, whose sum is exactly the next-sign boundary.

The inspected code still returns unknown when components are missing and leaves the time unit unresolved. This resolves the implementation-domain finding without adding a source timing conversion.

## H-A02 — complete exception and explicit Saturn target

A fresh visual inspection of **original PDF286 / printed252, opening paragraph**, confirms the exception “unlesse the disease be in its decrease and leaving the Patient or Querent.” The same clause specifies conjunction, square or opposition to Saturn and qualifies its assertion with “for the most part.”

The repaired input `disease_decreasing_and_leaving` is explicitly documented as a caller-qualified aggregate for the complete phrase. The docstring says that decreasing alone does not establish it and that an unresolved full phrase must be supplied as `None`. The aspect input now expressly names the Moon-to-Saturn relationship. The frequency qualification and the limit to prerequisite matching are also documented.

The focused regression verifies the aggregate's three states, with the positive prerequisites established: `False → SATISFIED`, `True → CONTRADICTED`, and `None → UNKNOWN`. This resolves the source-qualification finding without imposing a new clinical interpretation of the phrase.

## Verification and preserved history

Two selected producer test methods passed in one bounded process:

1. `RemainingArc.test_individually_valid_fractional_components_must_not_reach_next_sign`
2. `SourcePredicateQualifications.test_already_declining_exception_blocks_adverse_moon_clause`

The runner reported **2 tests, 0 failures, 0 errors**. Python bytecode writes were disabled. No reference tables or rules were loaded and no full-suite result is claimed.

All five original diagnosis, probe, and review-receipt files retain their previously recorded hashes. They are preserved as evidence about the earlier helper version; these repairs do not retroactively invalidate that diagnosis. No repository files were edited.

## Version and evidence anchors

- Earlier helper SHA256: `972076c053dc8ad340d6369ecdbf3893f3b1d1354231a087d0ade88b2a1f180f`
- Reconciled helper SHA256: `25777500a00551208e0fcae59a16af347d9cb513d1602b4f1299c959695244d5`
- Selected producer-test file SHA256: `3d3186e86772b16903f914f168c38c58ca952578aa4458e388cad994115e64db`
- Original PDF286 image SHA256: `00c21d6f5ac982f6bb791756ccf0013423616dde08c9c21735b26aa83153f9d5`

The JSON companion contains the complete selected-test output, original artifact hashes, per-finding dispositions, and scope limits. The bounded reconciliation is complete; root retains integration and publication.

