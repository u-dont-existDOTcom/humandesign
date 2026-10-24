# C21 Hellenistic primary-source research — durable continuation checkpoint

**Date:** 2026-10-24. **Stable main objective:** reconstruct and compare ancient astrological doctrines with documentary/source fidelity as one component of the broader *humandesign* 16-tradition map; later freeze variants and test against blinded, previously unseen actual human responses. **Root outcome OPEN, human predictive validations 0.** Ancient-text arithmetic, literary agreement and three codices sharing a table are NOT empirical human validation.

## Per-turn authority and isolated writing

Recover current `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md` and `LESSON-INDEX.md`, then `u-dont-existDOTcom/humandesign/AGENTS.md` and this checkpoint. Do not redo earlier C01–C20 book acquisitions or previously tested paper source corpus. No biography-driven readings, no merging unvalidated rules into production, no alteration of other traditions' map, no paid source purchase, and **never use Work to extract the owner's Gansten purchased Kindle book**.

- Parent accepted C20 SHA `c1b81156fad7b785b1449a775b863aac9b179b97` on `research/astro-hellenistic-c20-berlin-constraints-20261024`.
- Current exclusive C21 research branch `research/astro-hellenistic-c21-paulus-greek-20261024`, isolated worktree under `/home/joel/development-worktrees/humandesign/astro-hellenistic-c21-20261024`.
- Original research integration branch `research/astro-missing-book-audit-20261022` is integrator-owned; do not mutate or merge to it automatically.
- Source-critical C21 files: [research report](HELLENISTIC_SOURCE_C21_PAULUS_GREEK_TEXT_SCOPE_20261024.md), [exact short Greek clauses, page/hash provenance and open gaps](PAULUS_C21_GREEK_SECT_LIGHT_CLAUSES_V1.json), [source-domain adapter](paulus_c21_luminary_scope.py), [12 targeted regressions](test_hellenistic_c21_greek_sect_light.py), plus the `README.md` map pointer. No full-source copyright text in the repository.

## New textual evidence actually checked

**Eulogikon Greek original-language body** of Paulus's `Eisagogika` now accessed as both HTML and downloadable Markdown with HTTP200, recorded SHA256s. The digital Greek's 2026-10-23 edition/transcription is **modern**, NOT a second ancient manuscript or Boer 1958 printed critical apparatus. Chapters **5, 32 and 33** were read directly:

1. **Ch 5 by-sign monomoiria:** zodiac sign's domicile lord begins, seven-planet Chaldean order; Greek expressly includes **arcminutes as a degree**. Frozen C04 physical longitudes [n°,n+1°) use ordinal n+1 correctly. This supports existing C20 Berlin **Moon candidates 2/9/16/23 completed degrees**, but does NOT make its editor's **2°35′** definite.
2. **Ch 32 trigon monomoiria:** assigns the degree of **the light of sect**—Sun by day, Moon by night—from the appropriate sect triplicity lord; prevents second allotment to a planet before first star's return, supporting C05 *seven-distinct* narrative interpretation. Subjoined authorial diurnal table is described as **daytime**, with rulers reversed in nighttime case, fire opening **Jupiter–Sun** at night. The printed *digital rendition* contains trigon headings **but no legible 120-value matrix**. This does not resolve C04/C05 34/120 discrepancies or physically photographed scribal tables (Munich, Florence, Vatican), which remain source facts even where discordant.
3. **Ch 33** uses sect-light trigon monomoiria as one possible **Ascendant reconstruction**, alongside alternative procedures involving Moon's terms and previous syzygy. None of this directly establishes an individual Berlin papyrus Ascendant or whether a term-lord was visibly preserved. Do not apply chapter-32 *sect light* formula to arbitrary angular or planetary longitude simply because a historian compared them.

Source: `https://eulogikon.org/works/paul-alexandria-astrology-sum-aa.md`. Checked digital body SHA-256 `78b9da9d8fdf9187c969ebb4cd3b46151f9831d8e68d238274962f0e8696a263` (181,883 bytes); HTML SHA `ee00fd3c669cee1484b355b2b2ec04544f69bf159046d6d914fade0e51cd29cc`. The site's separate `content_hash` `sha256:e8d2406af73b0ab048c54663f266f83e37a27188a560b7a076b7d89c5bc54084` is **not** the downloaded file SHA.

## Research-only implementation and validation boundary

`paulus_c21_luminary_scope.py` checks the explicit **named luminary versus sect** before delegating to *unchanged* C05 narrative allocation. It rejects a generic `Ascendant` input or contradictory day/Moon, night/Sun pairing; ch 32 requires an explicit ordinal degree, without implicitly copying the fractional-degree convention from ch 5. The wrapper itself is a research interpretation, not authoritative translation or production natal algorithm.

The existing C04/C05 distinction remains: sevenfold Greek prose narrative vs Greenbaum corrected table **34/120** disagreement; physically inspected three manuscript tables have an eight-slot duplicated-Venus pattern with water exceptions; at Cancer ordinal degree 8, manuscript family = Mercury, Greenbaum = Mars, Greek narrative = Venus (all kept as separate rows/scope). C17 Oxford P.Oxy.4277 original photographs remain authenticated, its edited source match **1/3, two failures**. C20 Berlin paper four hypothetical Ascendant degrees remains untouched. No source data selected for fit to known biographies.

## Repro and next source frontiers

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**Verified C21 historical-source regression: 182/182 PASSED, exit 0** on isolated C21 worktree (170 retained C20 + 12 new source tests). Focused 12/12 also passed. These are *source/arithmetic tests only*, not human predictive validations. No release/merge permission implied.

**Next direct source work:**
- Access Boer **1958 printed Greek chapter-32 diagram and apparatus**, where planetary 120-cell original rows, corrections and manuscript sigla can be distinguished. Eulogikon *omits* those digital cell values. Do not silently treat a reconstruction as a printed source.
- Boer **1962** commentary Greek/diagram and Paris **Z/Y** genuinely different manuscripts to evaluate genealogical independence, not repeated codices.
- Jones **1999** *P.Oxy.* 4277 vol. II pp421–427 Greek restorations using the already-authenticated Oxford image, separate original ink/editor completions.
- Pursue other independent documentary original horoscopes with explicit degree and independent planetary label only where a source method can actually be tested without choosing answers after seeing the data.

**One-line resume:** C21 establishes from Greek chapters 5/32/33 that by-sign arcminutes count within the ordinal degree, trigonal monomoiria belongs to the **sect light** and skips prior planet repetition, and Ascendant derivation is a separate set of alternatives. **Online text does not contain the 120-cell printed matrix**, so Greek literary vs physical manuscript grid disagreements remain open. **0 human validations, no production rule.**

## C22 source-reconciliation addendum

The previous 34/120 figure counted differences between two sevenfold daytime methods, not the full difference from the manuscript. A complete C22 candidate table comparison found 12 matches to both, 11 narrative-only, 1 Greenbaum-only and 96 neither, across 120 cells. This is one unblinded manuscript-family transcription rather than human validation. The original C04/C05 rules and C21 source conclusions remain unchanged. See C22 report and continuation.
