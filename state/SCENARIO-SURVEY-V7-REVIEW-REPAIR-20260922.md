# Scenario survey v7 blind-review repair state — 2026-09-22

The original v7 redesign commit passed same-context and deterministic checks but failed a properly blinded semantic review with two blockers. The original review prompt is no longer treated as independent because it exposed producer rationale and prior audit material before diagnosis.

Confirmed repairs now present:
- bodily-signal follow-ups require a reported reaction, not a pre-established stable reaction; brief/inconsistent reactions remain eligible for the routes that measure time course/consistency;
- M05 and M06 now ask matched interpretation tasks, M06 assumes no concern, and X04 context/limits credit requires paired answers.

Verification: 447 / 447 deterministic checks pass.

The Stage-1 review record, information-firewall manifest, blind prompt, and reconciliation are under `tasks/scenario-survey-v7-review-repair-20260922/`.

Next: run a new blind Stage-1 review on the repaired bytes. Do not disclose prior findings or reconciliation to that reviewer until findings are frozen.

## Second blind rereview

A fresh mechanically firewalled GPT-5.6 Sol xhigh rereview of commit `4d4eddc4975bf2a4a146648ae547beb6986741b9` returned `NOT_READY_FOR_FRESH_PILOT` with four additional blockers. Those blockers are now repaired:

- F0 now contains a matched two-audience comparison;
- M11 credits only answer-originated objection handling rather than a supplied fairness rationale;
- G15/R07/R08 now hold work modality and ordinary conditions constant;
- G17 now directly compares high- and low-consequence corrections under similar confidence.

Verification now passes 459 / 459 deterministic checks. Another blind rereview of the exact repaired commit is required before fresh-pilot readiness.
