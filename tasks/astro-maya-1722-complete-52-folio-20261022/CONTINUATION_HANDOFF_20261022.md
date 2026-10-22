# Maya 1722 original manuscript completed 52-group label collation — B05 handoff

**Date:** 2026-10-22. **Parent user goal OPEN:** substantively read astrology original sources across schools and turn the ones that actually make source-grounded natal claims into reproducible, pre-frozen, blinding-safe predictions, tested on untouched consenting humans against decoys and nonastrology baselines. Source transcription/engineering tests are **not the human validation**.

## Resume identity and completed baseline

Owner-local laptop sparse Git worktree: `/mnt/hdd/var/tmp/humandesign-maya-sunset-and-natal-20261022`, research branch `research/astro-maya-1722-complete-52-folio-audit-20261022` forked from accepted B04 source branch `research/astro-maya-1722-primary-folio-collation-20261022` commit `0bf5f4345a40d296adbe07b6813f79254d393bfa`. Historical baseline source map covers **16** tradition/source families with one canonical Mermaid workflow; prior source files and HD production scoring untouched.

**Before this B05 pass**, B04's source audit checked 26 archival image SHA witnesses, 30 original date-row examples and **13/52** handwritten number/day-name groups from FAMSI Berendt copy. All that work remains committed/pushed and earlier packet remains in owner's `~/Téléchargements`.

## Work performed in B05

1. Visually inspected the original manuscript's missing folios `body0027` through `body0034`, including `body0026` and `body0035` boundaries. Existing B04 source photos for some folios were reused; no old successful reading was redone.
2. Manually transcribed group ordinals **14–52**, their coefficients 1–13, and the original five-name order from photographed folios 26–35 into `docs/astrology-research-map/MAYA_1722_B05_DIRECT_FOLIO_GROUPS_14_TO_52.txt`. First 13 rows and previous SHA in B04 ledger are left immutable.
3. Recorded original FAMSI photo SHA256/byte-size for folios 27–35 in `MAYA_1722_B05_FACSIMILE_PHOTO_SHA256.txt`, with overlap hashes for folios 30 and 35 matching the B04 original register. **Original source image bytes NOT committed to public Git.**
4. A full source-vs-independent algorithm comparison found **52/52** direct-manuscript group matches, **260 unique ordered (coefficient, day-name) entries**, four five-name units per manuscript folio 23–35. **This removes the 39/52 source-coverage gap**. The number 52 and completeness now have *physical photographic* support, not only algebraic extrapolation.
5. Source-exception: group **23** on `body0028` shows numbered signs but no clearly visible phrase in right-hand column of the digitized copy. Mark it absent/uncertain; no interpolated translation. All other original K'iche' augury prose remains untranslated/unclassified as natal vs omen/ritual. `body0036` starts a different prayer-like section; `body0037` notes `De otra mano`.
6. Owner-readable report `MAYA_B05_FULL_52_1722_FOLIO_SOURCE_AUDIT_20261022.md` and top-of-map README / owner guide updated. [Original source](https://www.famsi.org/research/mltdp/item58/); actual artifact is an **1877 Berendt copy of a 1722 text**, not autograph.

**Tests:** B04 **96/96** plus B05 **11 new** complete-photo, source immutability, missing/duplicate and negative-mutation tests -> **107/107** `python3 -m unittest discover -s docs/astrology-research-map -p 'test_*.py' -v`. `git diff --check` and clean portable archive cold re-run/checks required before claiming release of this branch if not already verified.

## Scientific significance / limits

- The original `Ahilabalzih` table is **52 individual paragraphs each associated with five distinct numeral/day-name states**. It demonstrates a coherent period-260 almanac structure, **not** an independently translated, verified set of 52 natal psychological descriptions.
- Group intervals repeat at +52 days while numeral remains constant and day name advances by 12 (mod20). This creates an authentic **5×52** formal parallel to some ancient Dresden/Madrid calendars, not proof they contain the same semantic prediction or descend independently.
- The publisher-authorized introductory excerpt of Weeks/Sachse/Prager 2009 `Maya Daykeeping` provided 20 historical name correspondences, but its 1722 full translation (printed pp64–135) remains **unread**. Avoid forcing meanings onto the source.
- A different source class reports early social naming of children from birth-day signs, but it is not logically identical to these 1722 almanac phrases.
- Existing 2005 film-date conflict and 2019 yearbearer observations remain unresolved; no birth-clock policy has been promoted. No private respondent data inspected, **0 prospective human validations, 0 production natal runtime rule promotions**.

## Precise continuation, no previous-work repetition

1. If directly available, obtain a legal full or partial **critical English translation of the 1722 `Ahilabalzih` entries** (Weeks/Sachse/Prager pp64–135) and distinguish natal, horary, religious or omen claims. Original photos already read: **do not redo their number/name transcriptions** unless discrepancy arises.
2. Analyze whether the source offers any *specific, ethical person-level prediction* with a stable birth-time calculation and behavioral outcome. If not, mark Maya natal track as source-only and advance a mechanically mature other school toward a real blind pilot; **do not make 1722 textual translation an artificial blocker to other traditions**.
3. For Maya-only calendar uncertainty, seek accurate 2005 segment-level film metadata/local practice without choosing variants to maximize chart fit.
4. All subsequent work remains inside `humandesign` with a new isolated branch/commit and reproducible handoff. Do not overwite accepted earlier B04/B03 or original imagery.

**Stop status:** B05 source-image *number/group reading* complete 52/52; parent owner's scientific goal remains **OPEN** and source K'iche' group-meaning translation remains pending. Next unit of scientific progress must address semantic person-predicate scope or human blinded test, not another synthetic victory.
