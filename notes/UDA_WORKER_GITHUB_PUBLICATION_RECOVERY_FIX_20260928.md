# UDA worker/GitHub publication recovery fix — 2026-09-28

## Incident

During the empirical-astrology Wave 1 parallel extraction, workers W04-W10 completed correct local commits in isolated scratch worktrees. Their shell `git push` commands failed because those worktrees lacked GitHub credentials. The coordinator initially treated the local commit receipts as if they were close to merge-ready and then required owner relay/recovery steps.

The actual reusable failure was a completion/publication boundary defect:

- branch isolation existed;
- local work was preserved;
- but remote retrievability was not part of worker completion;
- worker directives did not bind publication transport/fallback tightly enough;
- the already-authorized GitHub connector/API was not used immediately as the transport fallback;
- a local-only commit was allowed to masquerade as a deliverable integration state.

## UDA repair

Merged to `u-dont-existDOTcom/universal-dev-architecture` main as:

- merge commit: `dbda52123258fddf95ce69d32a247e9a5f8f1774`
- pull request: `#276`
- new canonical pattern: `patterns/worker-github-publication-and-recovery.md`

Key rules now enforced:

1. Integration-bound worker completion is destination-bound, not local-worktree-bound.
2. Explicit states:
   - `LOCAL_COMPLETE_REMOTE_UNPUBLISHED`
   - `PUBLISHED_UNVERIFIED`
   - `INTEGRATION_READY`
   - `BLOCKED`
3. Worker directives must include the publication contract: repo, remote branch/destination, owned paths, authority, fallback transport, verification, integrator.
4. Publication transport must be preflighted before substantial isolated work.
5. If shell Git lacks credentials but an already-authorized GitHub API/connector can publish the same scope/destination, the worker must use that fallback before owner interruption.
6. API recreation preserves both the original local HEAD and remote publication commit, and verifies exact remote content/diff.
7. Coordinators must verify every expected worker output remotely before declaring a parallel wave complete.
8. Local-only scratch commits are nonterminal and cannot be treated as integration-ready.
9. Durable-write and worker-self-remediation rules were updated to make this recovery path reachable.
10. The rule graph now routes parallel write isolation through the publication/recovery rule.

## Verification

UDA PR #276 passed:

- Deterministic repository audit: PASS
- unit tests: PASS
- VPS browser relay tests/syntax: PASS
- Mission Control app tests/types/build: PASS

## Project implication

Future parallel humandesign workers should be given remote publication instructions at launch, not after completion. If they are isolated scratch workers, the coordinator should predeclare unique worker branches and GitHub connector/API fallback from the start.
