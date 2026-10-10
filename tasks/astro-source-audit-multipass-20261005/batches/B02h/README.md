# Lilly third-house source packet — B02h

Start with `AUDIT_REPORT.md`. `RULES.json` is the112-record admitted source inventory; earlier candidate snapshots under `independent_review/` preserve review history and are not added to the record count. `WORKED_NUMERIC_TABLES.json` contains all44 coordinate entries with sign-reading provenance and missing values. `ARITHMETIC_CHECKS.json` is reproducible static arithmetic from those entries.

The source span begins below the divider at the third-house heading on PDF221 / printed187 and ends on PDF235 / printed201. It includes XXIX–XXXI and the absent-brother heading/chart before the numbered XXX heading. Resume at the entire fourth-house heading and preamble on PDF236 / printed202, before XXXII on that page.

## Run the standalone B02h checks

The distributed ZIP preserves sibling `B02h/` and `B02f/` directories. `B02f/` contains the unchanged geometry helper required by the new code. From the extracted packet root, with Python3 available:

```bash
python3 verify_packet.py
python3 -B -m unittest discover -s B02h -p 'test_*.py' -v
python3 -B B02h/lilly_third_house_arithmetic.py
```

The standalone suite contains24 tests. The source repository's full focused run contains115 distinct tests: these24 plus28 retained B02g,31 retained B02f and32 methodology/index tests. The packet preserves their actual logs but does not pretend to include all earlier repository test suites.

The builders can reproduce source/context files without the original PDF:

```bash
python3 -B B02h/integrate_examples.py
python3 -B B02h/build_source_data.py
python3 -B B02h/build_batch_evidence.py
```

These regenerate the admitted normalized inventory from the retained production source and example candidates. Rerunning them is not an independent re-reading of the original. Rechecking an uncertain glyph still requires the identified original PDF.

## Evidence and limits

- `HISTORICAL_CASES.json`: two actual historical enquiries, one hypothetical reuse, two reported operational episodes in the absent-brother enquiry; no independent validation case.
- `APPLICABILITY_AND_RELATIONS.json`:11 context groups, exception/context links and example dependencies.
- `UNRESOLVED.json`:29 source-specific textual, methodological, precision and evidential limitations, not29 proved contradictions.
- `QUERY_REFERENCES.json`: both house frames and three distinct historical question-time anchors.
- `RETAINED_SOURCE_EXCERPTS.json`:23 unchanged earlier records required to inspect the eight within-Lilly comparisons.
- `READING_RECEIPT.json` and `independent_review/`: actual reading, frozen first findings and later reconciliation.
- `TEST_RUN_SUMMARY.json` and `TEST_*.txt`: actual focused checks, not empirical predictive accuracy.
- `MANIFEST.json`: immutable source-core hashes. Later transport/delivery receipts and generated distribution files are excluded to avoid recursive hashes.

The original894-page PDF, original page images and full extracted text remain outside Git and the packet. Source identity is `LILLY1647_WELLCOME_B30338724`; SHA-256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. It is the same retained witness used by earlier batches.

Core source completion, remote publication and owner delivery are distinct stages. Consult `SOURCE_PUBLICATION_RECEIPT.json`, `DELIVERABLES_MANIFEST.json`, `PACKET_USABILITY.json`, `DELIVERY_RECEIPT.json` and `CLOSEOUT.json` for the corresponding completed stage. Some of these are generated after the source core or ZIP and therefore are not recursively included inside their own hash manifests.

No automatic astrology verdict, personal health or financial assessment, fitted-model revision, historical prediction rewrite or new empirical accuracy claim is produced by this packet.
