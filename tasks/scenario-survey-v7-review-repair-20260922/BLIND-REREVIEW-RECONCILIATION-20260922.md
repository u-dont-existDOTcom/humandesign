# Blind rereview reconciliation — 2026-09-22

Reviewed candidate: `4d4eddc4975bf2a4a146648ae547beb6986741b9`

Blind rereview verdict: `NOT_READY_FOR_FRESH_PILOT`; `semantic_change_required=true`.

## Confirmed blockers and repairs

1. **F0 did not elicit audience adaptation.** One audience cannot support a comparison construct. F0 now holds the same noisy-place preference/stakes constant and asks one matched comparison between close friends and new coworkers. Evidence credit is limited to the respondent's stated difference or lack of difference in framing.

2. **M11 allowed stimulus echo to masquerade as leverage.** The scene no longer supplies a fairness rationale. It now gives a concrete listener objection (“paying for all the ingredients feels like too much”) and credits only the respondent's answer-originated response: clarification, reframing, renegotiation, changed split, withdrawal, etc. The protocol now explicitly forbids crediting stimulus-supplied rationale/value/leverage as respondent evidence.

3. **G15/R07/R08 were not true matched work variants.** G15 now establishes a six-hour mentally demanding computer-work baseline with fixed ordinary conditions. R07 and R08 explicitly keep the same work modality and ordinary conditions while changing workload duration/intensity only. The protocol now requires material non-target determinants to remain fixed in matched variants.

4. **G17 lacked the threshold-determining consequence.** G17 is now a matched high-/low-consequence correction comparison under similar confidence: wrong start time affecting arrivals versus a harmless dessert-detail error. CORRECTION-REASON only clarifies the respondent's own rule if the comparative answer does not already explain it.

## Adopted nonblocking cleanup

- M07 now directly contrasts what came easily with what required learning/practice.
- G25 now supplies a concrete repeated failure explanation (forgot and did not message) rather than leaving cause latent.
- CARE-RESPONSIBILITY, CARE-LIMIT, and ROMANCE-FADE now carry explicit `context_requirement` fields.

## Deferred nonblocking observations

- PREFER-INFLUENCE still requires context-matched interpretation when used for D05 versus X08; current context binding and evidence limits remain the governing boundary.
- G10, PHYSICAL-CLOSENESS, and ROUTINE-CHANGE remain intentionally narrower than their broad source-facet labels; evidence-guide readings constrain credit to the literal answer.

## Verification

The repaired candidate passes 459 / 459 deterministic checks, including direct assertions for all four blockers and the adopted cleanup.

## Next gate

Run another fresh mechanically blinded semantic review on the exact repaired bytes. The rereviewer must not receive this reconciliation, prior findings, rationale, audits, or private participant material before freezing findings.
