# Life Patterns v8 + v8.1 paired-transfer intake

Audit date: 2026-09-06. This is an intake date, not an inferred interview date.
Status: read-only development intake; participant clarification pass closed for this intake.

## Disposition

Keep the original v8 record and v8.1 supplement separately, unchanged. The supplied review response approves three account changes. No additional autobiographical questions are requested for this bounded repair. Remaining weak support or source limitations stay visible rather than triggering another questionnaire.

This intake is not an immutable behavioral-profile freeze, a validated V2 annotation task set, a calibration result, or permission to execute target-model scoring. It does not silently import or relabel the material.

## Sources actually inspected

- The two participant-supplied JSON files, read locally.
- The supplied repair conversation excerpt, including the displayed proposed changes and approval.
- PR #24 at `6ee69947e6061dd94823806a2a63c1e4828e48b6`, open/draft/unmerged when read.
- `state/LIFE-PATTERNS-v8.1-TARGETED-REPAIR-AND-QUESTIONING-ADDENDUM-2026-09-06.txt` at that commit.
- `docs/research/LIFE_PATTERNS_AUTOMATED_CODING_EXECUTION_SPEC.md` at that commit.

No outside behavioral theory was used to recode participant material. No production/Railway audit or full application test suite was run for this intake. The PR description is not evidence of current production behavior.

## File identity

| Source | Bytes | SHA-256 of uploaded bytes |
|---|---:|---|
| `life_patterns_v8_transfer_record.json` | 54,488 | `3c37c0c76174c7ba698966155f991f0303cd4f0833d39ff475dfb0e1c5348637` |
| `life_patterns_v8_1_repair_supplement.json` | 25,844 | `93f838bb61e6a910ba0dbeb96a66b56c72986350dda5386243b098a738b818e7` |

The pairing manifest binds the files supplied together in this conversation. The supplement itself did not carry the original file's hash. Creating the manifest now does not prove historical cryptographic linkage or authenticate the original platform transcript.

## Structural checks

Both files parse as UTF-8 JSON with duplicate object keys and non-finite constants rejected. The checked ID collections are unique; checked episode, series, pattern, source, question-response, metadata, review, and approval references resolve. Original schema/status metadata matches. The review response text agrees with its referenced response. Four clarification questions were logged, including one rephrasing: within the existing four-question cap.

Original inventory: 14 pattern claims, 12 series reports, 16 episodes, 55 participant-turn index entries. Supplement inventory: 4 question entries, 5 response entries (including approval), 17 recovered-text entries, 3 approved account changes, 3 added-evidence records, 6 listed outstanding issues.

These are structural checks only, not a complete schema conformance or semantic/provenance authenticity certification.

## Evidence types are not interchangeable

| Target | Type as supplied | Intake treatment |
|---|---|---|
| PAT-006 | Repeated-series report | Preserve occasional/limited adolescent wording; no new distinct event, count, precise age, or childhood generalization is invented. |
| PAT-012 | Current behavioral example | Preserve as an example, not a newly dated bounded episode or quantified series. It does not establish that the stated consideration was the sole cause of the action. |
| PAT-014 | Concrete episode | Preserve the post-review episode and approved approximate-age interpretation; it anchors one conditional branch on one occasion, not a universal rule or an onset date. |

The supplement's three additions are not three new episodes. Source recovery is not new autobiographical evidence. Latest approval confirms representation of the three proposed changes; it does not independently verify history or approve every pre-existing metadata field.

## Outstanding support labels

| Pattern | Original stored label | Linked episodes / series | Disposition |
|---|---|---|---|
| PAT-001 | anchored_series | 0 / 2 | Preserve and flag; series evidence remains available. |
| PAT-007 | anchored_series | 0 / 1 | Preserve and flag; do not demand an incident just to repair a label. |
| PAT-010 | multiple_episodes | 1 / 1 | Preserve and flag; a possible alternative label would still require comparability review. |

No new official support-state vocabulary is introduced. Count compliance is necessary but not sufficient for evidence strength. Support must remain branch-specific and period-specific. The presence of one example for each side of a conditional claim does not establish repeated observations of either side.

## Source limits and separate reviewer observations

The supplement labels recovered strings as exact. Most cannot be independently checked against the complete original interview because that transcript is not supplied here. The known repair text and approval can be compared with the current excerpt; this does not authenticate every recovered original message.

Original and recovered approval coverage descriptions are not fully equivalent. In particular, the original turn index gives broader batch scope to one approval than the recovered review description does. Retain both as supplied; the latest explicit approval of the three changed accounts does not retroactively establish every original approval boundary.

The original transfer sometimes mixes actual actions, hypothesized alternatives, and summary interpretations. Do not pass unverified summary-only alternatives to a coder as established opportunity/feasibility evidence. Absence of an apology alone does not establish absence of every possible repair behavior. Outward action and a reported emotional response can coexist; exception links need proposition-level checking rather than automatic acceptance. These are reviewer cautions, not changes to the approved account.

The repair's adolescent follow-up restates a candidate prioritization pattern. Preserve it as prompted, qualified self-report rather than independent spontaneous corroboration. The supplement retains two weaker claims rather than automatically filling their gaps. No extra participant questions are requested solely to remove these limitations.

## Reuse and engineering choice

Reuse the existing v8/v8.1 separation and support-label rules. Adapt ordinary standard-library JSON/reference checks and SHA-256 file identity to the intake; do not invent a measurement metric or new codebook. This is a narrow file-audit utility, not a new research workflow.

Reproducible utility and synthetic tests:

- `scripts/life_patterns_intake/audit_v8_pair.py`
- `scripts/life_patterns_intake/test_audit_v8_pair.py`

Run from the repository root with private input paths and a NEW report path:

```bash
python scripts/life_patterns_intake/audit_v8_pair.py \
  /private/life_patterns_v8_transfer_record.json \
  /private/life_patterns_v8_1_repair_supplement.json \
  --output /private/structural_audit.json
python -m unittest discover -s scripts/life_patterns_intake -p 'test_*.py' -v
```

Executed locally: structural pair audit PASS; 11 synthetic unit tests PASS. Input mutation, missing references, incorrect review links/text, duplicate IDs/JSON keys, non-finite input, unsupported linkage metadata, question-budget violations, and preservation of flagged support labels are exercised within those tests. This is not a claim that the repository-wide CI or scientific validation passed.

## Next boundary

Collection for this repair is complete. The next engineering step is a source-checked private adapter/task preparation using the existing coding execution specification, with original and post-review evidence distinguishable. Only evidence actually available may be used; no reconstructed quotations, invented approvals, silent event splitting, or task-schema bypasses are permitted. Formal coder/model/prompt/batch/calibration identities must be frozen before actual independent coding runs. None was executed by this intake.

The owner archive is not a blinded coder packet: it contains upstream pattern interpretations and a method audit. Do not upload it wholesale into an independent coding pass.

## Privacy and authority

Only this source-free technical audit and generic audit/test code are committed to the repository. Participant narratives, exact answers, third-party identities, and source transcripts remain outside the public repository. Downloadable paired files are provided in this conversation, not published as repository research data. The archive is not encrypted. No merge, deployment, external participant/coder contact, scoring, or reveal is performed.
