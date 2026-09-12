# Life Patterns human UI opaque source-ID defect — 2026-09-09

Status: blocking human-comprehension defect found by owner manual review before any qualifying independent human first pass.

## Observed defect

The recurrence-corrected plain/provenance UI correctly removed redundant support-citation questions, but the optional exception/counterevidence control still displayed an opaque internal source identifier such as `EP-002-SEG-01` as the human-facing choice label.

That identifier is only a stable machine provenance key:

- `EP-002` = internal episode identity;
- `SEG-01` = first exact source segment for that episode.

The human auditor does not need to interpret this identifier. Asking a human to choose an opaque provenance key adds avoidable cognitive load and invites bookkeeping mistakes.

## Correction

Presentation only:

- keep the exact source-segment ID unchanged as the hidden exported value;
- show `Exact quote` / `Exact quote 1`, `Exact quote 2`, etc. in the interface;
- show the actual quote text beside any multi-source support or optional counterevidence choice;
- do not expose the raw segment ID as the decision label.

For a single-source Yes response, support provenance remains auto-bound and no support decision is shown. The optional counterevidence control may still be useful if the same quote contains a genuine limitation, exception, or conflict, but the human sees the quote text rather than its internal key.

## Scientific boundary

This correction does not alter:

- private evidence bytes;
- selected 44 episode + 22 repeated-pattern units;
- task identities;
- source-segment IDs stored in exports;
- response schemas;
- recurrence semantics;
- blinding or chronology;
- any automated or target-model output.

No qualifying human annotation had been collected before this correction.
