# Interruption-safe B07ax Merchant Nativity source checkpoint — 2026-10-19

**Root user outcome: OPEN.** The owner requests continued original-source Lilly + Chinese astrological research, proper astronomical/calendar/chart calculations, and eventually independently blinded human forward/reverse predictions versus controls. Historical source annotation counts and reproducibility tests are **not** actual human predictive success.

## Exact current state

- Active source branch: `research/astro-b07ax-merchant-nativity-opening-20261019`.
- Latest canonical Lilly registry at the time of this draft: **12,870** accepted original historical annotations, latest batch **B07aw**, next source **R12871**, original first-edition 1647 printed folio742/PDF776, CHAP CLXXV `The NATIVITY of an English Merchant Astrologically handled`. Separately Ptolemy **1,066**.
- Chinese canonical V7 **355** historical source annotations (154 BaZi, 201 Zi Wei), independently preserved, not modified.
- Pre-existing B07ax **photo/temperament/dignity witness** `ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json` and original **Mercury antiscion edition conflict** `MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json` committed at parent `d126426ad13eeed4d56a6160295b300ffe7bec81`. Both first 1647 and independently typeset second 1659 printed Mercury antiscion **26°06′ Pisces**; arithmetic from the separately printed natal longitude gives **26°26′ Pisces**, a **20-arcminute source/formula discrepancy**. Preserve printed value and derived mathematical diagnostic separately; zero actual event confirmations.
- Unaccepted B07ax candidates: `MERCHANT_NATIVITY_SOURCE_CANDIDATES_V1.json` proposes **30** source-only historical notes **R12871–R12900**. `build_b07ax_source_rules.py` produces provisional `RULES.json`, `ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json`, and `ACCEPTANCE.json`. **47 focused original photo, source arithmetic, and no-promotion tests pass.** Portable ZIP independent extraction, CRC/member SHA/bytes and guarded canonical index admission remain PENDING. **Do not count these as accepted yet.**
- Last candidate boundary R12900 is a source boundary only: physically distinct next printed **CLXXVI Of the Manners of the Native**, starting first-edition printed folio745 / PDF779 on the same page; proposed next source **R12901**, new chapter's body.
- Another distinct worktree/branch `research/astro-b07ax-merchant-nativity-chart-20261019` includes older photographic checkpoint and is **not** the current canonical/working source branch. Do not overwrite or duplicate its evidence. No concurrent source mutation process observed on the current branch at checkpoint.

## Interpretation/limits

The Merchant is an already known acquaintance of Lilly and the case contains historical temperament/humor and planetary fortitude/debility tabulations. These are unblinded historical printed claims; they are **not** demonstrations of genuine predictive success or personality/medical inference for current people. The 1647 original and separately typeset 1659 book are two witnesses to the *same* text, not independent human prediction samples. Original chart computed against historical epoch ephemeris remains unverified.

## Next executable safe action (do this without asking owner)

1. COMPLETED: validate pre-registered photo/source hashes and proposed RIDs with `python3 tasks/astro-source-audit-multipass-20261005/batches/B07ax/build_b07ax_source_rules.py`, then create **focused source/case and no-promotion tests**.
2. Add portable ZIP with CRC, exact member SHA/bytes, independently extracted test replay and evidence receipts; retain original source photographs and derived diagnostic.
3. Only when source-only checks pass, guarded append-only update canonical Lilly index from 12,870 to **12,900** (30 new notes, Ptolemy 1,066), ensure parallel Chinese V7 remains 355 and source next is **R12901**, physical CLXXVI. Keep zero independent real-human forecasts and runtime model promotion.
4. Commit and push with exact remote SHA readback; update handoff and checkpoint. Then continue the actual first-edition Manners chapter and the parallel Zi Wei ZWD-R0202 / BaZi BZI-R0155 research. Full astrology scientific empirical goal remains OPEN.

The current commit is deliberately labeled **WIP / unaccepted source candidates**, so an interrupted session can recover complete draft evidence without conflating staged notes with canonical acceptance.
