# Real private development preparation — 2026-09-06

Handoff steps 1–4 are executed. The next gate is the independent blind human
first pass, before any automated coding. This stage is **development in progress**.

## Canonical baseline and source provenance

GitHub was revalidated at task entry:

- main: `afc0bb82de0e481ae5a5d3453e0bcaf82b2a0286`; CI run 33454801631 successful.
- PR #24: open/draft/unmerged, head `5a278d135af4de5190d9b74d8e55489dc92efaf1`;
  base `codex/astrohd-owner-intake-quality-v1` at
  `40154251534cffebaf7f2b78b48c5a97c707b629`; CI run 34059401473 successful.
- The preparation source is that exact PR head. Later packaging/privacy repairs
  preserve the already generated source, selection, package and packet bytes.

The two exact source JSONs were found locally, copied unchanged into ignored
private storage, and checked against their original bytes after preparation.
`execution-receipt.json` records both exact-file SHA-256 and canonical parsed-JSON
SHA-256. The package's `source_record_sha256` and `supplement_sha256` refer to the
latter; they are not exact-file hashes. Neither original was overwritten.

The private CLI was run with defaults and `--render-blind-packets`:

```bash
.venv/bin/python scripts/prepare_life_patterns_development_package.py \
  --v8-record experiments/private/life-patterns/v8.json \
  --v8-1-supplement experiments/private/life-patterns/v8.1.json \
  --output-dir experiments/private/life-patterns/prepared-2026-09-06 \
  --source-commit 5a278d135af4de5190d9b74d8e55489dc92efaf1 \
  --render-blind-packets
```

Do not rerun into this immutable directory. Exact replay requires the original
preparation timestamp in `execution-receipt.json`, the original source commit and
unchanged inputs. A replay verified identical corpus, package, calibration
manifest, and all 16 packet bytes; it did not resample or replace the originals.

## Generated evidence

- Package: `LPKG-18170B8D3EEC8423A523`.
- Corpus: `LPDC-F2BBDA6F39040BF41D96`.
- Calibration selection: `LPCA-5B3E6CFCCE49807050DF`.

| Stratum | Eligible tasks | Observable units | Human units | Automated packets | Human packets |
|---|---:|---:|---:|---:|---:|
| Episodes | 17 | 374 | 44 | 6 | 6 |
| Exact-source repeated series | 5 | 110 | 22 | 2 | 2 |

There are 13 series reports in total; 8 summary-only reports remain preserved
privately and blocked from coding. Series are never counted as episodes.
The seed and all 66 human units were frozen before any labels existed, with the
unchanged per-observable selection floors of two episode units and one series unit.

This directory contains inspected public-safe receipts only. Actual source
records, corpus, tasks, packets, human forms and later raw responses belong under
`experiments/private/` and must never be staged or force-added.

## Saved human handoff and chronological boundary

The human handoff exporter reads the already prepared artifacts and copies only
the exact frozen human packets. It adds neutral response schemas, blank JSONL
forms, and an unfilled auditor attestation. Blank `state=null` values are not
annotations, cannot pass response validation, and must never become fabricated
human or automated coding. Exporting a bundle does not verify auditor identity
or attest to blindness.

```bash
.venv/bin/python scripts/export_life_patterns_human_calibration_bundle.py \
  --prepared-dir experiments/private/life-patterns/prepared-2026-09-06 \
  --output-dir experiments/private/life-patterns/human-calibration-2026-09-06
```

The owner identified a possible auditor who may complete the saved packet later.
No contact, recruitment, participation, independence, blindness, or completion is
inferred from that statement. Do not publish the auditor's identity. The owner can
contribute a separately identified sensitivity pass, but prior theory exposure
prevents that pass from serving as the independent blind benchmark.

Before accepting the human pass, confirm the auditor's independence and exposure
history; preserve exact first-pass raw responses and actual completion time;
validate full selected coverage separately for 44 episode and 22 series units;
and freeze the raw and validated artifacts before any LLM-label exposure.
`development_human_calibration.py` supplies the validators. Its built-in literal
attestations are not independent evidence of real chronology; the completed
human declaration and controlled handoff must support them.

Then follow handoff steps 6–10: at least three isolated passes per stratum,
separate deterministic consensus, comparison with the frozen human pass, a
theory-blind retain/revise decision, and a frozen validation route if justified.
This supervisor context has read target-related repository instructions and must
not be reused as an automated coder context. A fresh context alone is not an
access boundary: future coders must have access only to their assigned materials.

## Privacy, scientific risks and limits

- Source is `partial_exact_segments_only` and `prior_exposure_possible`.
  `development_only=true`, `validation_use_forbidden=true`, canonical BPF
  eligibility false, and target-model scoring unauthorized remain unchanged.
- Transfer summaries remain secondary orientation. Eight summary-only series
  are ineligible. Repeated series and episodes are dependent evidence from one
  development participant, not independent humans or interchangeable samples.
- A bounded lexical screen of actual task fields found zero explicit target-theory,
  birth-date/time or date-format flags. Exact patterns and limits are in
  `content-screen.json`. This is not proof of semantic blindness, deidentification,
  source completeness, or absence of indirect age/cohort/identity clues.
- Public receipt strings passed an allowlist check. The code now rejects arbitrary
  narrative in public blocked-series IDs and packet task IDs. Hashes can disclose
  equality with a known input; these approved hash receipts are not encryption.
- No duplicate or conflicting recovered original-turn IDs were found in these
  source files. The older recovery helper's last-value-wins behavior for conflicting
  duplicate IDs remains a limitation for future inputs; recheck changed sources.
- The human output contract was missing from the frozen human prompt. Providing
  schemas and empty forms repairs transport usability without changing the frozen
  measurement, packet content, selection, or labels.
- A human comparison can assess coding clarity/agreement. It does not establish
  construct validity, predictive validity, or the truth of any target theory.
- No human labels, automated labels, consensus, comparison, measurement revision,
  validation-route selection, target scoring/reveal, merge or deployment occurred.

## Verification and recovery

The inherited task lock was reconciled with the current owner request; its older
task/branch and historical next actions do not control this continuation.
`python scripts/task_preflight.py` verifies branch/checkpoint identity. The test
command in the lock is engineering verification only, not stage acceptance.

The first full-history test run exposed an inherited convergence-audit defect:
a supposedly historical rejection probe read present checkout files and therefore
could not regenerate its frozen receipt after later API changes. The probe now
materializes its declared `AUDITED_HEAD` for the diagnostic. The frozen historical
JSON and production behavior remain unchanged. Full-history regression tests
verify the exact regenerated bytes and the pinned source tree. Shallow CI skips
these history-dependent checks when the pinned commits are unavailable.

Run the full suite, CI-equivalent Ruff, and strict mypy after implementation
changes. Record final results in the canonical `state/CURRENT-STATE.md`; live
GitHub checks on the final branch head supersede the baseline run IDs above.

The next human action is to complete the saved independent first pass. Until then,
preserve these frozen artifacts and do not advance to automated coding.
