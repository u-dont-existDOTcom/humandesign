# B02l archive-part delivery preparation

## Handoff

`prepare_b02l_delivery.py` is a private, drop-in revision of the existing preparer. It accepts the same exact-commit argument and retains the original batch input and command-JSON output locations for root adoption. Only copies with private fixture locations were executed here.

Revised preparer SHA256: `624ac165f48566a8af170991da7a42b282b5872ceff7e57feee4694110d1ec5e`.

Original preparer SHA256, checked unchanged: `b851a42fd41d51753375dd8ea08cdcd9a8fe9277dfabfa90a0212e7de06efa40`.

## Changes

- An optional, nonempty `publication_parts` list selects archive reconstruction. Every part receives the normal B02l repository-path prefix. A reconstructed archive has no direct `repo_path` in the prepared specification.
- The generated command fetches each part from the supplied exact commit and verifies HTTP 200, byte count, SHA256, and Git blob SHA. It joins parts in their listed order and checks the complete archive's byte count, SHA256, and content-derived Git blob SHA before invoking the existing identical-or-new installer.
- Direct Markdown companions and the handoff continue through direct exact-commit downloads. Their receipt transport is `direct_http_file`.
- The archive receipt transport is `reconstructed_archive`. It lists ordered per-part HTTP and hash checks, reports `content_derived_git_blob_sha`, and explicitly sets `complete_archive_is_single_published_git_blob` to false. It makes no top-level archive HTTP-status or published-blob claim.
- The file installer, work-index insertion/locking/readback, and escape normalization blocks are byte-for-byte unchanged. Existing prior fixture evidence continues to cover their normal newline, preservation, and conflict behavior. Receipts omit private filesystem locators.

`PREPARER.diff` contains the exact source diff.

## Local execution diagnosis

Eight isolated transport fixture cases passed: a valid four-part ZIP join (including a repeat run), corrupted bytes, an HTTP-missing part, reordered valid parts, an omitted part descriptor, a truncated part, a wrong part Git blob SHA, and a wrong complete-archive content-derived Git SHA. Each failure left the archive uninstalled and work index unchanged, and emitted no completed-delivery receipt. The successful synthetic archive passed ZIP readback; its bytes matched the pre-split fixture exactly. The direct companions and handoff also completed within the successful fixture.

The generated Python compiled, retained the correct NUL/newline/regex values, prefixed each part correctly, and never requested the complete ZIP as a remote blob. `EXECUTION_DIAGNOSIS.json` records the checks and a clearly labeled synthetic success-receipt example. `exercise_parts.py` reproduces these local checks with all network calls replaced by fixture responses.

No live remote calls, owner delivery, archive rebuild, canonical-file edits, or Git writes occurred. These are transport fixtures only: zero tests were added to the 20 canonical source tests, and they create no additional source-review gate. The original accepted archive and frozen source-reader outputs were not written.
