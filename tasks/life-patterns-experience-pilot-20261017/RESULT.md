# Survey-first continuation: delivered v1 experiment

**Task:** Continue Life Patterns survey improvement after the correction that historical astrology source study must not displace questionnaire design.
**2026-10-17. Status:** OFFLINE DEVELOPMENT PILOT READY; NOT LIVE/NOT SCORED.

## Source audit used for design (not fresh astrology research)

- The legacy V7 questionnaire comprises 79 scene/question routes, largely behavioral; the active tendency-first version has 25 self-report questions. They do not directly sample most of the owner's proposed first-person experiences.
- The previously recorded eight-item optional pilot was wording-oriented, not interactive. This iteration turns it into a usable optional questionnaire with explicit response semantics.
- The source-referenced astrology audit remains contextual only. No new tradition claim, rule, chart score, or historical extraction was introduced.

## What changed

- Eight versioned experience items: self-surprise, surprises about people/world, awe, abrupt insight, felt predictability, subjective guidance, meaningful coincidences, and personal meaning versus perceived impact on others.
- Four default prompts, followed by a menu of four participant-selected topics (not inferred from chart, belief, or earlier answers).
- Explicitly distinct NOT_ASKED, ANSWERED, NEVER, UNKNOWN, SKIPPED and ALREADY_COVERED. A direct previous-source reference is required for skipping an item as already covered. Responses never feed live/frozen chart scoring.
- Frequency and optional felt intensity, subjective appraisal and later revision are separate; personal meaning and perceived contribution receive **two fields** rather than a forced composite.
- Local-only, self-contained HTML with explicit opt-in, reversible edits, import/export, no network calls and no silent storage.
- A qualitative 29-domain broad experience ledger flags additional omissions (dreams, art/creativity, play, home/family identity, worldview/practice, turning points, cultural exploration). It does not force any of these into the present pilot.

## Risk and status

This is a single opt-in development candidate; there are no human psychometric results. The wording must be assessed for clarity, repeatability and distinctness before scoring any astrological prediction. Existing interviews and Railway production remain unchanged. No participant-specific private record is read for this change.

## Verification

- New and existing pilot structure tests: 10 passed.
- Playwright browser automation against local HTML: PASS, including explicit consent gate, four default questions, two selected optional topics, never/unknown states, two meaning fields, answer editing, file export and re-import, and an external-request error gate (zero network requests and zero JavaScript errors).
- 375 px mobile viewport: PASS (375 px document width, no horizontal overflow).
- Ruff for changed code: PASS.
- Full unit and participant-service suites: **1,289 passed, six unrelated astronomy fixture skips**, with the candidate source PYTHONPATH explicitly selected. The first broad attempt used the shared environment's editable install pointing at another worktree and failed collection; correcting that environment resolved the errors without changing source.

## Remaining owner-only actions

None for viewing or using this offline pilot. The unrelated private Custom GPT editor update to use already-live Railway v1.8 remains a separate human interface step, unchanged by this experiment.
