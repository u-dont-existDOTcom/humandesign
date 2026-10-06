# Current astrology source audit

**Parent: OPEN, owner-authorized multi-pass source audit.** Latest completed unit: Ptolemy *Tetrabiblos*, Robbins translation 1940 / supplied 1964 reprint, English Book I chapters 1–16. No person predictions or runtime-model promotion.

## Recovery entry points
- `tasks/astro-source-audit-multipass-20261005/CURRENT_PASS.json` — last verified unit and next range.
- `tasks/astro-source-audit-multipass-20261005/PASS_PLAN.json` — five audit passes and source tracks.
- `tasks/astro-source-audit-multipass-20261005/DRIVE_INTAKE.json` — preserved historical13-file intake.
- `tasks/astro-source-audit-multipass-20261005/SOURCE_WITNESS_UPDATES_20261006.json` — controlling source-witness update for the replacement Rhetorius; use together with the historical intake.
- `tasks/astro-source-audit-multipass-20261005/SECTION_DISCOVERY.json` — 61 Ptolemy sections; 16 read, 45 unread.
- `tasks/astro-source-audit-multipass-20261005/batches/B01/RULES.json` — unchanged 24 source records, I.1–I.8.
- `tasks/astro-source-audit-multipass-20261005/batches/B01b/RULES.json` — 32 additional records, I.9–I.16.
- `tasks/astro-source-audit-multipass-20261005/batches/B01b/FIXED_STAR_TABLE.json` — complete 95 descriptive star/asterism groups in I.9, with weaker-analogue qualifiers and translator notes separated.
- `tasks/astro-source-audit-multipass-20261005/batches/B01b/READING_RECEIPT.json` — exact English scope, page boundaries, note checks and exclusions.

## Completed and not to repeat
All 13 original private sources were hash-verified. B01 and B01b now total 56 source records plus 95 star-table entries. The entries are not independent statistical predictions. There are 49 isolated definition tests (18 prior + 31 new); run the recorded broader regression suite at integration.

The replacement Rhetorius is an image-only 198-page file, not the 150-page truncated Files preview. Its copyright page identifies2009 / fourth translation edition/first published edition, not filename 2005. Visual footer mapping found193of 222numbered pages. Six gaps were recovered from the old preview into a private supplement, with 6/6 render matches; combined coverage is199/222, leaving 23 absent. The old preview and its 151-placeholder detection remain unchanged historical evidence. See `RHETORIUS_REPLACEMENT_AUDIT_20261006.json` and `RHETORIUS_SIX_PAGE_RECOVERY.json`. The replacement plus supplement has continuous printed pages1–103; whole-book completeness is not claimed.

Other source limitations remain: BPHS is Sharma, not Santhanam; the primary-directions source is an excerpt/interview, not the complete requested book. The owner could not obtain further books. These gaps do not block available reading batches.

## Next executable batch
**B01c: Ptolemy I.17–I.24.** Begin at the I.17 heading on English PDF103 / printed79; verify all table/section boundaries and stop before BookII. Topics: planetary houses/domiciles, triangles, exaltations, alternative terms, places/degrees, faces/chariots, applications/separations and related powers. Preserve alternative tables and translator qualifications; do not choose variants to fit known people.

## Important unresolved findings from B01b
The fixed-star catalogue has no admitted natal trigger/orb/epoch bridge yet. Keep constellation figures distinct from tropical signs, and group membership distinct from identifying an entire group with its brightest star. I.13 classifies opposition as disharmonious while its polarity explanation is in tension with I.12 under a gender-parity reading; retain the explanation as unresolved rather than silently correcting it. Robbins’s explicit I.14 and I.15 pair tables are source-specific and must not be replaced with modern reflection formulae. Seasonal hours are day-or-night duration divided by 12, not automatically 60 minutes.

## Invariants
Use live UDA/project authority and the V2 source-audit procedure. Preserve source/translator/project layers, complete conditional qualifications, unknown states, and old candidate/model freezes. Raw books, supplements and full extracted text stay outside Git. This is source audit, not a person-reading receipt. No background work is running. A completed chapter batch does not complete the book, corpus, implementation or validation.
