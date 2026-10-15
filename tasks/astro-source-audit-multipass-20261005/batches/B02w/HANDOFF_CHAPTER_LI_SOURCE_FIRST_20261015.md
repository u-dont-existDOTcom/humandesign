# HumanDesign astrology source study — Chapter LI source-first handoff

**2026-10-15, Africa/Dakar (UTC+0). Current outcome: PARENT ASTROLOGY SOURCE STUDY OPEN. B02w PROVISIONAL; zero new source units accepted.**

## 1. Owner goal and governing instructions

Continue the original-text, multi-author astrology methodology audit until the requested corpus is studied, with source statements and empirical predictive validations kept **strictly separate**. Do not let engineering/provenance tests masquerade as accuracy, real human cases, or an independently certified reading. Keep all durable work in `u-dont-existDOTcom/humandesign`. Begin each future turn by fetching the live Universal Development Architecture `AGENTS.md` and `LESSON-INDEX.md`, then this repository's `AGENTS.md`, and obey live source provenance, publication and handoff rules.

The user repeatedly authorized continuation and specifically requested an updated handoff. No unresolved owner spending, privacy, model-routing or publication choice is needed for further source-first editorial work.

## 2. Verified accepted predecessor

**Chapter L has already been completed as HISTORICAL DOCUMENTARY SOURCE intake** (batch B02v) and non-force published in both the research source branch and canonical research index. The exact authenticated publication receipt is `batches/B02v/PUBLICATION_RECEIPT.json`. Canonical `tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json` now accepts **2,974 Lilly source units ending R2974**, including 402 from Chapter L, with **75 retained textual ambiguities**. Retained Ptolemy = **1,066**, combined accepted historical documentary units = **4,040**. The accepted source archive was delivered to owner Downloads as `Astrology-Lilly-Chapter-L-Documentary-Source-Acceptance-20261015.zip`, SHA256 `c0834a95b3d14eabcd8f8c67721f1c321bc80f61ae760188b2c4f585d1a577ec`. Full independent diplomatic transcription was NOT claimed; the unresolved original printed p360 line4 erratum remains in that batch's provenance.

These are documentary text units, not 4,040 empirically verified astrological predictions. No personal chart, participant responses, timing forecast, blind score or runtime model was changed.

## 3. New finite Chapter LI original-source window — established this turn

