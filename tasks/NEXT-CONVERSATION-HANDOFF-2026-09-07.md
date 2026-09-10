# Life Patterns — next-conversation handoff

Repository: `u-dont-existDOTcom/humandesign`

Branch: `codex/discover-life-patterns-mvp`

Draft PR: `#24`

Before substantive work, fetch the **current PR #24 head** and treat GitHub as canonical. Then read, in this order:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-FAILED-RUN-2026-09-10.md`
3. `tasks/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-WORKER-2026-09-10.md`
4. `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-PROMPT-v1-2026-09-10.txt`
5. `state/LIFE-PATTERNS-R05-FACET-OVERLAP-AND-ABSENCE-SEMANTICS-DEFECT-2026-09-10.md`
6. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-10.md`
7. `state/LIFE-PATTERNS-HUMAN-UI-DIRECT-CHOICE-CORRECTION-2026-09-09.md`
8. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
9. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
10. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
11. `state/LIFE-PATTERNS-DEVELOPMENT-CODING-MANUAL-v2-2026-09-08.md`
12. `state/LIFE-PATTERNS-PRIVATE-ARTIFACT-RECOVERY-VERIFIED-2026-09-07.json`
13. `state/CURRENT-STATE.md`
14. `state/LIFE-PATTERNS-DEVELOPMENT-HANDOFF-2026-09-06.md`

## Current controlling state

The exact private source recovery, recurrence-v2 correction, private v2 freeze, and owner-led human-interface simplification are complete through the direct-choice UI. Human calibration is nevertheless **blocked before collection** by the new theory-neutral subcode-overlap / absence-semantics audit.

No qualifying independent human first pass has been collected. No automated Life Patterns coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## The first overlap/absence audit attempt is invalid

The owner returned the first attempted fresh blind worker output on 2026-09-10. Treat it as a failed execution/transport artifact, not as substantive audit evidence.

Public-safe identity of the returned text:

- bytes: `17554`
- SHA-256: `0e3b339c9e7ffa6362ada0a13ec2b2d11911608e7b5cdca4c39216a79f5a5b81`

Why it is invalid:

- Markdown escaping inserted illegal JSON `\_` escapes throughout the returned lines;
- after diagnostic removal of those presentation escapes, only `OA-001` through `OA-009` form a parseable prefix;
- attempted `OA-010` is syntactically corrupted;
- the remainder is process/meta commentary about response construction/truncation rather than audit findings;
- no complete 22-observable result and no valid final summary JSON exist.

**Do not salvage or use the first nine partial findings.** They are not authoritative and must not be supplied as substantive guidance to the rerun.

Failure record:

`state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-FAILED-RUN-2026-09-10.md`

## Exact next gate — fresh blind rerun with file-based transport

Run:

`tasks/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-WORKER-2026-09-10.md`

in a **new target-theory-blind context**.

For substantive reasoning that worker reads only the original frozen audit prompt plus its four authoritative measurement inputs. It must not inspect the failed run or target-theory material.

Instead of pasting a giant answer into chat, it writes exactly:

- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`

Then it runs:

```bash
python scripts/validate_life_patterns_subcode_overlap_absence_audit.py \
  --findings state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl \
  --summary state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json
```

The validator is mechanical only: JSON syntax, exact fields/enums, sequential IDs, internal summary counts, blocking-finding references, and 22-observable coverage. It does not judge substantive correctness.

The fresh worker commits the validated raw audit artifacts and returns only commit SHA, file hashes/sizes, validator result, and finding count. It does **not** revise the codebook/UI/response contract.

## Why the audit remains necessary

Owner review exposed that NBM-R05 is explicitly two-facet but was flattened in the human UI:

- option-set construction: `R05-O1..R05-O6`;
- choice resolution: `R05-R1..R05-R9`.

Some values can co-occur across facets. `R05-O2` is also structurally hybrid: affirmative default acceptance plus an absence-of-alternative-search condition. Its `non_action` registry status concerns the **absence of search**, not the affirmative acceptance itself. The audit must determine whether this and analogous issues across all 22 observables are presentation-only, response-contract limitations, or substantive codebook overlap requiring versioned theory-blind repair.

## Disposition only after the valid blind audit is frozen

- presentation-only findings -> repair UI grouping/copy and exact absence-target prompts;
- response-contract limitations -> make a versioned response contract before collection;
- substantive codebook overlap -> make a versioned theory-blind codebook clarification/revision, preserving historical artifacts, then regenerate dependent package/handoff/UI.

Do not use target-model information for any repair.

## Human calibration remains suspended

All current auditor kits are historical owner-review artifacts only. Do not give them to an independent auditor until the valid overlap/absence audit is frozen and all blocking findings are resolved.

The following prior design corrections remain controlling:

- ask the substantive human question directly;
- derive machine states behind the scenes;
- hide machine IDs;
- one-source provenance automatic;
- no optional research-data busywork;
- multiple-value ordering asked only after multiple values are selected;
- errors tell the human what action to take;
- generalized behavioral recurrence self-report is direct reported-recurrence evidence;
- self-selected confirming anecdotes are not independent frequency evidence.

## Hard boundaries

- no current auditor kit may be used for new human collection;
- no partial finding from the failed first audit may steer substantive repair;
- no theory-exposed substantive neutral-codebook repair before the valid blind audit is frozen;
- no automated Life Patterns coding before the eventual revised independent human first pass is frozen;
- no target-model scoring/reveal;
- never commit private participant narrative or private calibration HTML;
- no merge/deploy, assistant-initiated auditor recruitment/contact, or spending without separate authorization.
