# Model B detailed-source recovery audit

Audit date: 2026-08-21  
Machine-readable record: `mappings/model_b_detailed_v2_source_recovery_audit_v1.json`

## Conclusion

The original pre-search D1–D10/A1–A6 detailed mapping definitions were not recovered. `MODEL-B-DETAILED-V1` remains a useful structural intermediate, but it is not completion of the detailed-model objective. A scoreable `MODEL-B-DETAILED-V2` was not compiled because doing so would require inventing rules or reverse-engineering them from legacy outcomes.

No Model A/B behavioral benchmark is permitted yet: Model B V1 still delegates behavioral generation and scoring to Model A and therefore cannot produce different behavioral predictions.

## What the hashes establish

The legacy freeze binds two surviving inputs exactly:

| Legacy field | SHA-256 | Exact surviving artifact | What it proves |
|---|---|---|---|
| `target_sha256` | `54a7720f893d425bd34af500cec1a2580a9f12f2647742131b27daab1d5a7d34` | `reference/core/behavioral_target_combined(5).md` | The behavioral target text used by the legacy run survives. |
| `rubric_sha256` | `678f552b989f3547900a33e1e45fccaad2da969d94c950d0ec976d853455761f` | `reference/core/human_design_search_instructions_fixed_candidate_blind(6).md` | The generic scoring policy used by the legacy run survives. |

The target is not a D/A mapping table. The rubric freezes general salience, directness, pathway-combination, dependency, conditional-prevalence, contradiction, and holdout mechanics, but it does not assign those mechanics to D1–D10 or A1–A6. The legacy result contains no hash for a separate mapping source.

## Result-only evidence kept separate

`reference/legacy_runs/hd_global_search_results.json` records holdout seed `42` and these labels:

- `A5 defined Heart`
- `D1 61-24`
- `D2 43-23`
- `D6 28-38`

These are retained as result metadata showing that definitions existed. They are not treated as independently recovered pre-search definitions, complete structural selectors, or permission to infer the remaining split. Candidate winners, ranked paths, support values, prevalence values, and contribution patterns were not used to derive mappings.

## Separate partial calibration source

A mounted backup contains a reproducibly hashed CNA-S v1 calibration engine:

- engine SHA-256 `fede7bfae86a74525ed33e2249da7ef3376ccdf2a8b36a394c948fd88cd4c2d7`;
- README SHA-256 `0bba7252e744a1e8f59a8d19511f41e89171b2db1cf74b2ecaab585317089b8c`;
- README-recorded pre-run commitment `25991279f6006f8a503ff4c5bb3e1defa5e95424`;
- complete-channel presence weights: 43-23 = 12, 61-24 = 10, 1-8 = 8, and 26-44 = 8, plus coarse Type/Profile/Authority/topology weights.

This is not the missing detailed dictionary. The engine has no D labels, no behavioral observations or questionnaire response predictions for those channels, and no per-path role, directness, dependency, contradiction, or conditional-prevalence assignment. Its A1–A10 functions are explicitly Western-astrology modules, not the requested HD A1–A6 identifiers. Its README also describes the HD score as case-calibrated self-discrimination rather than independent validation. The artifact is therefore recorded as separate calibration provenance only and is not compiled or relabeled as `MODEL-B-DETAILED-V2`.

## Exact missing definition material

For every ID A1–A6 and D1–D10, the following pre-search material is missing:

- exact behavioral observation definition or predicted response;
- every allowed channel/gate/cardinal/repeated/Node/hanging pathway and its formal selector;
- primary, alternative, or corroborating role per pathway;
- directness class per pathway;
- dependency-cluster membership and reuse relationship;
- contradiction condition and severity;
- conditional-prevalence parent set per pathway;
- source citation and rationale.

The complete explicit discovery/holdout assignment is missing. The four holdout labels above survive only inside the result artifact; no unlisted ID is classified as discovery by inference. Also missing are the original mapping source list, atomic observation/confidence inventory, compiler or scorer, mapping configuration/library, implementation commit, and ephemeris file hashes.

## Surfaces audited

- Both independent repository roots and all refs, reflogs, path history, deleted/renamed history, and pickaxe searches. Both roots introduce the same `reference/` content; there is no older parent.
- The moved pre-init Git directory at `/tmp/hdmatch-empty-git-placeholder`. It is unborn and its index tree exactly equals the local baseline tree.
- Every unreachable Git object. All are recent Codex implementation or stash artifacts; none contains the historical definitions.
- Current source, scripts, configuration, generated artifacts, and source comments.
- The accessible project and Custom GPT ZIPs. Their manifests list only the already-known specification/reference material.
- A mounted older reverse-search package. Its generic protocol requires a frozen mapping table, but the package does not include that table.
- Accessible Human Design-related sibling files, mounted Downloads/Archives/Backups, constrained Trash/editor-backup locations, and exact legacy identifiers under `/home/joel` and `/tmp`.

No external cloud-account search or deleted-disk forensic recovery was attempted. Secrets, browser/session histories, unrelated personal files, real candidate data, and result/winner contents were not inspected. Archive timestamps alone were not accepted as provenance.

## Scientific disposition

- `MODEL-A-CORE-V1` remains the completed 75-case engineering baseline. No additional expensive Model A benchmark is needed.
- `MODEL-B-DETAILED-V1` is preserved and relabeled as structural-only/intermediate.
- `MODEL-B-DETAILED-V2` remains uncompiled unless the original pre-search definitions are supplied or recovered later.
- A separately labeled empirical model may be learned from development humans, but it cannot be called the historically frozen symbolic model and development performance cannot be presented as predictive validation.
