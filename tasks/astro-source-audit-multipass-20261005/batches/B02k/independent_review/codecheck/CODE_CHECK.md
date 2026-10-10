# Frozen independent code check — B02k candidate 01

**Finding:** I found no demonstrated implementation defect in the inspected bounded helper or verification runner. The frozen candidate contains **33 distinct unittest identities**, and a fresh private execution ran all 33 with **0 failures, 0 errors and 0 skips**. The principal weaknesses concern what those tests do not establish and what meaning the caller must supply.

This is a diagnostic code/data/test review. It does not adjudicate the historical fidelity of the 192 source records, validate clinical or predictive use, authorize repair, or certify integration in the wider project runtime.

## Frozen input and independence

The candidate manifest SHA-256 matches the assigned digest exactly: `9cc2299b54c514c07c6e330471d791bb7597875c5730c4116e9e703fd51976c0`. Every consumed candidate file below was checked against that manifest, and all eleven listed input files were unchanged when the audit ended.

I fetched the current main-branch root AGENTS.md through the connected GitHub tool before candidate review (Git blob `c27948c88cf7553f95241cbae7edab27f87689d2`). I used the parent-provided guidance copies for the independent-evaluation, source-provenance, task-activation and output rules; their exact hashes and the connected bootstrap receipts are retained in the JSON companion. Guidance copies are not represented as a separately fetched current commit.

The evaluator was a fresh delegated context. The parent disclosed the expected 33-test claim; the candidate test results were necessarily visible because those claims were being checked. I did not open producer source notes or drafts, helper_review contents, source_readers contents, other workers’ findings, or source-correction diagnoses. The audit report was limited to headings and lines 3–26, 55–77 and 139–150. Those spans also contain candidate inventory/provenance assertions; this code check does not adopt their historical conclusions.

RULES.json and SECTION_COVERAGE.json were hash-verified and machine-read only as suite dependencies and for bounded structural probes. Their historical narratives were not reviewed. No original PDF page or source image was opened, and no original source page is cited as independently observed here.

## Reproduction and distinct identities

| Test class | Distinct identities |
|---|---:|
| `TimeSelection` | 8 |
| `LunarMotion` | 5 |
| `SourcePredicateQualifications` | 4 |
| `RemainingArc` | 5 |
| `SourceLookups` | 5 |
| `SourceRecordIntegrity` | 6 |
| **Total** | **33** |

The count was independently recovered from the test-file AST and matched both the 33 retained log identities and the retained summary’s discovered identities. Private execution discovered the same set. Repeating those tests adds **zero** new test identities. The full exact identity list is in CODE_CHECK.json and REPRODUCTION.json. [Evidence: test_lilly_sixth_opening.py; TEST_B02k.txt:1–38; TEST_RUN_SUMMARY.json:4–55; AUDIT_REPORT.md:147.]

Execution used Python 3.12.14 and the command below from the private_run directory. The original helper, test file, runner and three JSON dependencies were copied byte-for-byte before execution. The candidate was never used as a writable test directory.

```text
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B run_verification.py
```

The process returned exit status 0. The retained receipt’s five file hashes all matched the frozen inputs, and its log SHA-256 matched TEST_B02k.txt. The fresh runner generated separate logs and a separate summary under private_run. Its nondeterministic elapsed-time line means a new log digest need not equal the historical log digest. The result counts and identities, rather than elapsed time, were the comparison target.

The runner correctly enumerates identities before unittest consumes the suite, counts distinct names with a set, records actual result fields, and exits according to wasSuccessful. It writes next to itself, which is why execution was isolated. The candidate summary does not record the runner hash or Python version; the frozen candidate manifest binds the runner, and this audit records its actual Python environment. [Evidence: run_verification.py:13–41; REPRODUCTION.json.]

## What the code establishes

### Source-time selection

