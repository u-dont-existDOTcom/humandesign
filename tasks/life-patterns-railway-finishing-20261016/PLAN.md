# Life Patterns — secure Railway finishing portal (2026-10-16)

## Owner outcome OPEN

Build/deploy the previously designed long-term workflow **now**, so an already interviewing participant can finish after the existing independent review reaches **ready**: same ChatGPT GPT interview → short-lived private Railway link → human-reviewed evidence confirmation → exact three CF003 questions → server-authoritative source-preserving final encrypted submission receipt. No restart/re-interview, no shared GPT bearer in a link, and no disclosed birth data.

## Existing incumbent / constraints

The existing Railway `life-patterns-participant` service has GPT review, secure/encrypted SQLite on persistent /data volume, six Action routes, exact behavioral source-match validation and transactional final submission. GPT remains interviewer, Railway remains independent reviewer, status `ready` is the only finish admission. Current browser survey / is disabled and Venice provider unconfigured; do not reopen it. The production Railway project has four **unrelated staged environment changes**: do not run an environment-wide accept-deploy or change secrets. Current deployment was Oct 9. The available Railway CLI supports target-specific `railway up` of existing service with current Dockerfile, but deployment route and staging semantics must be verified before using it. Preserve original volume, environment and one replica.

## Work contract / acceptance

1. Add a GPT-authenticated Action to issue a new **single-use, expiring, least-privilege** finish link only for existing `ready`, unsubmitted reviews. The returned URL's fragment contains an opaque random token, with no review ID, bearer secret, raw private source or visible DOB in path/query. Use exact configured HTTPS canonical origin.
2. Browser exchanges the link token exactly once for HttpOnly Secure SameSite cookie and CSRF token; short expiry and no automatic or repeated claim. Protect all state-changing operations with origin and CSRF and session status/expiry. No shared GPT Action credential in the browser.
3. Serve a single accessible mobile-responsive local web finish surface. It displays complete ready independent **neutral** evidence with source quotes, warns about remaining unknowns, and requires explicit participant confirmation. If inaccurate, offer return to the saved GPT chat for correction and another independent review: do not freeze a disputed record.
4. The *server* builds the final primary from the exactly reviewed candidate plus **only** stored clarifications, preserving original source turns verbatim and adding each admitted question/answer unchanged, then freezes after explicit confirmation and logs original consent. Freeze is never derived from a browser checkbox alone in the absence of source validation. Validate using the same existing submission gate, not a parallel weakened check.
5. CF003 three question wordings loaded from the versioned source, exact answers and skip rules from existing protocol, asked **after** primary freeze, stored separately and bound to canonical primary hash. Collect required familiarities as nonbehavioral metadata. Transactional final submission is tied to `review_id`, once; exact retry returns the same receipt; no duplicate source or review.
6. Run adversarial tests: no token / token reuse / expiry / wrong Origin / missing CSRF / attacker without session / not-ready review / paused+withdrawn / old submitted / duplicate submission / malicious HTML content / corrections, original turns unchanged, actual CF003 and hash, no accidental target leakage. Browser headless narrow check mobile and desktop if available.
7. Extend existing 1.6.1 Action schema additively; preserve prior six actions and plain progress semantics. Provide cumulative single existing-GPT update ZIP and full editor instructions under 8,000 strict characters.
8. Run targeted/full project suite, privacy audit, source checks; commit and integrate `humandesign`. **Only deploy if target service can be updated without accepting the unrelated staged environment patch** and exact service/volume/secret continuity is demonstrated. Verify live /healthz, portal non-issuance without bearer and schema; a real the participant review remains untouched until she chooses to finish.

## Status

Active; this plan is a work contract, not evidence of a finished or deployed portal. Synthetic tests never imply actual the participant consent or independent review readiness. No external participant's private source is read.
