# Life Patterns — external questionnaire incorporation

**2026-10-21. Research candidate and private respondent-source integration.**

For the outcome, open **RESULT.md**. For actual changes to our interview method, read **INTERVIEWER-V3-DESIGN-DELTA.md**. For the full working **research-only questionnaire** load **LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json**; it contains all earlier 23 optional topics plus seven conditional follow-ups and strict skip/unknown safeguards.

The external 31-question form's **design**, including which features to adopt versus reject, is reviewed exhaustively in **EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json** and authored in ITEM-DISPOSITION-SOURCE.psv. User-entered checkboxes and personal comments are **intentionally not in the repository**.

The user-**private** merged personal source, exact external extraction and readable response list are saved on their computer in Downloads / Life-Patterns-External-C-Import-20261021. The old survey sources and eight recent experience answers were preserved unchanged. A separate participant's apparently related 96-turn interview was excluded by source identity.

Regeneration:

- Run build_adaptive_survey_v3.py in the humandesign repository root; the builder requires no private questionnaire.
- Run tests/unit/test_life_patterns_external_survey_merge_20261021.py. Negative cases reject changed source hashes, coerced missing state, future-marked answers, dropped or duplicated questions, and overwriting the prior private master.
- merge_owner_personal_results.py and render_private_personal_import.py operate on explicit private files only. They refuse to overwrite their destination.

**No live GPT/Railway or frozen astrology scorer was changed.** The v3 additive instrument is a testable research candidate, not an automatic release of someone else's externally authored yes/no rules.
