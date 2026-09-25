# Life Patterns neutral measurement repair — fresh blind worker

Use this wrapper for the **substantive repair proposal only**. The complete overlap/absence audit is already frozen and valid. Do not rerun the audit.

## Fresh-context requirement

Work in a new target-theory-blind context. Do not inspect Human Design, astrology, target mappings, birth/chart data, target-model outputs, participant-specific model results, or model-fit results.

For substantive reasoning follow exactly:

`state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-PROMPT-v1-2026-09-10.txt`

Read only the authoritative inputs listed inside that prompt.

## Frozen audit identity

Authoritative audit commit:

`7ea0641e0913815306f8c182be5e7e8b18115fff`

Expected audit artifacts:

- raw JSONL: `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-RAW-v1-2026-09-10.jsonl`
  - SHA-256 `37642f31135f3d446488a3a0a6736468b30b6114d5a292bcaf01096d65fb16e6`
  - bytes `83030`
  - findings `134`
- summary: `state/LIFE-PATTERNS-SUBCODE-OVERLAP-ABSENCE-AUDIT-SUMMARY-v1-2026-09-10.json`
  - SHA-256 `7184f89a9d6c8fa0560e0ceba07287f101f559ddcf872b3db62e39de34cb7b47`
  - bytes `1170`

Verify these identities before reasoning. If they do not match, stop rather than repairing a different audit.

## Required outputs

Create exactly the three candidate artifacts specified by the repair prompt:

1. `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-CLARIFICATION-v2-CANDIDATE-2026-09-10.md`
2. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v3-CANDIDATE-2026-09-10.json`
3. `state/LIFE-PATTERNS-OVERLAP-AUDIT-BLOCKER-RESOLUTION-v1-2026-09-10.jsonl`

The blocker matrix must contain all and only the 45 blocking OA IDs from the frozen audit summary, exactly once each.

## Commit discipline

Before committing:

- parse the contract JSON;
- parse every blocker-matrix line as JSON;
- verify matrix finding IDs exactly equal the 45 frozen blocking IDs with no duplicates;
- verify every matrix object uses the exact required field set;
- verify every `ready_for_blind_review` value is `true` only when the resolution field states a concrete rule;
- verify the candidate codebook document explicitly preserves historical v1 rather than overwriting it;
- verify no target-theory terminology or target-model information appears in the substantive repair artifacts except a generic statement that such information was unavailable/unused.

Commit the three exact candidate artifacts to `codex/discover-life-patterns-mvp` and push them.

Return only:

- GitHub-visible commit SHA;
- SHA-256 and byte size for each of the three files;
- blocker matrix row count;
- exact statement that all 45 blocking IDs are present exactly once;
- exact statement that no software/UI/package implementation was performed;
- exact statement that no target-model information was used.

## Stop boundary

Do not modify the original v1 codebook, existing response schemas, package, calibration selection, human handoff, or auditor UI. Do not code participant evidence. Do not run automated coding, consensus, human calibration, target scoring/reveal, merge/deploy, recruitment/contact, or spending.

A second fresh target-theory-blind reviewer must audit these candidate artifacts before implementation.
