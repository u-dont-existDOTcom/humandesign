# B02v continued original-source review — 2026-10-14

**Status: OPEN, unaccepted editorial source inventory; no new scientific validation.**
This file supplements `REVIEW_PROGRESS_20261014.md`, `WORKING_CHECKPOINT.md`, and the remote `HANDOFF_20261014.md`; their previous reports remain retained. All work lives in HumanDesign, not only ChatGPT. No cumulative accepted index is advanced here.

## Authority and recovered state

- William Lilly, *Christian Astrology* 1647, exact original PDF381/printed347 **below** the thief-house heading, through PDF400/printed366 **above** the Chapter LI horizontal divider. No Chapter LI text included. Original page rasters PDF381–400 and errata PDF888 are preserved separately from edited prose; original full scan declared SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.
- Accepted predecessor: B02u ends R2572, 2,572 Lilly documentary units, 1,066 retained Ptolemy, 3,638 combined. Provisional B02v: 402 source-text units R2573–R2974, 2,974 Lilly/4,040 combined **ONLY IF ACCEPTED**. ZERO B02v source units accepted. These records are not 402 individual people/cases/predictions.
- Seven local producer draft components were preserved; seven current corrected drafts feed `assemble_source_draft.py` to produce `RULES_DRAFT.json`. Producer output is not independent source testimony. The output status remains `PROVISIONAL_SOURCE_IMAGE_EDITORIAL_DRAFT_INDEPENDENT_REVIEW_PENDING`.
- This ChatGPT continuation inspected original images including PDF397 and independently examined the p399 vs p400 text **relative to the producer source draft**. This is source-image collation, **not** a separately instantiated blind independent model reviewer and not complete record-by-record adjudication of all 402 units.

## Confirmed additions beyond the earlier four corrections

- **PDF392/printed358, R2785**: Source prints lord of ascendant applying to **"the second"**, or lord of second applying to **"the Ascendant"**. The draft had silently made this aspect between two house *rulers*. Corrected the normalized statement to preserve original role labels. Ruler-vs-cusp interpretation retained unresolved (`U47`). Prior bytes preserved in `recovery/producer_p391_392_before_20261014_p358_review.json`.
- **PDF395/printed361, R2848**: Source first-offence clause uses Part of Fortune `⊗`, not indefinite "a Fortune". Corrected source subject and kept alternative seventh-lord and Jupiter branches separate (`U48`). Original before this edit in `recovery/producer_p393_395_before_20261014_p361_fortune_glyph.json`.
- **PDF396/printed362, R2873**: Source directs reader to consider several age methods and "pitch upon the greatest number", **not explicitly the majority/most-agreed testimony**. Corrected to source wording; whether maximum-age or consensus intended remains unresolved (`U49`). Pre-edit bytes retained in `recovery/producer_p396_397_before_20261014_p362_age_review.json`.
- **PDF399/printed365, R2940–R2945**: Major page-alignment error. Producer erroneously placed on p365 five claimed capture conditions whose texts actually appear in the **separate** p366 compact list, creating false page-level duplicates and losing the distinct p365 conditions. Original p365 lists seventh-lord contact with a retrograde planet; Moon separating from seventh lord to conjunction with first lord; the converse departure from conjunction to first lord toward seventh lord; Sun and Moon joined to seventh lord (some say beholding him suffices); seventh lord going to conjunction/combustion; and the obscure last angular conjunction/infortune-in-seventh branch. Replaced those SIX editorial records in `PRODUCER_SOURCE_DRAFT_P398_400.json` from original p365 image, with unresolved grammatical relations marked. Original producer bytes: `recovery/producer_p398_400_before_20261014_p365_capture_review.json`, SHA256 `db7505bcf5ff0ea149c876d7a6eedc460ca47c4f4620160f20dd91780335598e`. Page p366 standalone alternatives remain in R2965–R2973; claims of literal repetition were qualified (`U50`).
- **PDF400/printed366, R2958**: Elliptical trailing original phrase concerning seventh/eighth lords was kept unresolved. A conjunction partner or fully specified sufficiency condition must not be invented.
- Printed page360 line4 same-volume erratum remains unresolved at exact glyph/replacement level; body passage located on PDF394, but source has not authorized supplying a hypothetical new symbol.

## Checks and scientific boundary

- `python3 assemble_source_draft.py` completed after these edits with 402 provisional source units, covering PDF381–400; 2,572 accepted predecessor remains.
- `python3 test_b02v_staging.py` passed **18/18** after p399 corrections (source staging only).
- `python3 independent_review/test_reconciled_draft.py` passed **12/12** after the p392 repair and before the p395/p396/p399 changes; later invocation was tool-blocked, not a pass. A separate attempt to extend this suite with p399-specific regression assertions was also refused by a tool safety check and was **not** retried through disguised edits.
- `git diff --check` produced no whitespace errors, and `python3 -m json.tool UNRESOLVED_DRAFT.json` parsed the current 50-entry issue ledger.
- No source-completeness acceptance, ZIP release, extracted archive replay, canonical research-branch publication, owner OS Downloads final delivery, participant/model change, empirical prediction, forensic inference, clinical claim, or historical outcome verification has been established in this continuation.

## Resume without repeating completed work

Preserve local corrected source drafts, exact original backups and 50 issues. Re-check currently unadjudicated or ambiguous planet/house/angle operators page-by-page on original images, now emphasizing PDF389–394 and PDF397–400 and p360 erratum; verify whether every distinct source condition is represented and no source statement has been duplicated or attributed to the wrong page. Use a genuinely separate image-first reviewer if authorized and actually available; incomplete prior Claude/Codex reader logs are NOT reviewer verdicts. Then perform source-only integrity tests, complete archive ZIP/hash/CRC/extract/replay, source+canonical branch non-force publication and exact remote readback, and owner Downloads deliverable SHA256 checks. Chapter LI starts PDF400 **below** divider only after Chapter L is accepted.

Research aim remains historical documentary source extraction. Lilly's statements about theft, guilt, appearance, sex, age, and capture are not validated facts or an acceptable means of identifying or investigating real people.
