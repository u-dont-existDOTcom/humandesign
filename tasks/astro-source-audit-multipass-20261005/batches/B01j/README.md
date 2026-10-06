# B01j source-audit packet

`REPORT.md` explains results. `RULES.json` and `EXTERNAL_FORTUNE_TABLES.json` preserve the conditional source records and tables. The reading receipt, coverage, source-page quality checks, unresolved ledger and cross-source comparisons establish their stated scope and provenance.

The source PDF and complete OCR are deliberately not included. They are the owner's existing private source files. The packet is not a new natal prediction model.

From this folder, with Python and pytest installed:

```bash
python3 -m pytest -q test_b01j_reference.py
```

`b01j_reference.py` uses only the included table. Route evidence and topical qualification must be established outside that helper. It does not calculate a natal chart or predict outcomes.

`APPLY_CHECKPOINT.py` is an integration/recovery utility for the exact repository baseline and writer branch recorded in `ACTIVE_CONTRACT.json`; it is not needed to read the report or run the isolated tests. The canonical repository retains the complete earlier audit.
