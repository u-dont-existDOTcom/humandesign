# SCIENTIFIC RANKING CORRECTION — EXTRA-HIGH REASONING OUTPUT — DRAFT BRANCH ONLY — NOT MERGE/DEPLOY AUTHORIZATION

The cross-class audit showed that `core_fit` could split states that were identical on dependency-controlled net rubric bits, meaningful contradictions, and detailed support. The downstream audit compared two alternatives for correcting that behavior.

The chosen production semantics are `rank_order_without_core_fit`:

1. higher `net_rubric_bits`;
2. fewer `meaningful_contradictions`;
3. higher `detailed_support`.

When those three fields tie, the states receive equal scientific rank. Longer duration and then earlier start time provide deterministic intra-tie order only. They do not split scientific rank.

`core_fit` remains calculated and reportable as a descriptive field. It is excluded from both state ordering and scientific-rank equality. Date-score and date-rank algorithms remain unchanged, while date-level `best_state` selection no longer uses `core_fit`.

This correction introduces no replacement ranking metric and makes no new allocation. The frozen mappings, questionnaire prompts, evidence semantics, dependency collapse, and `core_fit` calculation remain unchanged. The two pre-patch audit JSON artifacts, their receipts, and their earlier disposition remain preserved as historical evidence and must not be regenerated against the changed production semantics.

Prediction freezes remain bound to an exact code commit, so a session frozen on older code cannot continue under the corrected implementation. This record authorizes a correction on the draft branch only. It does not authorize merge or deployment.
