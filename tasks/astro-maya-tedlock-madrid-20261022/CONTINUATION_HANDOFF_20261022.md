# Continued Maya reading: source audit and calendrical anchors (2026-10-22)

## Parent outcome and snapshot
Original owner task: continue researching the astrology systems in their actual original books; develop a source-to-claim-to-question map to empirically compare their independently calculated birth-derived predictions against untouched consenting humans, not only accumulate annotations.

**Parent outcome OPEN.** This batch is a **source-reading/reproducibility increment**, not a complete preregistered Maya predictor or demonstrated human validation.

Previous accepted integration: `research/astro-maya-cross-tradition-integration-20261022`, accepted head `64378021da0763cbb7c6792ab2dd63436444ff56`, 16 mapped family classes, 37 passing source/algorithm tests, no blinded human evidence.

Current new isolated sparse worktree (owner laptop): `/mnt/hdd/var/tmp/humandesign-maya-tedlock-madrid-20261022`; branch `research/astro-maya-tedlock-madrid-witness-20261022`. Source originals on owner device in `~/Documents/astrology`; **do not copy copyrighted full books, private participants or personally identifying birth data into this public repository**.

## Delivered in this increment

1. `docs/astrology-research-map/MAYA_TEDLOCK_MADRID_FIRST_CALENDAR_ANCHOR_AUDIT_20261022.md`: a page-anchored, readable report from Tedlock printed pp. 94–100, 107–126, plus selected *Madrid Codex: New Approaches* sections.
2. `docs/astrology-research-map/MAYA_TEDLOCK_MADRID_SOURCE_WITNESSES_V1.json`: authenticated owner book SHA-256, dated historical Momostenango day reports (1975-06-22=9 Akabal; 1977-03-02=4 Ik; 1977-03-15=4 Tziquin), Gregorian-date-only GMT 584283 **3/3 matches** vs GMT 584285 **0/3**, interpretive exceptions and unreconciled birth day-boundary.
3. `docs/astrology-research-map/test_maya_tedlock_madrid_anchor.py`: 9 additional source/engine scope and sensitivity tests. Complete affected map tests: **46/46 pass** on current laptop worktree, including pre-existing 37/37.
4. Canonical map README and owner book guide updated with **links** to this latest **partial-book** reading. Single original Mermaid map, other traditions' source records and all previous SHA-pinned reconciliation records untouched.
5. **Explicitly unscored preregistration draft `MAYA-MOMO-NOJ-DIVERGENT-THINKING-DRAFT-01`** from Tedlock printed p. 122, hypothesizing higher masked-rater novel problem-solving task performance for Noj-born adults than non-Noj matched comparisons. This task is a development interpretation of historically reported birth-day disposition, **not a validated claim**.

Key source separation: Komon Tohil/Zunil source E birth “good travelers” is not the same as Tedlock/Momostenango E birth ritual professions. Vail's Madrid calendar/almanac findings and Pohl's Borgia/Nahua-Mixtec marriage prognostics are not automatically Maya natal rules.

## Next authorized actions, still open

- Build contemporary birth-specific civil-date-to-Chol-Q'ij day boundary / clock policy from practitioner-anchored records (or abstain when unverified); the three historical Momostenango field dates do **not** prove all present-day K'iche' traditions have the same day boundary.
- Finish Tedlock's context-specific numeral/Noj day passages and compare distinct communities without conflating ritual divination with natal trait claims. Continue original Madrid codex folios/source reading separately.
- Seek independent content-validity review for the Noj-to-divergent-thinking translation, fix one task rubric with native language and education controls, cohort and power, matched temporal decoys/permutations, non-astrology baseline and complete explicit failure criteria.
- Only after those gates are met, freeze a model/questionnaire/calendar commit and predictions **before** untouched, consenting human responses; keep previously answered owner/friend data out of confirmatory test.

## Status
No production scoring changes, no respondent data fetched or exported, no automatic model promotion. Blinded human forward/reverse success count **0**. Underlying empirical astrology hypothesis remains **unvalidated**.

### Reproduction
From a checkout of this isolated branch:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_*.py' -v
```
The printed primary-source page locators and SHA hashes allow checking against the **owner's own** books; this repository deliberately does not distribute the books.
