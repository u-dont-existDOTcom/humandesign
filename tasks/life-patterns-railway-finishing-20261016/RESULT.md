# Railway finish-page implementation — 2026-10-16

## Owner goal

A participant with an already completed Life Patterns GPT interview should finish in a secure Railway browser rather than continuing indefinite GPT round-trips. Preserve the original source, existing independent review, consent, and the required three-question CF003 follow-up. Do not restart or invent completeness.

## Implemented

- The existing Railway participant service gains `POST /api/gpt/reviews/{review_id}/finish-link`, an additive seventh GPT Action. The *existing* GPT Action Bearer credential is used only to issue a single-use, 20-minute link **after** that review is `ready` and unsubmitted. The link contains only a random opaque token in the URL fragment, no review ID, source, name, birth data, or Bearer secret.
- The link exchange is one-time in the same encrypted service's SQLite database, then a separate HttpOnly, SameSite Strict, Secure two-hour browser cookie represents the limited finishing session. All write endpoints require exact configured same-origin and rotating CSRF token. User can reopen the page during the private session without redeeming another link. Expiry and cross-session access fail closed.
- Mobile/desktop `/finish` page displays the independent neutral source-quoted evidence, conditions and missingness. Participant must explicitly confirm or return to the original GPT for correction/re-review; the browser does not invent or edit a behavioral answer. All source rendering uses text nodes, a restrictive content-security policy, and no external libraries.
- The final primary is reconstructed server-side from the **original exact candidate record** and actual saved admitted clarification history including skips. It is confirmed/frozen only on explicit participant action. The original V7 questionnaire, route mappings and existing full evidence admission are unchanged.
- Exactly three CF003 question wordings are loaded from the pinned separate module; original answers and nonbehavioral metadata are stored separately from primary. Existing `validate_gpt_submission` checks exact source/consent/freeze; existing `Store.create_gpt_submission` writes encrypted, review-bound, one-submission-only data transactionally and returns real receipt. Exact duplicate response is safe; changed-answer replay is rejected.
- Old six GPT Actions remain unchanged; v1.7.0 adds only issuance. A cumulative existing-GPT update ZIP includes instructions under 8,000 characters (7,949 strict), original eight Knowledge files and v1.7.0 Action. The GPT offers Railway *only* on ready status and must not also submit in GPT after link issuance.
- Existing full Railway Venice questionnaire remains disabled. No new hosting/service/database or inference provider was created, and no real participant data or target/birth inputs were accessed during development.

## Verified

- Synthetic API end-to-end with independent worker-produced `ready` state, one-time link, token expiry, cross-browser access, origin/CSRF controls, changed submission retry, exact primary/secondary hashes and final encrypted receipt: all 11 focused finishing tests passed.
- Synthetic record with multiple previously answered and *skipped* independent clarifications survived exact source-bound storage; a link issued for a now-paused review was rejected.
- Real Puppeteer Chromium test at 390px and desktop: final page, malicious-looking source rendered as text, confirmation, exact three CF003 answers, encrypted receipt and page reload; no remote browser calls.
- Root repository suite: 1,092 passed, three unrelated official Swiss chart-fixture skips. Entire participant service suite: 244 passed, including 11 secure-finishing tests. Older v1.6.1 Action/GPT package remains deterministically reproducible through pinned historical source assets; new 1.7.0 builder also reproducible.
- Original versioned Action manifest updated to correct latest hashes. Existing scientific readme and code not repurposed to claim astrological or Human Design validity.

## Release / owner boundary

Project's production Railway environment had **four unrelated staged project changes**, while the specific participant service had zero staged config changes and still used its original persistent `/data` volume, one replica, and Dockerfile. Deployment should use a *service-specific* `railway up` from clean tested repository source; never accept the whole environment patch. Verify new live /healthz `ready_review_finish_enabled`, v1.7 Action operation and auth refusal without Bearer before inviting user.

The private Custom GPT editor remains a separate surface. The owner's ZIP is copied into `~/Téléchargements/Life-Patterns-Railway-Finish-2026-10-16/`. The owner must update the same GPT's Instructions, Knowledge handoff guide and existing Action schema without replacing its credential. The user may then test a link with the participant only when **her already saved independent review actually returns ready**; no real the participant review is accessed or modified automatically.

This is engineering enablement and human UX, not astrology validation.
