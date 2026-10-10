# B02l changed-item repair round 1

## Recommendation

**Accept IF-01 through IF-06 as resolved.** R1560 and the five repaired report units now preserve the source readings identified in the frozen initial diagnosis. The new C42 correctly binds the existing title/byline, resolving MC-01’s omitted-text-binding issue.

**One metadata evidence-reference correction remains:** C42 cites `TASK_ENVELOPE.json`, but that file is absent from the frozen candidate and its 45-file manifest. This is RR1-01. The metadata facts themselves remain supported by the source context and provided task-start metadata. Include and manifest the exact cited task envelope, or replace that unavailable filename with a truthful, available provenance reference. No further change to R1560 or the five corrected source paragraphs is required.

This is a recommendation within the agreed diagnostic role. Root retains final adjudication. The remaining reference issue was introduced in the expressly reviewed C42; it is not an additional source-review, testing or assurance gate.

## Source-adjudicated repairs

| Finding | Target | Round-one result |
|---|---|---|
| IF-01 | R1560/A011 | Original PDF294/printed260 prints **principall Significators**. All seven affected canonical/duplicate strings now preserve the plural. The repeated-from uncertainty remains; no all-of-group rule is added. |
| IF-02 | C10 | Exclusions now apply to **both Saturn and Mars**, matching original **neither of them** on PDF294. Prior strength, square/opposition and other qualifications remain. R1562 is unchanged. |
| IF-03 | C35 | Earlier PDF283/printed249 **sign nature/quality** is separated from later PDF301/printed267 **disease quality/nature and discretion**. No combined algorithm or extra cases are inferred. R1438 is unchanged. |
| IF-04 | C09 | PDF294/printed260 is now included in the citation and ledger page list for the lordship clause crossing the page break. Meaning and R1559 are unchanged. |
| IF-05 | C24 | **Sign of the eighth house of the yearly revolution of the World** is restored, retaining the natal-angle reference frame and other qualifications. R1629 is unchanged. |
| IF-06 | C08 | The transient distemper is now the explanation of suspicion accompanying alternative no-present/no-ensuing-sickness judgments. Negative-scope uncertainty remains. R1557 is unchanged. |
| MC-01 | C42 | Existing title/byline is uniquely bound and correctly hashed. Its factual metadata is supported. A newly introduced unavailable evidence filename remains as RR1-01. |

I inspected direct original-PDF crops only for the changed assertions, on PDF283,293,294,300 and301. Unchanged sections were not reopened for another exhaustive source review. The exact before/after claim texts, changed record leaves and point-of-use evidence are retained in `CHANGED_ITEM_RESULTS.json`.

## Remaining correction: RR1-01

C42 lists `SECTION_COVERAGE.json` and `TASK_ENVELOPE.json` as evidence. The first exists and is manifest-bound. The second does not exist in `/workspace/scratch/43f75264c32e/review-candidate-b02l-02/` and is absent from `CANDIDATE_MANIFEST.json`.

The report title/byline was already present in candidate01 and was supported in frozen MC-01. This finding concerns the newly introduced evidence pointer, not an assertion that the date or batch label is false. The bounded repair is to package the actual cited envelope or use an available, truthful metadata-provenance reference. No new source research, helper change or test identity is requested.

## Exact carry-forward accounting

| Inventory | Final accounting |
|---|---:|
| Source-first units retained | 92 |
| Canonical records | 101 = 100 unchanged + 1 rechecked |
| Ledger units | 42 = 36 unchanged + 5 rechecked + 1 new metadata unit |
| Table data rows | 25, unchanged and carried forward |
| Candidate02 manifest files verified | 45 |
| Original source-window page comparisons carried forward | 14 |
| Canonical distinct focused tests | 20 |
| New test identities in this round | 0 |
| Remaining source-meaning corrections | 0 |
| Remaining metadata-reference corrections | 1 |

The 100 unchanged records are identical JSON objects, with matching normalized hashes. The 36 unchanged ledger items are identical complete objects, including text, citations and qualifiers. After substituting placeholders for the five changed report units, candidate01 and candidate02 report text is identical. C42 binds the existing title/byline; it does not add or modify report prose. All 42 ledger texts occur exactly once and match their text hashes. All substantive report text and the formerly unbound metadata remain accounted for; unchanged organizational headings carry forward from the original whole-report scan.

Only six existing manifest files changed: `RULES.json`, `AUDIT_REPORT.md`, `CLAIM_LEDGER.json`, the current Lilly index snapshot, the actual test summary, and the actual test log. The two added files are `ROOT_SOURCE_CORRECTIONS.json` and `REPAIR_ROUND01_CHANGESET.json`. The former was hash-verified as a file without reading its narrative. All 45 declared file hashes and byte counts match.

## Helper, tests and index

The helper, test module and runner are byte-identical to candidate01. The repaired actual test receipt and log report the same 20 tests, with no failure, error or skip. The exact test ID list is unchanged, and every receipt-bound tested-file hash matches candidate02. The current Lilly index differs only in the current B02l `RULES.json` hash, now:

`7f95bfd2e73d8c3c6f5ababdd12ee6e04b45fae314b35323ae50f905899c966c`

I did not run an additional independent suite in this repair round. The initial private execution and helper behavior review carry forward through unchanged code/test identities; the repaired actual receipt is checked against the changed data/index hashes. Repeated execution creates no new test identities. No claim of disease-prediction or treatment efficacy follows.

## Preserved freezes and limits

The original source-first outputs and all 30 files bound by the initial diagnosis freeze remain byte-for-byte unchanged. SC-01 (**vitious**, not the reviewer’s initial **viscous**) and SC-02 (**she longs after**, not the initial **he** anchor) remain disclosed. The candidate was correct on those readings. IC-01, the nonunique inheritance of the fiery-sign condition into the Venus/Mars continuation, remains as previously diagnosed; unchanged R1601 was not newly adjudicated.

No candidate or canonical file was changed. Work and new evidence remain in the private `repair_round01/` directory. No other-worker narrative, reconciliation or status summaries were read, no agent inventory was used, and no additional review scope was introduced. The modern byline date was assessed using the provided task metadata; no mid-task clock read or fabricated completion time was used.

This is same-family contextual diagnostic review. It is not cross-family, expert, clinical, IV&V or empirical validation. If a follow-up is requested, the existing policy allows at most one remaining changed-item repair check, limited to the metadata-reference correction and resulting bindings.

## Artifacts

- `CHANGED_ITEM_RESULTS.json`: per-finding decisions, exact changed claim objects, record-field differences, remaining correction and acceptance recommendation.
- `MECHANICAL_CARRY_FORWARD.json`: all file, record, ledger, code, test and index comparisons, plus prior-freeze integrity checks.
- `REPAIR_REPORT_RESIDUAL.txt`: report after masking all42 bound ledger units.
- `REPAIR_ROUND01_FREEZE.json`: hashes and byte counts for the completed result and direct original-source crops.