The first two event stages are ordered and require explicit unavailability before falling back. An unknown earlier event prevents selection of a later event. At the third stage, known alternatives are retained; an unknown alternative preserves UNKNOWN, different supplied token strings preserve CHOICE_UNRESOLVED, and equal strings can share SELECTED. The TimeEvidence constructor requires exact bool/None availability and a nonblank string token only when availability is True. This is selection among supplied event identifiers, not validation of chronology, calendar conversion or event truth. [Evidence: lilly_sixth_opening_reference.py:42–100.]

### Guarded descriptive conditions

All facts accept exact bool or None. A known False defeats a conjunction even if another input is unknown; otherwise an unknown produces UNKNOWN. The two public guarded predicates preserve unknown when negating their explicit exclusions. The caller supplies whether the benefic is an author of disease and whether the disease is both decreasing and leaving. SATISFIED describes the supplied prerequisites; the function does not return a prognosis, certainty or probability. [Evidence: lilly_sixth_opening_reference.py:21–39 and 144–162.]

### Lunar thresholds and within-sign arithmetic

The declared mean is 47,436 arcseconds, the separate analogy threshold is 47,400 arcseconds, and their difference is 36 arcseconds. Both comparisons are strict. The four receipt examples produce the reported boolean pairs, including the distinct outcomes between the two thresholds. These are numerical facts about the declared constants, not verification of their historical attribution. [Evidence: lilly_sixth_opening_reference.py:17–18 and 109–122; ARITHMETIC_CHECKS.json:6–48; ARITHMETIC_RECOMPUTATION.json.]

Remaining arc is calculated exactly with Fraction. The input (29, 30, 0) yields 1/2 degree. Each known component is range-checked; when all three are known, their combined position must also remain below 30 degrees. Missing components keep remaining_degrees unknown, and time_unit is always None. Fractional inputs are used exactly without rounding or selection of months, weeks or days. [Evidence: lilly_sixth_opening_reference.py:125–141; test_lilly_sixth_opening.py:116–136; ARITHMETIC_CHECKS.json:49–75.]

The arithmetic receipt was independently recomputed from its DMS and coordinate strings: all 21 comparisons passed, including its bound helper hash. The receipt names `python build_analysis_evidence.py` as its original execution, but that generator is not in the frozen manifest and was not run here. Its numerical content was corroborated; its original generator-execution event was not independently established.

Numeric validation is a representation boundary. A valid integer passed as daily motion is interpreted as arcseconds even if the caller intended degrees. The function name and parameter contract carry the unit; the API does not use unit-tagged values or dimensional analysis. The test called invalid_units checks invalid Python representations, not accidental substitution of another unit. [Evidence: lilly_sixth_opening_reference.py:103–122; test_lilly_sixth_opening.py:83–89.]

### Lookup, signs and preserved precision

