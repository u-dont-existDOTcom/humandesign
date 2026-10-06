# B01k — marriage and children

This is a source-only audit of Ptolemy IV.5-IV.6 in Robbins's supplied 1964 reprint. Start with REPORT.md, then RULES.json and RELATIONSHIP_FAMILY_TABLES.json. READING_RECEIPT.json and SECTION_COVERAGE.json bind the read spans. SOURCE_PAGE_QC.json records image inspection without redistributing book pages. CROSS_SOURCE_COMPARISONS.json distinguishes source scope from corroboration. UNRESOLVED_INTERPRETATIONS.json and INTRASOURCE_QUALIFICATIONS.json retain operational gaps.

The reference helper takes already-qualified source conditions. It is not a natal interpretation or fertility/relationship-safety engine. The historical sexual-role claims are archived in attributed records, not exposed as a classifier. No probabilities are provided.

Run the isolated checks with:

```sh
python -m pytest -q tasks/astro-source-audit-multipass-20261005/batches/B01k/test_b01k_reference.py
```

APPLY_CHECKPOINT.py is a guarded, one-time progression script for the declared baseline; do not rerun it against a later checkpoint. Existing rules and models are not promoted or changed by this batch.
