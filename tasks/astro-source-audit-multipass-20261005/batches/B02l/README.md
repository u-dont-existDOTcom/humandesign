# Lilly's Dariot continuation: records and report

Start with **AUDIT_REPORT.md** for the findings. The exact source span is the complete DARIOT Abridged introduction on original PDF292/printed258 through the upper bridge on PDF302/printed268, stopping above the divider before Hermes. Chapter XLIV and the wider audit remain open.

## Contents

- `RULES.json`: 101 source records, R1550–R1650, with full conditions, qualifications and provenance.
- `SECTION_COVERAGE.json`, `COUNTS.json` and the cumulative-index snapshots: scope and counts.
- `UNRESOLVED.json`: 36 retained limit/anomaly entries and six separately typed source-resolved entries.
- `REFERENCE_TABLES.json` and `ARITHMETIC_CHECKS.json`: documentary mappings and the bounded lunar-angle example.
- `evidence/Lilly-Dariot-Original-Source-Window.pdf`: original PDF292–302, 888, 277 and283, in that order. The first eleven pages are the admitted main-span page context. Extraction boundaries remain explicit.
- `source_readers/` and `independent_review/`: frozen source work and diagnosis evidence, in separate roles.
- `CLAIM_LEDGER.json`: every substantive report unit bound to its text and evidence.
- `CONTINUE_HANDOFF.md`: exact next source passage and preservation constraints.

## Run the focused checks

From this extracted folder, run:

```sh
python run_verification.py
```

Python's standard library is sufficient. This runs 20 distinct source-data and bounded reference tests and writes `TEST_RUN_SUMMARY.json`. The helper does not require an ephemeris, supplied patient, network access or the rest of the application. Repeating these tests does not increase the distinct-test total. The archive manifest, when present, records the delivered bytes before a local rerun rewrites its test receipt.

Rebuilding source data with `build_source_data.py` is a repository-maintenance operation: it expects the retained Ptolemy index and prior B02k records in their repository paths. It is not required to inspect the records or run the standalone suite.

The source-window PDF contains already-read and next-unread boundary context. Do not count the lower Hermes opening as part of this batch. No original Dariot collation, modern clinical mapping or predictive validation is claimed.

Publication, preservation, archive usability and direct-delivery operations have separate receipts. The record inventory and tests do not substitute for those receipts.
