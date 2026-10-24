# Correct Wellcome 1647 page-to-canvas references

2026-10-24. This is a source-LOCATOR correction, not a numeric-text edit.

The earlier original Lilly 1647 first-edition page photographs from Wellcome Collection (b30338724) were saved with correct printed page labels 713, 714, 715 and correctly SHA-256 verified. The preceding research metadata mistakenly stated one-less IIIF zero-based canvas indices.

A direct photograph-to-printed-page check established:
- Printed page 713 -> ZERO-BASED IIIF canvas 747
- Printed page 714 -> ZERO-BASED IIIF canvas 748
- Printed page 715 -> ZERO-BASED IIIF canvas 749

IIIF manifest: https://iiif.wellcomecollection.org/presentation/v2/b30338724

In this isolated research branch I corrected the old source metadata, regenerated the row-level Naibod CSV source notes and source provenance JSON, updated the test and README, and rebuilt its file-hash verification manifest.

The underlying source photos, actual printed numerals and algorithms are unchanged. Previous verified findings remain: 22 original year-column versus modern retype differences; one original 1′=5d4h versus retype 1′=6d4h difference; original minute-27 label absent; minute rows 25,28,39,41,44,48 uncertain. There remain 23 verified NUMERIC TABLE-CELL source differences, plus a separate worked-example final-prose difference.

Do not silently rewrite the earlier published source branch; this note explicitly records its superseding locator correction. No personal natal data, human responses or historical prediction timing rules were changed.
