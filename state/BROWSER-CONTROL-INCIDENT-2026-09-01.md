# Browser-control incident — 2026-09-01

Incident ID: `MC-BROWSER-REPO-TAB-SPRAWL-20260901-001`

Status: `ROUTING_TO_SHARED_PRO_SUPERVISOR`

## Observed failure

While preparing the Extra High and Pro evidence packets, Codex opened six transient
GitHub browser tabs: the two Mission Control packet blobs, the Human Design handoff,
and three implementation-source pages. This visibly flooded Joel's active Brave
session. Joel reported the failure before the Pro meta-review packet was submitted.

The GitHub tabs are now closed or stale. The signed-in Extra High and shared Pro
supervision conversations were not closed or interrupted.

## Evidence-bounded cause assessment

The proximate cause was an unnecessary retrieval choice: Codex used the connected
browser to extract exact GitHub text even though authenticated `gh` and the local Git
checkout were already available. The tab-per-source approach had no cleanup guard and
did not minimize impact on the owner's active browser.

This is a workflow/control failure, not evidence of a Brave-extension defect. The
generic connected-extension selector successfully bound the active Brave session.

## Immediate containment

- Use the browser only for signed-in ChatGPT reasoning-surface evidence that cannot be
  obtained through GitHub CLI or local Git.
- Use `gh` and local Git for all subsequent repository reads and writes.
- Reuse one browser tab where navigation is genuinely required; close agent-opened
  transient tabs promptly and preserve owner-opened tabs.
- Add this incident to packet
  `PRO-META-A40D413-AUTHORITY-PROVENANCE-20260901-v1` for the shared Pro supervisor to
  accept, revise, or reject a durable Mission Control control.

## Proposed durable control for Pro review

Before browser navigation, record `browserNecessity` and `nonBrowserAlternative`.
Repository content retrieval must default to authenticated CLI/local checkout. If a
browser is necessary, record agent-opened tab IDs, cap transient tabs at one unless
strictly necessary, and close only those recorded tabs when finished. A violated cap or
available non-browser path should emit `UNNECESSARY_OWNER_BROWSER_MUTATION`.

This proposal is a candidate pending the shared Pro supervisor's verdict; it is not an
accepted Mission Control policy.
