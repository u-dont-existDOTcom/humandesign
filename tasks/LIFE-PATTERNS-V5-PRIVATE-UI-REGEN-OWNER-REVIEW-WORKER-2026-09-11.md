# Life Patterns V5 private UI regeneration + owner usability gate — worker instructions

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

## Goal

Complete the **private-package boundary only** after the verified public V5 implementation. Regenerate the exact existing private human-calibration package into the final V5 human-first UI, browser-smoke the real private build, and return it to the owner for usability review.

This worker does **not** redesign semantics, recode participant evidence, start human collection, perform automated participant coding, reveal target-model outputs, or merge/deploy anything.

## Canonical prerequisites

Before doing work, fetch the current PR #24 head and read:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-11.md`
3. `state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`
4. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-VERIFIED-2026-09-10.json`
5. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
6. `scripts/build_life_patterns_human_calibration_ui_v5.py`
7. `scripts/build_life_patterns_human_calibration_ui_v5_final.py`
8. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`

The public implementation authority is the successful CI run `34623829382` for implementation head `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`: 675 passed, 7 expected skips, Ruff clean, strict mypy clean.

## Private source requirement

Use **only the exact existing private V2 handoff bytes** corresponding to the preserved receipt:

- receipt id: `LPHB2-F34245FAE32B513DDCFE`
- SHA-256: `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`

If those exact bytes are not available in the working/private context, **stop at this boundary**. Do not reconstruct the handoff from public artifacts, chat summaries, or memory. Report that the exact private handoff must be re-supplied/re-mounted.

Never commit, paste into public state, or otherwise expose private participant narrative, private handoff bytes, decrypted private evidence, or generated private calibration HTML.

## Required build

From a private/local working location outside the public repository, run the final builder against the exact verified handoff:

```bash
python scripts/build_life_patterns_human_calibration_ui_v5_final.py \
  --handoff-zip /PRIVATE/PATH/exact-v2-handoff.zip \
  --output-html /PRIVATE/PATH/life-patterns-human-calibration-v5-final.html
```

Record the generated build receipt privately and verify at minimum:

- receipt schema is `life-patterns-human-calibration-ui-final-build-receipt-v5`;
- embedded private handoff is unchanged;
- no network is required;
- owner usability review remains required;
- not-applicable label is `Doesn't apply to this story`;
- insufficient label is `Not enough information`.

## Real private browser smoke

Open the generated private HTML in the intended local browser. Test the real package without uploading private evidence anywhere.

Required smoke checks:

1. UI loads offline and private evidence is readable after the handoff unlock flow.
2. Navigation and progress save/reload work.
3. Top-level fallback labels/semantics are correct:
   - `Doesn't apply to this story` means the prerequisite is affirmatively absent;
   - `Not enough information` means the exact source is insufficient;
   - silence/non-mention is not treated as affirmative absence.
4. At least one ordinary affirmative value can be selected/saved.
5. Where a hybrid value is present in the real calibration set, verify:
   - affirmative component is separately selectable;
   - the absence claim has four separate gate questions;
   - an insufficient absence gate does not discard the affirmative fact and does not assert the combined hybrid parent.
   If no hybrid appears in the real selected units, record `not_applicable_to_real_unit_set` rather than manufacturing one.
6. Where a pure absence-dependent value appears, verify all four gate elements are required before it can be saved as observed. If none appears, record `not_applicable_to_real_unit_set`.
7. For multiple exact source segments, verify source choice is claim-specific. For a single source, verify provenance is automatic. Record whichever shapes actually occur in the real unit set.
8. If multiple same-facet substantive facts occur in a real unit, verify stage separation is requested; chronology is requested only after distinct stages and no temporal order is invented when source order is not established. If no such unit occurs, record `not_applicable_to_real_unit_set`.
9. Final response export produces:
   - `episode_responses.completed.v5.jsonl`
   - `series_responses.completed.v5.jsonl`
10. Existing progress backup and auditor-attestation downloads still work.
11. No network request is required or attempted.

Do not create synthetic private claims merely to force every conditional UI branch during the real smoke; those branches already have public automated tests. Test only shapes that actually occur in the private calibration set and explicitly mark absent shapes as not applicable.

## Public-safe verification artifact

After the real private smoke passes, write **one public-safe receipt only**, containing hashes/counts/statuses but no participant content or generated private HTML. Recommended path:

`state/LIFE-PATTERNS-V5-PRIVATE-UI-SMOKE-VERIFIED-2026-09-11.json`

It may record:

- exact private handoff receipt id/hash verification result;
- final builder commit/path;
- generated HTML SHA-256 and byte count only;
- offline/network status;
- smoke check status names without participant text;
- whether conditional shapes were tested or were not applicable to the real unit set;
- `owner_usability_review_pending=true`;
- `human_collection_authorized=false`.

Do not record filesystem paths that reveal private participant identity if those paths are identifying.

## Owner usability gate

Return the generated **private** V5 HTML/package to the owner for hands-on review. The owner decides whether the UI is understandable and usable.

Do **not** infer acceptance from technical tests. Human collection becomes eligible only after the owner explicitly accepts the UI. If the owner reports a usability defect, preserve the accepted V5 scientific semantics and repair only the human interaction/presentation unless a genuine semantic defect is demonstrated.

After explicit owner acceptance, persist a public-safe owner-acceptance receipt and update `tasks/ACTIVE-TASK.json`, the dated current-state overlay, `state/CURRENT-STATE.md`, and the continuation handoff. Only then may the independent human first pass begin.

## Hard boundaries

- no reconstruction of missing private evidence;
- no private participant content in GitHub;
- no human collection before explicit owner acceptance;
- no automated participant coding before the complete revised independent human first pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy, recruitment/contact, or spending without separate authorization.
