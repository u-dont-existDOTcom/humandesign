# Relationship/AstroHD current state

As of: `2026-08-31 12:09 GMT`

This task-specific checkpoint supersedes the older repository-global next action in
`state/CURRENT-STATE.md` and the Pro-checkpoint sequence in `CURRENT_PLAN.md` for the active
relationship/AstroHD continuation. The controlling directive is GitHub issue #18:
https://github.com/u-dont-existDOTcom/humandesign/issues/18

## Current objective

Build and test a genuinely blinded Human Design/AstroHD system that makes specific precommitted
predictions and is evaluated against real participant evidence. Synthetic recoverability,
governance completeness, tests, and model review are supporting evidence only; they are not
evidence that Human Design predicts humans.

## Reconciled repository state

- Public default branch: `main` at `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`.
- Active local branch: `codex/astrohd-relationship-continuation`.
- Recovered pre-receipt head: `dbb5ac6e4a3b37f1679d614c9cd1f52ef88ac5a5`.
- Issue #18's last-known head `4d5cc5eaa77164eaa71dbf0bd9a1533dd4c95409` is a
  preserved ancestor of the recovered head, not the current tip.
- The recovered branch is a direct 128-commit descendant of current `main`; no rebase, squash,
  merge, or history rewrite occurred.
- Before this recovery receipt, the committed diff against `main` contained 454 files,
  53,910 additions, and 54 deletions.
- The interrupted untracked checkpoint-14 methods-scan draft was excluded because it was
  incomplete, had never entered branch history, and issue #18 explicitly stops that work family.
  Every committed continuation commit and its ancestry remain unchanged.
- GitHub had one other open pull request before this branch was published: stale draft PR #1 at
  `3bab2c58f6972b4a66b7b68bb8cde6ba507d64db`, dirty against `main`. It remains untouched.

## Privacy and durability boundary

- `python scripts/check_private_artifacts.py --repository-root . --diff-base origin/main` passed
  against the recovered branch, including forbidden private paths, tracked credential shapes,
  branch-diff paths, and reachable-history checks.
- No private participant record, raw response, exact birth record, email address, recovery token,
  session token, secret value, or Railway volume content was accessed or added.
- No path required exclusion from the GitHub branch. The branch may therefore be published in full.

## Railway and live-runtime reconciliation

- Project `humandesign-relationship`, production service `relationship-web`, is online at one EU
  West replica with the persistent `relationship-web-data` volume attached.
- Active successful deployment remains
  `60c360b2-6591-4e96-9d82-66e6808f82e5`, created from the PR #17 merge lineage documented at
  `450d806efe66e8299f5d43dd046685e8415b9a30`.
- Read-only live checks returned health `ok`, configured direct OpenAI model `gpt-5.6-sol`, and
  configured magic-link plus six-digit-OTP recovery.
- No Railway setting, variable, secret, deployment, volume, or participant data was mutated.

## Active bounded sequence

1. Preserve and push the exact continuation history plus this recovery receipt.
2. Open one draft PR against `main`; do not merge or deploy it.
3. Route the exact PR base/head diff and this state receipt to a fresh Extra High review context.
4. Stop implementation at review boundary A until Extra High issues a versioned next directive.
5. After that directive, perform only its bounded execution/evidence sequence.

Extra High must classify each changed surface as one of:

- `DIRECTLY_REQUIRED_FOR_FIRST_HUMAN_EVIDENCE`
- `REUSABLE_ENABLEMENT`
- `DUPLICATIVE_GOVERNANCE`
- `DEFER`
- `REMOVE_OR_ARCHIVE`

## Explicit stops

- Do not create another governance, methods-scan, acceptance-matrix, dossier, or Pro-checkpoint
  child.
- Do not use Pro for ordinary repository review, branch recovery, pilot drafting, smoke-test
  interpretation, or governance cleanup.
- Do not contact, screen, recruit, compensate, or collect material from humans.
- Do not merge, deploy, migrate, release, or change participant-facing scientific inference.
- Do not present synthetic performance as Human Design accuracy.

Current outcome state: branch-recovery cycle in progress; root scientific outcome open; scientific
adequacy remains warning-level; release remains closed.
