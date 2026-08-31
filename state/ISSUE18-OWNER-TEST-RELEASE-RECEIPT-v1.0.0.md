# Issue #18 owner-test release receipt v1.0.0

Date: `2026-08-31`

## Scope and authority

This receipt covers the owner-authorized merge and production release of the exact
PR #20 candidate, the repaired relationship birth-time intake, Railway source and
persistence recovery, and the first owner-only recovery probe. It does not authorize
friend recruitment, change a scientific mapping, or claim human validity.

Controlling sources:

- Human Design issue `#18`;
- owner authorization for PR #20 merge, production deployment, and one owner-only
  live test;
- PR #20 reviewed head
  `7f24ebc9936cb98db7e69a9ffa8dfbe018008a3c`;
- merged `main` commit `b5c2cc57513d4b5505fd23a8e4c605e4607c11b9`.

## GitHub release evidence

- PR: `https://github.com/u-dont-existDOTcom/humandesign/pull/20`
- State: `MERGED` at `2026-08-31T20:04:04Z`.
- Required `verify` checks: `SUCCESS` on the exact reviewed head.
- Source branch was preserved after merge.

## Railway release evidence

- Project: `humandesign-relationship`.
- Environment: `production`.
- Service: `relationship-web`.
- Deployment: `0c26073a-ff83-449b-a976-7ae4342d7e00`.
- Deployment status: `SUCCESS`.
- Deployment source: branch `main`, exact commit
  `b5c2cc57513d4b5505fd23a8e4c605e4607c11b9`.
- GitHub App repository access was restricted to
  `u-dont-existDOTcom/humandesign`.
- Production source branch is `main`; automatic deployment on GitHub push is enabled.
- The retired Railway Amsterdam region identifier was migrated to the current
  `EU West (Amsterdam, Netherlands)` identifier. Geography did not change.
- Privacy-safe persistence check: the mounted volume's file count, total bytes, and
  aggregate digest matched exactly before and after migration. Raw records and the
  private digest are intentionally absent from this public receipt.

## Live checks

- `GET /healthz`: HTTP `200`, `{"status":"ok"}`.
- `GET /api/study/recovery/status`: configured with `magic_link` and
  `six_digit_otp`.
- Production markup contains explicit `aBirthHour`, `aBirthMinute`,
  `aBirthSecond`, `bBirthHour`, `bBirthMinute`, and `bBirthSecond` controls.
- Production markup contains recovery email, code, request, and verify controls.
- One owner-authorized recovery request returned HTTP `202` with the deliberately
  generic anti-enumeration response.
- A privacy-safe private check found zero saved studies associated with the owner
  test address. Therefore no email was expected or delivered. This proves the
  missing-account privacy path, not the credential round trip.

## Adequacy assessment

- **Operational alignment:** `PASS` for the exact deployment, public health,
  repaired birth-time controls, configured recovery surface, and volume
  preservation. `PENDING_OWNER_SESSION` for successful email/code recovery and
  single-use replay rejection.
- **Scientific adequacy:** `NOT_ESTABLISHED`. These checks demonstrate software and
  release behavior only. They provide no evidence that Human Design, AstroHD, or
  AstroRRF predicts or describes people or relationships accurately.
- **Release adequacy:** `OPEN_OWNER_ONLY`. The owner can run the fresh production
  questionnaire. Sharing with friends remains outside this receipt until the owner
  smoke and recovery round trip succeed.

## Constraints and next boundary

- Incremental paid spending: `$0`; no purchase or Railway plan upgrade was made.
- No friend was contacted and no synthetic production session was created.
- Next evidence boundary: the owner creates one fresh production study using the
  authorized email address. Codex then requests recovery, verifies one single-use
  credential, confirms replay rejection, and updates this receipt without committing
  credentials, contact data, exact birth data, raw narratives, or private hashes.
