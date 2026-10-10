# Using the Lilly fourth-house source packet

Start with `AUDIT_REPORT.md`. The batch contains148 source records, the original reader notes/candidates, source/issue/case ledgers, one22-entry chart transcription, bounded reference code, arithmetic, focused test receipts and final review evidence. Its source scope is PDF236 through the last XXXVIII paragraph above the divider on256.

## Standalone verification

Extract the complete ZIP. From the extracted packet root run:

```bash
python3 verify_packet.py
python3 -B -m unittest discover -s B02i -p 'test_*.py' -v
```

The new standalone suite contains29 tests and uses the Python standard library. The required unchanged geometry helper is included under `B02f/lilly_presence_ship_reference.py`. No pytest installation is needed for this new suite.

To recompute the static numeric checks from the transcribed table:

```bash
python3 -B B02i/lilly_fourth_house_arithmetic.py
```

This writes `B02i/ARITHMETIC_CHECKS.json`; its output should reproduce the delivered arithmetic. Do not run generation scripts merely to read the report. `build_source_data.py`, `build_batch_evidence.py` and `run_verification.py` are repository-production tools; the latter two expect the full repository and retained source/test files. The standalone commands above are the supported packet interface.

## Where the evidence lives

- `RULES.json` is the admitted normalized inventory. Each record retains its original candidate as `source_fields`; `RECORD_ID_MAP.json` maps reader-local IDs to canonical IDs.
- `UNRESOLVED.json` separates50 unresolved textual/model/evidence limits from6 source-resolved readings. Those are not counts of proved author mistakes.
- `WORKED_NUMERIC_TABLES.json` is the exact frozen derivative copied from the source chart reader. Missing minutes remain null. `ARITHMETIC_CHECKS.json` records computations separately.
- `HISTORICAL_CASES.json` separates one enquiry, several dependent episodes, prior information, five bodily-mark reports and three unspecified experience accounts.
- `CROSS_SOURCE_COMPARISONS.json` and `RETAINED_SOURCE_EXCERPTS.json` include the required29 earlier source records. Source-repository paths in original receipts are provenance; local pointers in the derived comparison file lead to the included candidates and notes.
- `independent_review/` preserves source-first freezes and the fresh final diagnosis. Producer reconciliation and final review disposition are separate files.
- Index snapshots and the dated continuation state are in the packet's `context/` folder. The original894-page PDF is not included; its identity and precise page/paragraph locators are preserved, and the retained original remains the primary evidence.

The111-test repository result includes82 retained tests whose source projects are not duplicated wholesale into this packet. Their actual commands/results are included as receipts. The packet's29-test suite checks the complete new batch and its included arithmetic companion.

These files document a historical text and bounded calculations. No predictive model was promoted or empirically validated. The next reading starts with the fifth-house heading and XXXIX on PDF256 / printed222 below the divider.
