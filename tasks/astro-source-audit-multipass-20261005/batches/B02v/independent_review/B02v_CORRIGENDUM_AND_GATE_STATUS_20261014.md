# B02v — Source corrigendum and recovery gates (2026-10-14)

**State: OPEN / UNACCEPTED.** Parent goal: documentary source-complete study of the historical astrology corpus, with source intake always distinguished from empirical predictive evidence.

## Accepted and draft boundaries

Latest GitHub canonical source index was fetched in this continuation: **2,572 accepted Lilly source units** (B02u ending R2572), **1,066 retained Ptolemy**, **3,638 combined**. The next accepted source text still starts original Lilly PDF381/printed347 below `Of the house of the Thiefe, and the mark thereof`. No new B02v records are accepted or promoted.

B02v has a **402-unit candidate** R2573–R2974 drawn from original PDF381–400, STOPPING ABOVE the Chapter LI divider on original PDF400. Last corrected local source review retained **51 textual uncertainties**. The two p399/400 capture-rule lists are now correctly distinguished (see prior `REVIEW_CONTINUATION_20261014.md`). Source records are not observed people or independent events.

## New image-verified source correction — R2699, original PDF388/printed354

Original original-page image `evidence/pdf-388.png` was read directly. In the Moon-in-tenth description of a house entrance it prints **“as a Furnace or Querne, or such like”** (literal source witness). The producer's `tenth_moon_underground_oven` paraphrase incorrectly substituted **oven** for **quern**, a hand-operated grain mill. The original printed object is not an oven.

Actual correction in local `PRODUCER_SOURCE_DRAFT_P388_390.json`:
- Kind becomes `tenth_moon_underground_quern`.
- Text retains the house-entrance context and an underground doorway or frequently used household feature, including **furnace or quern**.
- Added original short anchor, revised preconditions, and uncertainty record `U51`.
- Before-edit source frozen byte-for-byte: `recovery/producer_p388_390_before_20261014_quern_review.json`, SHA256 `8f629a70b9b693a26928e1c77fb0b41990ab19b2f69c59019771b7fa68e6ea10`.
- Corrected local producer SHA256 `fce4b68c4397e1e27b8c9ca6278a65143a56bb17bc15e95388865253bad3f04d`.
- Producer edit succeeded; uncertainty ledger now **51**. The cumulative generated `RULES_DRAFT.json` is **stale**: assembler invocation was blocked by a tool safety check, so it still holds the obsolete `tenth_moon_underground_oven`. Do not read the current compiled draft as latest source truth.

## Test and packet integrity boundary

Before R2699 was corrected, a **v1 provisional ZIP** was actually built, extracted, CRC-tested, SHA256-checked, and copied byte-identically to the OS-designated Downloads folder:
`/mnt/hdd/home/joel/Téléchargements/Astrology-Lilly-B02v-Provisional-Source-Packet-20261014.zip`.

Its historical SHA256 is `7f27edfd05f8bb6ce59361d565cfc0ffa0778237d6149415bbbca7de7ff6f5cc`; 81 files including 21 original source images; three extracted source-only suites passed **18 + 20 + 12 = 50** before U51. This ZIP is now **SUPERSEDED AS A CURRENT DRAFT**, but remains immutable evidence of the earlier snapshot and pass status. It was always marked UNACCEPTED, not a final source-fidelity or predictive result.

Current tests:
- `test_source_integrity_v2.py` preserves the original **50-issue V2 fixture**; its fixed count is obsolete for the corrected 51-issue draft. A surgical edit to this test was denied by tool safety checks; do not report it as a pass.
- Added `test_source_integrity_v3.py`, explicitly covering R2699, original backup hash, U51, p399 repairs, and preserved accepted index. Executed **12 tests, 11 pass and 1 expected FAIL** on compiled R2699 because compilation is blocked/stale. This is an **open source-consistency failure**.
- The earlier 18/18 staging, 12/12 reconciliation and 20/20 V2 results apply to **the earlier uncorrected snapshot**, not the latest local source state. A successful old archive does not validate a newly edited source packet.
- No new current ZIP or owner deliverable has been verified after U51.

## Local Git conflict / independent review limitations

Two safe local Git commits (`b379881`, `98a5ac8`) contain all earlier producer/review content. Attempting to merge remote source-ref updates hit **one add/add conflict** at `PRODUCER_SOURCE_DRAFT_P381_384.json` (local source-corrected versus remote older). Local working copy has the corrected original-byte hash `bf0c109f99e1801c851be90ca7b2e7d99c7b4ed2ec069c75c46ca8ad84da13dd`; the local branch still has a pending `MERGE_HEAD`. Multiple attempts to stage resolution or abort via the Desktop Commander transport were rejected by tool safety; do not bypass a safety refusal or claim clean Git/remote publication. GitHub research branch remains at its earlier remote checkpoint, with a published partial review report; the newer two local commits are **not remotely merged**.

A narrower separately instantiated Codex image-first p399 reading was attempted. First command could not start from deleted inherited CWD; second command waited for open STDIN, was terminated; input-closed retry encountered a tool safety block. **No independent final source-review output was produced**. Do not claim image-reader independence completed, or use partial logs as evidence.

## Exact next authorized work (not acceptance)

1. On a permitted safe tool route, reconcile the sole add/add Git conflict by verifying remote-original versus local-corrected content, preserve local corrected R2576/2577, and commit without force/reset/owner-data loss. Separately verify what was actually published.
2. Rerun `assemble_source_draft.py` after the R2699 quern change; rebuild counts/coverage, verify R2699 and all 402 record identities, and adjust only current staging tests to 51 issues while retaining historical V2 receipts.
3. Finish image-first line-level comparison of all 20 source pages, with explicit undeciphered glyphs and 36 direction-table rows; obtain genuinely separated review if available rather than accepting model self-review as independence.
4. Run the current source-only suite, and only after semantic source fidelity is admitted, prepare definitive acceptance ZIP, manifest, CRC/sha checks, extraction/test replay; publish non-force to source+canonical research branches and match owner Downloads destination bytes.
5. Preserve all participants, chart model versions, forecasts and blind validations. The historical source claims are not an acceptable method to identify any real offender, property location or personal characteristic.

**No new owner choice has arisen.** The remaining blocker is tool-specific safety/admission plus unfinished source review, not a missing research authorization.
