# Scenario-first survey v7 redesign audit — 2026-09-22

## Result

**HISTORICAL SAME-CONTEXT PASS ONLY.** This audit did not establish fresh-pilot readiness. A later mechanically blinded Stage-1 review of commit `57cc884f11a6b8203b8860c77e84f01de250a193` found two semantic blockers, both now repaired on the review-repair branch and awaiting blind rereview.

This is a same-context design audit, not independent human validation or AstroHD validity evidence.

## Mechanical checks

- 459 / 459 deterministic bank/protocol/evidence-route checks now pass after two rounds of blind-review semantic repairs; direct regression assertions cover every confirmed blocker.
- 78 canonical question nodes; IDs unique; family membership is one-to-one.
- All context-source references resolve.
- All planning-target identifiers resolve to the source-requirements contract.
- Only the three intentional routing/context nodes (`A0`, `E0`, `WHY`) remain without direct planning targets.
- Retired filler node `C0` is absent.
- Known failed v6 phrases/scenes are absent.
- Each canonical prompt has at most one actual response-task question mark.
- All canonical admissions point to `INTERVIEW-PROTOCOL-v6.md`.

## Evidence-route integrity

- 73 / 73 source-requirement facets are represented in `EVIDENCE-GUIDE-v7.json`.
- Evidence-guide facet IDs exactly match the 73 required facets.
- Zero evidence-guide routes point to missing/retired question IDs.
- `C0` is not referenced by any evidence route.

## Live-failure regression cases

The following previously observed failures are now blocked or repaired:

1. Hidden rationale in an exchange scene → rationale supplied in `M11`.
2. Undefined “poor progress” → concrete persistent organizational blockage in `R10`.
3. Undefined “intense/heavy” work → concrete workloads in `R07`/`R08`.
4. Fully working method used as a novelty discriminator → replaced by recurring friction in `WORKING-METHOD`.
5. Generic repetition as a global trait → exact-activity repetition only in `D0`/`PRACTICE-REASON`.
6. Direct ticket price/hazard used as a familiarity-transfer cue → `M05`/`M06` now require a familiarity-dependent deviation.
7. Abstract unspecified incumbent value → concrete old/new trade-off in `M09`.
8. Status question rendered tautological by “same practical benefit” → direct intrinsic-admiration question in `STATUS`.
9. Positive/negative romance mirror → `ROMANCE-FADE` admitted only for genuinely additional weakening pathways.
10. Whole-scene replay after a partial answer → protocol requires acknowledgement plus only the missing piece.
11. “It depends” treated as failure → protocol requires retaining named conditions as scoped evidence.
12. Coverage-driven continuation → protocol and checkpoint require stopping when no useful admissible distinction remains.

## Semantic sweep notes

A heuristic sweep flagged a small number of intentionally referential prompts (`that reaction`, `that ability`, etc.). These are acceptable only under the bank’s context-binding rule and v6 protocol: the interviewer must render the antecedent explicitly when the reference is not immediately adjacent. They are not blockers in the text-only bank because their admissions require the matching antecedent.

Broad words such as “manageable” or “reasonably well” remain only where the respondent is being invited to choose an ordinary personal baseline, not where an unspecified degree is the determinant being measured. The high-load work variants were concretized because intensity itself determines their answer.

## Exploratory separation

`EX-SENSORY-CONFLICT-01` is present outside the canonical families with `mapping_status=unmapped_neutral_candidate` and `automatic_evidence_credit=false`. It cannot fill a canonical AstroHD facet under this candidate.

## Remaining assurance debt

- Two mechanically blinded fresh-context reviews have run. Each returned `NOT_READY_FOR_FRESH_PILOT` on the then-current candidate; all confirmed blockers from both rounds are repaired, and the newest repaired bytes still require another blind rereview.
- No new multi-respondent human pilot has been run on v7.
- No app/runtime interviewer implements v7 yet.
- No psychometric reliability, validity, completion-time, or target-theory recovery claim is made.

## Recommended next step

Run a new mechanically blinded Stage-1 semantic review on the repaired candidate bytes. Advance to a fresh respondent pilot only if that rereview is ready. Do not resume the completed owner pilot merely to test unanswered fields; that would confound redesign validation with repeated exposure.