The frozen table has five namespaces and 37 entries: 12 house rows, 12 sign rows, 7 planet rows, 1 retained planet-sign callback and 5 historical star labels. The actual twelve sign identities and the exact house/planet key sets are present. All 37 lookups returned exactly their selected JSON entry in the supplemental pass. Unknown namespaces and unrecorded keys were rejected, including attempted house/sign substitution and an unlisted planet-sign cell. The Saturn-in-Cancer callback remains a separate entry from generic Cancer. [Evidence: REFERENCE_TABLES.json#/namespaces; lilly_sixth_opening_reference.py:165–178; BOUNDED_PROBES.json.]

All five star entries retain null minutes, seconds, modern_epoch_longitude, ordinal_to_continuous_degree_convention and nearness_threshold. This demonstrates missing precision remains missing in the frozen data; it does not verify the historical degree numbers against a source image. Returned nested structures are detached from retained data. [Evidence: REFERENCE_TABLES.json#/namespaces/historical_fixed_star; BOUNDED_PROBES.json.]

The namespace is case-sensitive and the key is converted with str, which admits integer house keys. A caller-supplied path can load another JSON file. The function does not enforce schema, source hashes or the top-level source_only/clinical_mapping flags. The source-bound claim in this audit therefore applies to the verified frozen default table, not to arbitrary caller-supplied data. [Evidence: lilly_sixth_opening_reference.py:171–178.]

## Coverage weaknesses and material limits

### COV-01: Catalogue test checks sign count rather than exact sign identities; most table contents are not asserted

The house and planet key sets are asserted exactly, but the sign test only requires length 12. Only the Saturn-in-Cancer row and selected Pleiades fields receive content assertions. A wrong or substituted sign key, changed unasserted row content, or false precision in four other stars could evade those candidate tests.

**Current candidate:** The independent probe verified the actual twelve sign identities, all 37 lookup routes, and the five null precision fields on all five star rows. They passed. Exact routing equality is equality to the supplied JSON, not historical-source fidelity.

**Remaining limit:** The candidate unittest suite does not retain those broader identity/precision checks, and neither suite comparison verifies correspondence wording against the original source.

Evidence: test_lilly_sixth_opening.py:140-144; test_lilly_sixth_opening.py:146-166; REFERENCE_TABLES.json#/namespaces; BOUNDED_PROBES.json#/probe_groups/lookup_catalogues; BOUNDED_PROBES.json#/probe_groups/all_lookup_routing.

### COV-02: Record-integrity assertions establish structure and flags rather than checked meaning

The test named test_all_records_have_checked_source_anchors_and_conditions checks nonempty anchor/source strings, condition_logic field presence, and a page-set range. It does not inspect an image or check source entailment, condition content, or nonempty page arrays. Coverage equality is a set comparison, which does not establish semantic segmentation or unique assignment. Contiguous numbering alone does not fix the expected 192-record total.

**Current candidate:** The independent structural probe additionally found 192 records, 192 unique full IDs, nonempty page arrays, and aligned locator-array lengths. Those checks passed. The candidate report correctly limits mechanical checks to anchor presence and coverage at line 145.

**Remaining limit:** Correct transcription, complete source coverage, clause meaning, and classification remain for the parent source evaluator. Passing these tests cannot establish them.

Evidence: test_lilly_sixth_opening.py:175-205; test_lilly_sixth_opening.py:207-212; AUDIT_REPORT.md:145.

### COV-03: Several material API validation branches are absent from the 33 candidate tests

The retained suite lacks many invalid TimeEvidence forms, strict boolean checks across every exposed predicate path, a full false/unknown condition matrix, valid Fraction lunar inputs, valid fractional coordinate arithmetic, an unknown namespace lookup, and nested source-locator return mutation.

**Current candidate:** The one-shot supplemental pass covered representative validation branches, all 243 time-availability combinations for a shared stage-three token, all 81 four-input combinations for each guarded predicate, exact fractional arithmetic, unknown namespace rejection, and nested lookup detachment. All observed checks passed. The retained distinct unittest count remains 33.

**Remaining limit:** These audit probes supplement this diagnosis; they are not present in the candidate test file and do not add candidate unittest identities.

Evidence: test_lilly_sixth_opening.py:59-63; test_lilly_sixth_opening.py:83-89; test_lilly_sixth_opening.py:92-136; test_lilly_sixth_opening.py:157-166; lilly_sixth_opening_reference.py:21-39; lilly_sixth_opening_reference.py:53-59; lilly_sixth_opening_reference.py:103-141; lilly_sixth_opening_reference.py:171-178.

The supplemental pass executed 632 assertion checks, with group counts and failures recorded in BOUNDED_PROBES.json. It found no failing observation. This includes a finite 243-case availability matrix, 81-case conjunction and guarded-predicate matrices, validation cases, exact arithmetic, lookup routing and structural checks. These are supplemental audit assertions, not 632 additional candidate unittest identities and not independent historical observations.

## Non-predictive boundary and final disposition

Complete inspection of the helper supports its narrow component-level boundary: it selects supplied event evidence, compares numbers, tests caller-qualified prerequisites, calculates remaining arc and retrieves table entries. It contains no horoscope reconstruction, treatment selection, survival estimate or predictive aggregation. The tests also verify that all records carry REFERENCE_ONLY_NOT_PROMOTED, independent_evidence_unit false and case_id null. [Evidence: lilly_sixth_opening_reference.py:1–178; test_lilly_sixth_opening.py:187–191.]

Those flags do not prove that no code elsewhere in the project consumes the records in a prediction runtime. The wider repository and runtime were outside this audit. The report’s global non-promotion statement is therefore supported here only by the inspected component and metadata, while its explicit absence of clinical/predictive validation is consistent with all inspected code and receipts. [Evidence: AUDIT_REPORT.md:7 and 145; TEST_RUN_SUMMARY.json:53–55; ARITHMETIC_CHECKS.json:74–75.]

**Disposition:** no demonstrated code defect requiring a candidate change was identified in this bounded pass. Three coverage weaknesses are retained as diagnostic findings, with current-candidate probes and residual limits separated. Historical attribution, complete source fidelity, clinical/predictive validity and wider runtime integration remain outside this conclusion. The parent evaluator owns reconciliation and any later action.

## Exact input hashes

Full candidate inputs below were SHA-256 checked before use and after the audit. AUDIT_REPORT.md was read only in the stated ranges; RULES.json and SECTION_COVERAGE.json were machine-read dependencies. The companion JSON also contains guidance hashes, bootstrap blob identities, exact test IDs, claim checks and API-boundary details.

| Input | SHA-256 |
|---|---|
| REVIEW_CANDIDATE_MANIFEST.json | `9cc2299b54c514c07c6e330471d791bb7597875c5730c4116e9e703fd51976c0` |
| lilly_sixth_opening_reference.py | `25777500a00551208e0fcae59a16af347d9cb513d1602b4f1299c959695244d5` |
| test_lilly_sixth_opening.py | `3d3186e86772b16903f914f168c38c58ca952578aa4458e388cad994115e64db` |
| run_verification.py | `0bded9bea1063348aa462d758da5a840cd294958e53e8109aacd70926afef4d3` |
| REFERENCE_TABLES.json | `d3e2476aa8ce05ff8fcb2c1fd1642abc6fbd8fea0df4f561aff15c077d03212e` |
| TEST_RUN_SUMMARY.json | `b638dbba461196e863b4bd95cc2a9e05cd8bca899c7fc2501978c1db0d53d9f7` |
| TEST_B02k.txt | `b49a4418e7ae67801d84f07abc014b586d4bfdc8176e83745f3457446ce91bc8` |
| ARITHMETIC_CHECKS.json | `a08ea0aca4d99f065286becbefdb5bd523264678c0de55a66334b45838a47234` |
| AUDIT_REPORT.md | `b41de7cbf9b8b391a3a59d092e6effd4857520a8d6c04bf1acbcf0299466b049` |
| RULES.json | `60ab17ba2ebc6fd0c23e3d698eb276834af82655da430c2d7ce6b12cf516e6a4` |
| SECTION_COVERAGE.json | `5786ddb13b68e2a2ad5f53565342704a7c3d55eea5aab2faa236fcd4ef0a7938` |

## Reproduction materials

CODE_CHECK.json is the structured companion to this report. REPRODUCTION.json holds environment, exact test identities, hash comparisons and fresh execution results. BOUNDED_PROBES.json and bounded_probes.py retain the one-shot boundary pass. ARITHMETIC_RECOMPUTATION.json retains the independent receipt recomputation. The runner’s reproduced log and summary remain under private_run; REPRODUCED_STDOUT.txt and REPRODUCED_STDERR.txt retain process output.

The two CODE_CHECK files are the frozen diagnostic result. FROZEN_OUTPUT_MANIFEST.json records their exact hashes and supporting-evidence hashes. They were made read-only after writing. No candidate or repository file was edited, no Git action or owner-device action was taken, and no repair/re-review loop was run.
