# Researcher desktop launcher repair — October 9, 2026

The original desktop launcher depended on unavailable Wayland clipboard commands and exited immediately, leaving the private dashboard locked and giving the appearance of zero records.

The replacement invokes a standard Python launcher with no visible terminal. It retrieves the existing authenticated service credentials at runtime, refreshes a restricted local feedback HTML report, and opens the official researcher dashboard through its supported one-time navigation handoff. The local report contains no access credential; the transient bridge has owner-only permissions and is deleted. The original server authorization remains intact.

Verification: the installed local report opens in the active Wayland session with exit code zero; the secure browser launch also returned exit code zero and resulted in authenticated HTTP 200 requests to the dashboard, feedback, sessions, and submissions endpoints. The live feedback report contains 10 entries and is mode 0600. The repo tests check HTML escaping and credential-file permissions.

Separately, production storage was checked against the exact canonical hash of the owner's 84-turn primary file. It matched exactly one encrypted submission with 84 primary turns, three CF-003 answers, received 2026-10-09 20:35:15 UTC. No resubmission is necessary.

Owner use: select **Life Patterns Researcher Dashboard** in the application menu. If the online dashboard fails, open `~/Téléchargements/Life-Patterns-Question-Feedback-Current.html` (actual Downloads is on /mnt/hdd). It is a read-only private fallback, not a replacement for the authenticated admin controls.

This task changes neither the frozen question bank nor the behavioral review, and saves no participant text or private tokens in Git.
