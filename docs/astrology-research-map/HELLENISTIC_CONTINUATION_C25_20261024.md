# C25 — Vienna base commentary manuscript source continuation

**Date:** 24 October 2026. **Root owner outcome OPEN:** reconstruct ancient Hellenistic astrology accurately within a 16-tradition source map, and eventually independently freeze source models and test untouched/blinded real humans. **Human predictive validations: ZERO.** Historical-source tests check stored evidence and arithmetic but never demonstrate astrology works. Do not abandon the original source research for a model-fitting exercise.

## Required live bootstrap, owner controls, branch

Fetch live `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`, `LESSON-INDEX.md` and `u-dont-existDOTcom/humandesign/AGENTS.md` before reading this checkpoint and [C25 report](HELLENISTIC_SOURCE_C25_VIENNA_BASE_F205V_20261024.md). Preserve the established source map, all previous negative and unresolved source readings, and the owner's purchased Gansten Kindle exclusion (no Work extraction).

- **C24 accepted source base** `a189f796bb396b20b9554f9fb7d0351a77c04000`, branch `research/astro-hellenistic-c24-commentary-collation-20261024`.
- **C25 isolated child branch** `research/astro-hellenistic-c25-vienna-base-witness-20261024` on the owner's authorized computer, sparse-checkout `docs/astrology-research-map/`. Parent integration branch `research/astro-missing-book-audit-20261022` integrator-owned. No direct merge or production changes.
- New files: [C25 original source report](HELLENISTIC_SOURCE_C25_VIENNA_BASE_F205V_20261024.md), [exact primary-image metadata and bounded source-number register](HELIODORUS_C25_VIENNA_A_F205V_SOURCE_LAYOUT_V1.json), [strict numbered-degree layout comparator](heliodorus_c25_vienna_layout_audit.py), [C25 source-only tests](test_hellenistic_c25_vienna_base_layout.py), plus research-index pointer. No copyrighted photo or publication reproduced in Git.

## New actual original witness

**Vienna Österreichische Nationalbibliothek (ÖNB), Cod. phil. gr. 115 / historical Vindobonensis A**. Official catalogue `https://onb.digital/result/1182CE33`, complete official IIIF manifest `https://api.onb.ac.at/iiif/presentation/v3/manifest/1182CE33`, **468 canvases**. Commentary portion described in Pinakes as **f162r–218v**. Downloaded **125** original manuscript thumbnails, canvas indices **325–449**, all returned HTTP200, examined as **six** contact sheets; zero failed fetches. A red-ruled multi-column table was found on handwritten **folio 205v**, IIIF zero-index **417**, displayed **canvas 418**; neighboring folios 205r and 206r inspected.

Original photo IIIF service `https://api.onb.ac.at/iiif/image/v3/1182CE33/uk4nGb4uCinwsqiR`; physical original digital file declared **4192×6562**. Actual inspected study derivative `.../full/2600,/0/default.jpg`: **2600×4070**, **1,533,303 bytes**, SHA256 **`6b6e01af7442746186c8b7fef15d0687d53d982681ccebeb4106dc9fdde15748`**. Do not mislabel the hash as corresponding to the 4192×6562 full original. Temp owner-side study file `/tmp/c25-onb-review/Vienna-A-f205v-2600.jpg`; temporary photos not committed to Git. An appropriate source photo can be refetched if necessary but avoid repeating the 125-page search.

## Main C25 source observation and negative interpretation

**Vienna A folio205v appears structurally unlike Florence Plut.28.14 folio204v.** Vienna's red ruled table has four apparent triplicity sign-group headings, an additional **left Aries-marked section of unknown purpose**, red Greek ordinal numbering, and two **numbered-degree columns** per visual row. Directly inspected visible five candidate number pairs (numbering interpretation **provisional**):
(1,16), (2,17), (3,18), (14,29), (15,30). The layout plausibly splits **1–15** and **16–30** across approximately fifteen rows. **No complete table of Vienna planet assignments was independently read** (zero source degree→planet labels admitted); the exact red heading/adjacent Greek is not yet accurately deciphered to philological standards.

**C24 Florence** had **two planetary glyphs at each same ordinal degree** for 30 degrees × four triplicities (240 provisional, unblinded glyph names). The Vienna numbered subdivisions therefore **must NOT be called day/night slots** simply because they are side by side, and it is **not even proved this Vienna diagram is the *same monomoiria table*** rather than a different numerical/term/degree scheme within the commentary section. These distinctions are explicitly false-gated in C25 source registry/tests. Never use the 5 candidate numeral pairs to backfill hypothetical planetary labels. All C24 observations remain untouched: first slot C05 104/120, C04 102/120; second slot adjacent exchange 120/120 and C05 night 48/120, all **source-transcription diagnostics rather than human results**.

## Authorship and dating uncertainty

A 1963 contemporary review (Charles Mugler, *Revue des Études Grecques* 76 p294, URL in report) says **Boer chose older Vindobonensis A as principal manuscript for her 1962 edition** but replaced the lost early chapters 1–8 with a later 14th-century Byzantine recension. This is *an editor's report*, not direct inspection of the 1962 Greek critical apparatus and not proof f205v's table was used in the edition.

**Date must stay unresolved:** Official ÖNB catalog field **1200** with an explanatory note on **1241 solar eclipse**, specialist Pinakes **twelfth century around 1111–1169**, and another published range **1169–1241**. No silent reconciliation or selection based on being older.

## Next executable frontiers

1. Read **Greek page f205r, exact f205v table title and f206r**, ideally with qualified source-aware transcription and independent blind planet glyph verification. Determine what the table is (same monomoiria rule or another sort of degree/ruler table) *before* comparing literal planetary values with Florence or Boer. Confirm 15+15 degree numbering. A visual layout hypothesis by itself is not proof.
2. Compare its actual lemma with **Boer 1962 printed critical Greek apparatus**, especially Vienna A's manuscript siglum and locations; original printed text NOT read in C25. Distinguish actual Greek text and later editorial interventions.
3. Revisit the 14th-century Florence f204r/f205r adjacent prose and figure abbreviations, and possibly a distinct third commentary manuscript, if needed to distinguish day/night vs alternate degree sequence. Don't create source rules because recurrence looks elegant.
4. Keep P.Oxy.4277 published three label calculations **1/3 matches, two negatives** and Berlin 21347 conjectures **2,9,16,23** unchanged, pending Jones 1999 critical apparatus. Preserve all Hephaistio §37/44 contradictory source numerals.
5. Eventually preregister/blind human testing only after source versions frozen; no predictive-validity claim yet.

## Reproducibility / status

```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_c25_*.py' -v
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**Verified C25 complete historical-source regression: 238/238 PASSED, exit 0**, on the isolated C25 worktree (228 preserved C24 tests + 10 new). This is source metadata/layout arithmetic, not validation of astrology in people. No engineering-green proxies count as human prospective validation (**zero**).

**Stop admission:** Parent research OPEN; specific result (new base Vienna original photo) achieved; next action source Greek meaning/planet reading, executable with existing original photo and public critical scholarship. An unavailable or unread Greek lemma is a bounded source uncertainty, not owner-decision gate. Keep writing on isolated worker branch with provenance and do not redefine original owner's goal.
