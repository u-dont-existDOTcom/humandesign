# Continuation checkpoint — Brahe and Placidus primary text

Date: 2026-10-24. Root user goal OPEN: reconstruct multiple astrological calculation systems accurately, freeze competing historical rule packages, and eventually test their predictions on untouched blinded human data. This pass advances historical source labeling and interpretation, not predictive performance.

## New source frontier / supported claims

Brahe De Nova Stella (1573), Latin contemporary prose in Dreyer critical transcription, folio G1r-G1v: genuine varying DAILY motion in Sun/other planet directions, corresponding equatorial interval per symbolic year in natal context. In that same paragraph Brahe's meteorological daily-calendar technique instead invokes Moon movement. No inspected original phrase fixes local-true-midnight endpoints; retain later Gansten-informed reconstruction status.

Placidus de Titis as represented by Cooper edited English Primum Mobile (1814), printed pp.23-25, scan PDF pp.40-42:
 - theses 58,65: successive postnatal solar days' right-ascensional movement per year; method-level alignment with cumulative solar RA solver.
 - thesis 60: angles cannot be moved in converse.
 - theses 61,62: zodiacal rays excluded for converse; rays are in mundo.
These limitations are historically edition-specific; the original Latin 1657 is located bibliographically but corresponding pages were NOT read in this pass. The original public-domain 1814 full PDF was saved outside Git under user's books/astro folder; only the three selected source page screenshots and SHA-provenance were committed.

## Engineering change

New source_witness_scope.py supplies evidence-applicability status: compatible selected rule, partial source support, incompatible with Cooper's witness, or not established. Solar key JSON adds primary_source_scope metadata and corrects prior mistaken "Brahe original unread" note. Old mathematical routines, historical Lilly tables, geometry variants, and production scoring remain unchanged.

A generic role-reversed zodiacal promissor ray remains calculable; it MUST NOT be advertised as Placidus's historical converse rule based on Cooper. The record is a warning for future frozen author-labeled tests, not a new user-facing lock or conjectural universal restriction.

Tests: 94 prior/new checks PASS on synthetic/strict SWIEPH inputs. Frozen Brahe 126-contact and Placidus 114-contact examples compare exact numerical contacts and coverage before versus after; only metadata changes. Two source records and selected page hashes are independently verified. Ruff and mypy checks documented in VERIFICATION.json.

## Open research

1. Resolve original Latin 1657 first edition thesis 58–65 against Cooper's edited translation.
2. Independently inspect 1573 Brahe first-edition folio rather than relying only on critical edited transcription.
3. Finish remaining exact original 1647 Lilly minute/day/hour cell collation and any mathematical edge-case source variants.
4. Keep historically permissible method choices predeclared. Do not select them by matching real known life events or count label-swapped equivalent rotations as independent successes.
5. Ultimately complete combined prospective forward-blind astrology comparisons after model mappings/prediction statements are frozen.

Research branch: research/gansten-solar-primary-source-20261024; parent branch: research/gansten-solar-brahe-placidus-20261024. Separate research-only module; no production promotion.
