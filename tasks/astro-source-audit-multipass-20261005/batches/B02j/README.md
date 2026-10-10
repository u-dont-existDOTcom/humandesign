# Fifth-house source-audit packet

This packet contains the complete B02j extraction of Lilly, Book II, XXXIX–XLIII, PDF256 below the divider through PDF276. It is source research and bounded reference arithmetic. It does not make personal predictions or medical assessments.

Start with `AUDIT_REPORT.md`. `RULES.json` contains all 201 records and their conditions, qualifications, source locations, original-reader fields and unresolved references. `RECORD_ID_MAP.json` maps the report’s short A/B/C identifiers to canonical records R1157–R1357. Conditions are explicitly **non-executable** source representations. A flat list of source clauses must never be interpreted as an implicit AND.

`SECTION_COVERAGE.json` accounts for all admitted headings and unnumbered material. `UNRESOLVED.json` retains 64 typed limit entries; it is not a count of source mistakes. `WORKED_NUMERIC_TABLES.json` preserves 45 coordinate entries, including inferred signs, missing Mercury minutes in the figure and the separate later arithmetic witness. `HISTORICAL_CASES.json` keeps two dated enquiries and their dependent claims together.

`ARITHMETIC_CHECKS.json` is the replay output. `lilly_fifth_house_reference.py` implements only the declared static comparisons and small source mappings. It does not select a whole-chart judgment, calculate a historical ephemeris, choose disputed readings or combine timing methods. The 6:6 hour-chain replay is an explicitly conditional analyst sensitivity calculation; Lilly’s printed 8:4 table stays unchanged.

## Run the standalone checks

Python 3 standard library is sufficient for the delivered test suite:

```bash
cd B02j
python3 -m unittest -v test_lilly_fifth_house
```

There are 36 unique focused tests. Prior subset runs and the archive repeat do not add unique tests. `TEST_RUN_SUMMARY.json` and `TEST_B02j.txt` preserve the source checkpoint execution. `PACKET_USABILITY.json`, delivered beside the ZIP, records the actual extraction/hash/run check of that archive.

For a fresh arithmetic replay without rewriting the packet:

```bash
python3 - <<'PY'
import json
from pathlib import Path
from lilly_fifth_house_reference import comparison_receipt
print(json.dumps(comparison_receipt(json.loads(Path('WORKED_NUMERIC_TABLES.json').read_text())), indent=2))
PY
```

`build_root_source.py` and `build_source_data.py` preserve the source assembly procedures. Running them rewrites their generated files and should be done only in a disposable copy. `build_batch_evidence.py` is an archival controller script: it additionally expects the original source PDF, retained repository and task scratch inputs, and PyMuPDF. It is **not** needed to read the packet, replay the arithmetic or run the 36 tests.

## Provenance and supporting material

`source_readers/` holds the frozen notes, original candidate arrays, scope receipts and targeted errata checks. `implementation_review/` preserves the collaborator’s initial diagnosis, including findings subsequently repaired. `IMPLEMENTATION_RECONCILIATION.json` binds those repairs to the final test receipt. The final independent source/claim diagnosis and its reconciliation are separate so that initial findings are never silently rewritten.

`RETAINED_SOURCE_EXCERPTS.json` contains four exact earlier records used for targeted within-Lilly comparisons. It does not duplicate the whole retained corpus. `LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json` gives the cumulative frontier; the larger Ptolemy audit is retained at 1,066 records and was not rerun here.

`evidence/` contains selected original-page and detail witnesses for the two figures, the testimony table and arithmetic. The original 894-page source PDF is not inside the archive. It is identified by SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`, filename `Lilly-1647-Christian-Astrology-I-III.pdf`, Wellcome witness `b30338724`. Use its 1-based PDF page numbers; printed pages in this admitted span are 34 lower.

Publication, preservation and delivery receipts distinguish source-core state, packaged distribution and final transport verification. The archive manifest has an explicit file set; it does not hash itself or claim to contain receipts created after the ZIP was finalized.

## Next source passage

PDF277 / printed243, at the top: “Of the sixt House, and its Questions.” Include “Sicknesse, Servants, small Cattle.” and Chapter XLIV, “Judgment of Sicknesse by ASTROLOGY.” Include the complete opening paragraph. This passage was inspected only as the boundary and remains unextracted. The broader multi-author, multipass research task remains open.