Primary source: original 1647 William Lilly *Christian Astrology*, Wellcome b30338724. Full original PDF SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`, size 141,842,963 bytes. Full PDF already exists on laptop in `batches/B02w/lilly-1647-b30338724-original.pdf`; not uploaded to Git or packed in the small ZIP. Source acquisition/hashing and initial PDF401–404 rendering were previously completed—do not redownload.

**Exact physical Chapter LI boundaries, confirmed from original images:**

- Opens on original **PDF400/printed366 BELOW** the horizontal divider after Chapter L's final capture clause. Heading `CHAP. LI. Of Battle, Warre, or other Contentions.`
- Continues on original **PDF401/printed367** and **PDF402/printed368**. The opening `De-fendant` word crosses PDF400→401; a separate `Wood or Stone` injury clause crosses PDF401→402.
- **Ends at the bottom of original PDF402/printed368 after the last opponent-death clause.**
- Original **PDF403/printed369 starts `CHAP. LII. Who shall doe best in a suit of Law.`** Chapter LII's BODY is not part of Chapter LI and must not be included in B02w.

The accepted B02v `evidence/pdf-400.png` was copied **byte-identically** into B02w `evidence/pdf-400.png` (SHA256 `c48dcf91952b83d9dfdc230fcc8205500993841cd6a461cdba17fb6a0ae11eab`). Original PNGs PDF401–403 retain their earlier byte hashes; supplemental PDF404 is preexisting next-chapter context. `SOURCE_WINDOW_MANIFEST.json` preserves all physical roles and image hashes; `RETAINED_LILLY_INDEX_BEFORE_B02w.json` freezes canonical B02v predecessor.

## 4. Concrete source extraction completed

Read the three original Chapter LI printed pages in source order and created `SOURCE_FIRST_CLAUSES_DRAFT.json` with **42 provisional editorial documentary units R2975–R3016**, comprising **41 Chapter LI heading/claim/conditional units and one Chapter LII navigation-only boundary**. These are NOT accepted. The source-first draft has short **editorially normalized anchors**, source page/printed-page locators, distinct conjunctive/alternative branches, explicit preconditions (30 kinds), qualifications, documentary-only flags, and original-image authority. `assemble_li_initial.py` deterministically regenerates:

- `RULES_DRAFT.json` — 42 contiguous provisional source units, no empirical cases or runtime promotions.
- `SOURCE_WINDOW_MANIFEST.json` — original pages 400–403 with verified hashes and next-chapter exclusion.
- `SOURCE_ORDER_DRAFT.json` — print order, exactly two cross-page records R2978 and R2999.
- `UNRESOLVED_DRAFT.json` — **11 retained uncertainties** LI-U01–LI-U11, especially abbreviated converses, compound aspects/benefic-malefic alternatives, printed node-like glyph scope, the elliptical `and so of the tenth and seventh`, and the `fortune of the Actors` referent.

`recovery/SOURCE_FIRST_CLAUSES_before_precondition_annotation_20261015.json` is the exact before-edit source version (SHA256 `4cb34d982f927866892d52b5b6dcc1218cc1269b33cbe2b10871104ca9bbc1f7`). `annotate_li_preconditions.py` adds the explicit Boolean and directed-application predicates, preserving the earlier original producer bytes. The detailed paragraph-by-paragraph source distinctions and limitations are in `LI_SOURCE_FIRST_INVENTORY_NOTES_20261015.md`.

**Important:** Abbreviated `& e contra` appears SIX times and is intentionally NOT silently expanded to a particular executable reverse pattern. Statements predicting victory, safe return, injury, death or legal success are **historical textual assertions only**, not validated cases, actionable danger estimates or forensic evidence.

## 5. Verification and owner delivery

`test_b02w_staging.py` passed **16/16 source-only tests** on the source draft. These check original page SHA256, prior accepted index, page boundary, printed-page locators, contiguous IDs, 42 unique kinds, both real cross-page clauses, original alternative/AND operators, no expansion of converse syntax, and absence of empirical/runtime promotion. The previous `verify_source_opening.py` also passed on the laptop and verified four original PNGs PDF401–404 plus the full original PDF SHA256.

A distinct **UNACCEPTED B02w source-first ZIP** was created by `build_b02w_provisional_packet.py`; it is **not** the accepted Chapter L archive and **not** a source-acceptance release.

- Filename: `Astrology-Lilly-Chapter-LI-Source-First-Provisional-20261015.zip`
- **21 file payloads**, **9,038,925 bytes**
- SHA256: **`fcf6ec2942d3f3d429bc96548107630bb2f76a4eee29bbf4d973b79686e45c7f`**
- Owner's actual Downloads path: `/mnt/hdd/home/joel/Téléchargements/Astrology-Lilly-Chapter-LI-Source-First-Provisional-20261015.zip`.
- ZIP CRC, each member's SHA256, actual extraction into fresh temporary directory, and the **extracted copy's 16/16 staging tests** passed. Owner Downloads bytes match archive SHA256.
- Machine verification: `SOURCE_FIRST_PROVISIONAL_PACKET_RECEIPT_20261015.json` (generated only on success).
- The original 141MB PDF is intentionally NOT in the ZIP; archived original-page PNGs, hashes and source-first editorial files are sufficient for a bounded handoff.

## 6. Remaining substantive work and exact next commands

**The root astrology source study remains OPEN.** Chapter LI's physical extent is known and a source-first draft now exists, but a complete source-to-record omission/fidelity audit and acceptance for this chapter have NOT been established. User has authorized continuing automatically. Next worker should:

1. Verify live HumanDesign Git branch and checkpoint, including this handoff and the latest remote publication receipt. Respect branch ancestry, preserve unrelated work and do not rerun prior successful download or archive-build commands.
2. Independently re-read original **PDF400 only below divider, PDF401 and PDF402** against all 42 draft units, starting from the original paragraphs; check for any omitted conjunction/disjunction, source-heading/margin condition, aspect direction, exception or countervailing clause. Confirm Chapter LII first heading on PDF403 remains boundary ONLY. Give special attention to p401 compound safe-return conditions and p402 financial-gain/reconciliation alternatives and the two separate death clauses.
3. Preserve exact before-edit producer bytes before changing any source material. Resolve/reclassify the 11 uncertainties only with original text evidence; record irresolvable glyph/early-modern syntax honestly. Avoid inventing inverse rules from `e contra`.
4. Regenerate draft/manifest, run focused source tests and add a reverse original→record coverage check. **Only if Chapter LI is demonstrably complete at the established documentary standard** build an acceptance packet, perform CRC/per-file hash checks and actual extracted test replay, update canonical Lilly index non-force after source admission, and verify remote readback plus owner Downloads bytes.
5. Begin Chapter **LII on original PDF403/printed369** only once LI documentary acceptance is complete; then continue the parent multi-author astrology original-text corpus lane.

**Current last accepted Lilly remains R2974 / 2,974; retained Ptolemy 1,066; combined 4,040.** If and only if all 42 provisional B02w units are later accepted without count revision, proposed Lilly would be R3016/3,016 and combined 4,082—these figures are not current accepted totals.

**Resume instruction:** Verify publication of this handoff, open `LI_SOURCE_FIRST_INVENTORY_NOTES_20261015.md` and `SOURCE_FIRST_CLAUSES_DRAFT.json`, then compare original images PDF400–402 clause by clause before advancing acceptance. No new owner decision is outstanding.
