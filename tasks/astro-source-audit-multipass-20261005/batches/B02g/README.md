# Lilly wealth source packet: B02g

Start with REPORT.md for the findings and source-page references, and CONVERSATION_HANDOFF.md for the exact continuation point. RULES.json contains 122 normalized historical source records; its top-level collection is `rules`. Source claims, printed calculations, retrospective reports and unresolved points remain separate.

The packet reproduces the completed second-house section, Book II XXVII–XXVIII, PDF pages 201–221 of the registered 894-page witness. The raw PDF, full text and original page images are not included. Their source identity and exact hash are recorded in READING_RECEIPT.json and the handoff. Original-source inspection remains necessary for independent philological rechecking.

## Reproduce the new checks

In the distribution ZIP, this directory is B02g and its sibling B02f contains the unchanged retained geometry helper. From the extracted ZIP root, run:

```sh
python3 -m unittest discover -s B02g -p 'test_lilly_wealth*.py' -v
```

These 28 new tests use the Python standard library. The supported run for this delivery used Python 3.12. They verify source-data integrity, preserved qualifications and uncertainty, and bounded static arithmetic. They do not evaluate predictive accuracy.

The original focused research run passed 121 tests: these 28 plus 93 retained tests. Its four logs preserve the exact pytest commands and outputs. Replaying all 121 requires the full HumanDesign research checkout and pytest; the packet's standalone command targets the 28 new tests only. Repeating those tests for ZIP usability does not increase the number of distinct passing tests.

The B02f helper is included unchanged to supply geometric functions used here. Its other data-dependent functions refer to the full B02f datasets and are outside the standalone wealth-packet interface. Do not treat the companion as a complete copy of B02f.

## Provenance and delivery

MANIFEST.json hashes the immutable source snapshot, including its reviewed report, source records, tests and evidence. Its exclusions are explicit to avoid self-hash and publication/delivery cycles. The distribution provenance names the exact published source revision. The publication and owner-delivery receipts record transfers separately; extracting records or passing tests alone does not prove those transfers.

All earlier source batches, participant inputs, fitted models and prediction freezes remain unchanged. The broader multi-author audit stays open; next extract the third-house heading and entire preamble below the divider on PDF 221, then Chapter XXIX on PDF 222.
