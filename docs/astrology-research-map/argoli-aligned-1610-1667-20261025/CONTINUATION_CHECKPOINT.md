# Argoli aligned original-edition calculation checkpoint

**Date:** 25 October 2026. **Active research task:** `argoli-aligned-original-edition-math-20261025`. **Research branch:** `research/argoli-full-volume-source-20261025`. **Parent committed checkpoint:** `research/argoli-edition-witness-20261025` commit `e879c887c0f34039dbfc1dcf7f6ca787a3e8dbec`.

**Owner's root objective: OPEN.** The user wants historically differentiated Western, Hellenistic, Jyotish, Chinese and other astrological rule systems tested prospectively against genuinely untouched human evidence, independently frozen interpretations and proper controls. Exact geometry and source fidelity are subordinate supporting work, **not** predictive accuracy. Existing verified 96 synthetic charts, 173–188 scoped historical regression tests and the 800-case independent Regiomontanian geometry holdout remain preserved from parent commits; do NOT restart them.

## Actual new findings, independently observed in original page scans

1. A complete IIIF presentation manifest for the digitized **1610 Rome Argoli** `bsb11218073` returned **1760 BSB canvases**, source-hash `059bf74a74e89fa423987304001979761e0b7274df220ac1ad1524e954225fc7`. The Augsburg Staats- und Stadtbibliothek is named as holding institution; original rights NoC-NC. The image service permitted lawful scholarly access and the exact images on digital leaves **51,52,53** were obtained; they carry printed original pages **39,40,41**.
2. The pre-existing **1667 Michigan 107-image excerpt** contains a genuinely corresponding historical chapter passage at printed **pp.29–30**, extracted from scan physical leaves **42–43** and preserved in this branch. Earlier 1610 Chapter XIII aligns to later 1667 Chapter XV; do not compare unaligned same-numbered printed pages. Exactly five primary page images plus the full 1610 IIIF manifest are versioned.
3. Three worked calculations checked visually across aligned original pages and reproduced by typed exact sexagesimal arithmetic:
   - 1610 p39 / 1667 p29: 162°50′ − 125°11′ = **37°39′** in **both** printings.
   - 1610 p41 / 1667 p30: 14°20′ − 0°05′30″ = **14°14′30″**, same pole interpolation in both.
   - 1610 p41: 163°17′ − 119°55′ = **43°22′** correctly printed; 1667 p30 prints **45°22′** with the *same operands*, an observed apparent 2° arithmetic printing error. DO NOT replace the printed witness reading with the computed result; keep original and arithmetic separate.
4. A separate **1667 University of Turin** Internet Archive `bub_gb_065WxfytjWIC` PDF has **1,036 scanned leaves** (59,359,291 bytes; SHA-256 `2eacb5bb7f5b28f99dfea3d60c8728ddb467a33c53aebfbeb149606b8e4e87fc`). Saved zero-click on the user's Zorin laptop at `~/.local/share/hdmatch/research-artifacts/argoli-full-editions-20261025/Argoli_1667_Turin_Full_Volume_Archive_bub_gb_065WxfytjWIC.pdf`, with page-number JSON, scandata and text derivatives alongside. The inspected sections contain extensive position and oblique-ascension **tables**, reversed in printed page order; this is **not** an independent second prose copy of printed 1667 p30 and does not confirm whether the 45°22′ discrepancy occurs in multiple copies.
5. The separate **1644** original printing is still not collated. Google Books 1644 `55A7UHqfQi4C` / `KW9-ZybQ8eMC` returned HTTP429 from authorized Zorin route; Gallica IIIF original copies returned HTTP403 previously. Do not falsely report 1644 equivalence; preserve source blockers rather than hammering pages.

## Source files and method tests

- `ARGOLI_ALIGNED_EXAMPLES.json` is the structured source/edition alignment with source SHA and explicit 1667 printed discrepancy. Original BSB manifest and five original page JPEGs are in this directory.
- `src/hdmatch/astrology/argoli_printed_arithmetic.py` implements exact nonnegative sexagesimal (D/M, D/M/S) subtraction as a **small independent diagnostic**; cannot claim complete source method or authorial time keys.
- `tests/unit/test_argoli_aligned_1610_1667.py` checks all three arithmetic witnesses, hashes, BSB original IIIF canvas labels, source status and the preserved printing error.
- `README.md` is the human-readable source/evidence comparison. No paid books, secrets or human participant data were used.

## Future priorities

1. Obtain another **1667 original prose witness of aligned p30** to classify the 45°22′ source error as edition-wide vs scan/printing-copy-specific.
2. Find original **1644 method chapter** to compare correspondence across all three historical printings, targeting source headings and **numeric tuples**, not same-page numbers.
3. Separately complete historically source-backed primary-direction strength, time-key and genuine direct/converse conventions where the evidence permits; if not, retain unresolved branches without slowing the user-requested empirical project.
4. Independently freeze the modern diagnostic pilot interpretation, opportunity denominators, birth-time-uncertainty propagation and chart-label/temporal controls and acquire untouched human outcomes. Do not use synthetic parity or known-owner cases as validation.

**End-of-turn status:** math crosswalk and primary-source evidence require final source checksum verification, scoped test run, GitHub publication and local user Downloads ZIP. The historical third-edition collation and root empirical validation remain OPEN.

## Final mechanical verification

The original 1610 BSB institutional manifest contains 1,760 canvases. Exact original 1610 leaves 51–53 and 1667 Michigan leaves 42–43 have been hashed and visually aligned. The independent source test suite includes all three explicitly recorded calculations, original printed result statuses, IIIF source labels, and the two-degree 1667 mismatch. The first full inherited suite run had **five missing-file errors** only because the sparse worktree excluded the already committed Argoli-edition audit directory; after adding that existing directory without changing its files, the full suite passed **195/195**. This is an environmental checkout reconciliation, not a scientific or mathematical correction.

Focused code and manifest were checked with Ruff; the typed arithmetic and verification code passed mypy. Exact BSB source-image hashes and the original Michigan 1667 PDF hash were reverified; the new fully digital 1667 Turin tables PDF remains a separately hashed research source outside Git, to be delivered locally with the handoff.

The strongest source-level outcome is **two aligned original 1610/1667 arithmetic agreements and one apparent later printing error**, not complete collation of the editions. One original 1667 prose witness was examined for the error. New experimental human predictive evidence: **none**. Source-engineering milestone does not complete the root objective.
