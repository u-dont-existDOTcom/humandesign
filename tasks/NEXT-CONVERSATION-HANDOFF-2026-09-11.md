# Life Patterns — next-conversation handoff — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

GitHub is canonical. Before substantive work, fetch the **current PR #24 head**; do not infer current state from an older chat/handoff.

## Read order

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-11.md`
3. `state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`
4. `state/LIFE-PATTERNS-V5-PRIVATE-UI-REGEN-BLOCKED-2026-09-11.json`
5. `tasks/LIFE-PATTERNS-V5-PRIVATE-UI-REGEN-OWNER-REVIEW-WORKER-2026-09-11.md`
6. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
7. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-VERIFIED-2026-09-10.json`
8. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
9. `scripts/build_life_patterns_human_calibration_ui_v5.py`
10. `scripts/build_life_patterns_human_calibration_ui_v5_final.py`
11. `docs/research/LIFE_PATTERNS_HUMAN_CALIBRATION_MINIMAL_BURDEN_POLICY_2026-09-09.md`
12. `docs/research/LIFE_PATTERNS_RECURRENCE_EVIDENCE_POLICY_v2_2026-09-08.md`
13. `state/CURRENT-STATE.md`

## Current controlling result

The blind V5 semantic/contract gate is closed successfully:

- repair: `320cb577f4adfbcc644c986f7f532feef0fbe80b`
- independent re-review: `ce04642146c41a7d5d94f85360572c78de887682`
- all **47 carried findings resolved**
- no blocking new finding
- `semantic_change_required=false`
- `safe_for_implementation=true`

The public V5 mechanical implementation is also closed successfully:

- implementation code head: `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`
- CI run `34623829382`: **SUCCESS**
- **675 passed, 7 expected skips, 0 failed**
- Ruff: **all checks passed**
- strict mypy: **no issues in 174 source files**

Public verification receipt:

`state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`

Do **not** rerun the V5 semantic repair/review or redo the public implementation unless new evidence demonstrates a real defect.

## What changed mechanically

The accepted V5 response graph is implemented with response-level record containment, exact-one references, stage/evidence-unit ownership, stage-local cardinality, claim-specific provenance, four-part absence gates, cross-facet co-presence without forced ordering, and same-fact anti-double-counting.

An implementation-only hybrid restriction was corrected: pure absence-dependent values such as `R14-i` may carry exactly one gated absence component. Mixed hybrid values still require their accepted affirmative+absence pair. A hybrid affirmative can remain observed if the paired absence is insufficient, while the combined hybrid parent is withheld.

The final owner-facing V5 builder is:

`scripts/build_life_patterns_human_calibration_ui_v5_final.py`

It preserves historical V2 files and the private embedding boundary, groups human choices by facet, removes the old global value-relation question, asks stage/chronology only when meaningful, uses claim-specific quote provenance for multi-source claims, exports V5 episode/series envelopes, and uses the exact top-level fallback labels:

- `Doesn't apply to this story`
- `Not enough information`

Silence/non-mention is not affirmative absence.

## Exact private source identity

The next gate requires the exact **outer transport ZIP**, not merely the inner receipt hash.

Outer transport supplied to the builder:

- filename: `Life-Patterns-Recurrence-Corrected-Human-Calibration-V2-PRIVATE-2026-09-08.zip`
- SHA-256: `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- bytes: `422297`
- members: `15`

Inner LPHB2 receipt that must also independently verify:

- receipt id: `LPHB2-F34245FAE32B513DDCFE`
- receipt SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- packets: `8`

**The inner receipt SHA is not the outer ZIP SHA.**

Current-context recovery attempted File Library lookup three times, including exact filename/hash lookup; the retrieval service errored and returned no file bytes. Prior-context retrieval did not recover the bytes either. Public GitHub intentionally does not contain them. See:

`state/LIFE-PATTERNS-V5-PRIVATE-UI-REGEN-BLOCKED-2026-09-11.json`

## Exact next gate

Recover or re-supply the exact outer ZIP above, then run:

`tasks/LIFE-PATTERNS-V5-PRIVATE-UI-REGEN-OWNER-REVIEW-WORKER-2026-09-11.md`

Do not reconstruct the ZIP from public artifacts, chat, or memory.

With the exact bytes available:

1. verify outer ZIP SHA-256 and byte count;
2. verify the inner LPHB2 receipt and its declared member/packet bindings;
3. build the final private offline V5 UI using `scripts/build_life_patterns_human_calibration_ui_v5_final.py`;
4. browser-smoke the real private package under the worker's checklist;
5. write only a public-safe hash/status receipt — never private evidence or generated private HTML — to GitHub;
6. return the private UI/package to the owner for hands-on usability review.

Technical smoke tests do **not** equal owner acceptance.

## Authorization boundary

**Human collection remains unauthorized.**

Only explicit owner acceptance of the regenerated private V5 UI may unlock the independent human first pass. Only after that entire revised independent human first pass is completed and frozen may automated Life Patterns participant coding begin. Target-model scoring/reveal remains later and separately unauthorized.

## Hard boundaries

- do not commit private participant narrative, exact private handoff bytes, decrypted evidence, or generated private HTML;
- do not reconstruct missing private evidence;
- do not start independent human collection before owner UI acceptance;
- do not perform automated participant coding before the revised independent human first pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy, assistant-initiated recruitment/contact, or spending without separate authorization.
