# Life Patterns current state — 2026-09-10

Status: public-safe controlling overlay for the active Life Patterns development-transfer task. This supersedes the 2026-09-09 overlay for current next-action state but does not erase historical records.

## Current scientific gate

**Human calibration is paused before collection.** Owner UI review exposed a possible substantive neutral-measurement defect in NBM-R05 and a broader need to audit all subcodes for overlap/facet/absence semantics before an independent human first pass.

No qualifying independent human first-pass annotations have been collected. No automated Life Patterns coding, consensus, human-vs-automated comparison, target-model scoring, or reveal has occurred.

## R05 finding

The frozen reconciled codebook explicitly defines NBM-R05 as two facets:

1. option-set construction (`R05-O1..O6`);
2. choice resolution (`R05-R1..R9`).

The current human UI flattened them into one list, hiding that values from different facets may legitimately co-occur.

`R05-O2` — “accepts one/default option without searching for alternatives” — is additionally hybrid:

- **affirmative behavior:** accepts/selects one/default option;
- **absence condition:** does not search for alternatives.

The frozen non-action registry includes R05-O2 because its truth depends on proving the **absence of alternative search**, not because accepting an option is itself non-action. The prior generic UI wording “did not act” was therefore semantically wrong for this value.

The same R05-O2 wording also appears potentially overlapping with R05-R1 (selects without reported comparison / first acceptable option) and R05-R4 (follows an explicit rule, prior commitment, or default). Whether that is acceptable complementary facet coding, a response-contract problem, or substantive redundancy must be resolved theory-blind before collection.

## First overlap/absence audit attempt — invalid

The owner returned the first attempted fresh blind audit output on 2026-09-10. It is **not an authoritative audit artifact**.

Returned text identity:

- bytes: `17554`
- SHA-256: `0e3b339c9e7ffa6362ada0a13ec2b2d11911608e7b5cdca4c39216a79f5a5b81`

Failure facts:

- Markdown escaping made the returned lines invalid JSON as transported;
- after diagnostic removal of the presentation-only underscore escapes, only OA-001..OA-009 form a parseable prefix;
- OA-010 is corrupted;
- the remainder contains process/meta commentary rather than required findings;
- no complete 22-observable audit or final summary JSON exists.

Do not salvage or use the partial prefix. The rerun must be fresh and must not receive those partial findings as substantive input.

Failure record:

`state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-FAILED-RUN-2026-09-10.md`

## Required audit rerun

Canonical substantive audit prompt:

`state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-PROMPT-v1-2026-09-10.txt`

Execution wrapper:

`tasks/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-WORKER-2026-09-10.md`

Run the wrapper in a new target-theory-blind context. For substantive reasoning the worker uses only the frozen audit prompt and its four authoritative measurement inputs.

To avoid another large-response transport failure, the worker writes the complete audit directly to:

- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`

Then it must pass the mechanical validator:

`scripts/validate_life_patterns_subcode_overlap_absence_audit.py`

The validator checks transport/schema/internal consistency only; it does not judge substantive correctness.

## Disposition rules after a valid blind audit is frozen

- Presentation-only finding -> repair the human UI, explicitly group facets, and name the precise absence proposition in any evidence gate.
- Response-contract limitation -> create a new versioned contract before collection.
- Substantive codebook overlap -> perform a new theory-blind versioned neutral-measurement clarification/revision, preserving all historical v1/v2 artifacts unchanged, then regenerate dependent package/handoff/UI.

Do not tune any revision using target-model information.

## Suspended artifacts

Every existing private auditor kit remains historical owner-review material only and is **not eligible for new independent human collection** until this audit gate is cleared.

## Existing corrections that remain controlling

- generalized behavioral recurrence self-report is evidence of reported recurrence;
- confirming anecdotes are not independent frequency observations;
- concrete examples are requested only for information gain;
- human UI asks substantive behavioral questions directly and derives machine state behind the scenes;
- machine IDs and optional research-data busywork are not human tasks;
- one-source provenance is automatic;
- ordering is asked only after multiple behaviors are selected and must use plain-language behavior labels.

## Hard boundaries

- no independent human collection yet;
- no automated coding before the eventual revised human first pass is frozen;
- no theory-exposed substantive neutral-codebook repair;
- no target-model scoring/reveal;
- no merge/deploy, assistant-initiated auditor contact/recruitment, or spending;
- never commit private participant narrative or private calibration HTML.
