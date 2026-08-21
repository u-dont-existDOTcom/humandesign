# Blind and validation boundary audit

Audit commit: `dc2b5455619afcf82a09828c5e3090fc86b600ba`  
Audit date: 2026-08-21  
Execution: read-only; no benchmark or answer-key operation

## Conclusion

No enabled recovery or API route directly accepts answer-key material. However, the findings below can invalidate a blind-validation or untouched-final-test claim unless they are closed. They are implementation gaps, not evidence that the completed 75-case artifact was altered.

## Findings

| Severity | Finding | Required disposition |
|---|---|---|
| High | Synthetic recovery checks for plaintext answer keys only at freeze, after scoring, and the scan is limited to `*.json`. | Run a fail-closed preflight before scoring; broaden defense-in-depth detection; document and require a genuinely keyless OS/container boundary for claim-grade runs. |
| High | A reveal record stores an encrypted-envelope hash but verification does not check the envelope, and evaluation accepts an independently supplied plaintext dictionary. | Bind the reveal receipt to canonical decrypted-key bytes and encrypted-envelope bytes; verify both before evaluation. |
| High | Noise comparison loads evaluation, manifest, and blind input but does not establish the prediction freeze/reveal chain. | Verify predictions, freeze, reveal receipt, envelope, manifest binding, evaluation hashes, and timestamp ordering without decrypting the key. |
| High | Human final-test evaluation is in memory and cannot enforce a one-time release or prove freeze-before-reveal ordering. | Use sealed external key material, append-only protocol/freeze/reveal/release receipts, timestamp checks, and a persistent single-use release ledger before making an untouched-final-test claim. |
| Medium | Human blind scoring accepts a caller-provided callable whose claimed model reference is checked but whose implementation/capabilities are not. | Construct the scorer internally from exact frozen artifacts or run it in a restricted keyless worker; bind code identity. |
| Medium | Human bundle fitting checks development IDs but does not validate record content against `PersonSplitManifest.dataset_hash`. | Accept the full dataset at the high-level fit boundary, validate the manifest, select development internally, and bind the selected content hash. |
| Medium | Recovery resume validates input hashes but not the full recovery configuration. | Require exact manifest/config equality and bind aggregation, threshold, and related settings into comparison provenance. |
| Low | Generation prints the external reveal-key path. | Print only a non-secret receipt/status identifier; keep secret-location logs evaluator-only. |

## Controls verified

- Synthetic reveal verifies frozen prediction bytes before decryption.
- `recover` exposes no key or reveal option, and its runtime function has no answer-key parameter.
- Enabled FastAPI dependencies are non-secret; stateful reveal/run routes fail closed.
- Revealed target-set hashing includes case ID, true UTC, local date, and chart hash.
- Noise comparison rejects missing or unequal target-set hashes.
- Human participant IDs are unique/disjoint, and existing high-level fitting requires exactly the manifest's development IDs.

## Claim boundary

The pre-recovery filesystem scan is defense in depth only. Same-user file permissions and a predictable external path do not isolate a decoder from evaluator secrets. A claim-grade blind run must execute recovery in a distinct keyless user/container/workspace with only public inputs mounted. Code-level signatures and hashes then provide the auditable artifact chain; they do not replace process isolation.

## Implementation status

The synthetic preflight/reveal/noise/resume fixes and the human dataset/scorer/final-release fixes are assigned on isolated branches. This report must be updated with exact commits and tests before those findings are marked closed.
