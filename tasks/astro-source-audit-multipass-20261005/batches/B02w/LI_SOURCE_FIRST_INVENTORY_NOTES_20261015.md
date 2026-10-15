# Lilly Book II, Chapter LI — original-source first inventory

**2026-10-15, Africa/Dakar (UTC+0). Status: PROVISIONAL HISTORICAL SOURCE ONLY, NOT ACCEPTED.**

## Original witness and exact finite scope

William Lilly, *Christian Astrology* (1647), original Wellcome b30338724, **full PDF SHA256** `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`. Locally verified full original PDF: 141,842,963 bytes; not placed into Git or the small review packet. Original rendered source images `evidence/pdf-400.png` (copied byte-identically from accepted B02v), `pdf-401.png`, `pdf-402.png`, and boundary `pdf-403.png` are SHA256-verified in `SOURCE_WINDOW_MANIFEST.json`.

**The Chapter LI boundary is now resolved.** It starts *below* the printed horizontal divider near the bottom of **original PDF400/printed366** (after Chapter L), continues **PDF401/printed367** and **PDF402/printed368**, and **ends after the last opponent-death clause at the bottom of printed368**. The first words on PDF403/printed369 are **`CHAP. LII. Who shall doe best in a suit of Law`**, followed by Chapter LII body, which is **not Chapter LI**.

This means full Chapter LI has a finite original-source window of part of one page plus two complete pages; the opening PDF400/401 word `De-fendant` and the injury PDF401/402 phrase `Wood or Stone` are actual sentence continuations, not independent rules. The Chapter LII heading is recorded only as a final navigation boundary. Do not import Chapter LII legal-suit content into LI.

## First pass extracted in source order

`SOURCE_FIRST_CLAUSES_DRAFT.json` contains **42 source-grounded editorial units** R2975–R3016, assembled in `RULES_DRAFT.json`. This includes Chapter LI headings, scope statements, local house/planet assignments, condition–consequence branches, printed margin instructions, five literal abbreviated `& e contra` clauses plus one differently worded `the contrary noteth the contrary` converse clause, and the one Chapter LII navigation boundary. There are **41 LI heading/condition units** and **one LII boundary unit**. This count measures documentary annotations, NOT independent cases or predictions.

The source-first reading maintains four logically distinct subsections:

1. **Whether the querent overcomes an adversary:** assign ascendant lord, Moon and the planet from which Moon separated to querent; assign seventh house/lord and the planet to which Moon applies to defendant. Compare angular strength, dignity and associated benefics. Preserve two opposing benefic/malefic side conditions, seventh lord in ascendant, and both abbreviated `e contra` variants without inventing full inverses.
2. **Whether one returns safely from war or dangerous voyage:** distinguish well-disposed strong ascendant lord with a favorable planet, the contrary, favorable seventh lord despite weaker ascendant lord with losses, Moon applications, eighth-house malefics, Saturn bruises and Mars/printed node-like glyph weapon dangers. These are historical assertions, not clinical risk evidence.
3. **Further safe-return clauses:** first lord with benefic or benefic in first is a positive alternative; Sun with first lord is independently adverse because the author interprets combustion; seventh-benefic versus first-malefic gives impediment *without death*; malefic with first lord alongside benefic first gives losses/wounds but likewise *not death*. Saturn first or with first lord gives adverse travel counsel; Saturn/malefic combinations and the compound first/dragon-node/eighth clauses give distinct alleged injury/death alternatives. Preserve the PDF401→402 sentence boundary.
4. **What ensues of the war:** locally reassign first/querent versus seventh/opponent, then retain the strong/weak converse configurations, the compounded BOTH-lords-in-first with benefic aspects to the **cusp** of second, the outcome alternatives of victory/financial gains/**or reconciliation**, the separate both-sides-loss result, and two adverse death clauses by first/eighth and seventh/second rulers. The original margin gives houses 10,11,12,1,2,3 to querent's side and houses 9,8,7,6,5,4 to the opponent's side; these are source-authored marginal classification rules, not measured outcomes.

Each normalized condition has `source_locator.pdf_pages`, printed-page mapping, editorial short anchor, source-paraphrase statement, explicit preconditions for compound source conditions, and retained uncertainties. **Do not turn abbreviated `e contra` or elliptical `and so of the tenth and seventh` into fully specified computational tests.** The first-pass finite window and source operators were directly examined on original image scans, but this is **same-context editorial inspection, not a blinded independent/diplomatic word-for-word audit**.

## Preserved uncertainties and testing

`UNRESOLVED_DRAFT.json` retains **11 specific source/interpretation limitations**, including abbreviated converses, hard-to-parse aspect grouping, planetary glyph scope, the ambiguous meaning of `Actors`, and Chapter LII physical boundary. An exact snapshot of the initial source-first clauses was saved under `recovery/SOURCE_FIRST_CLAUSES_before_precondition_annotation_20261015.json` before 30 explicit precondition fields were added. `assemble_li_initial.py` rebuilds the source draft, source-order and image manifest deterministically from the saved source inventory.

The current canonical predecessor has **2,974 accepted Lilly historical-documentary records through R2974 (Chapter L/B02v)** and **1,066 retained Ptolemy** = **4,040 accepted documentary source records combined**. The proposed B02w R2975–R3016 would move Lilly to 3,016 and combined to 4,082 **only if source-only acceptance later occurs**; these hypothetical values are NOT accepted totals. At current stage `RULES_DRAFT.json` explicitly has `accepted=false`, `newly_accepted_documentary_records=0`, and all 42 records are `REFERENCE_ONLY_NOT_PROMOTED`.

All procedures are for historical source extraction. No claim that astrology predicts war, safe travel, injury, death, litigation, or real events is supported by this study.
