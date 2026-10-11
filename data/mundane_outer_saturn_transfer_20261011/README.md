# Immutable source snapshots used by 2026-10-11 transfer backtest

The **raw** external dataset copies are intentionally **not** committed in the public HumanDesign repository. The executable script can download the same provider files if unchanged (`--fetch`), verifies source SHA-256, and will fail if the provider later changes them. Exact private source snapshots are delivered separately to the authorized owner.

- Powell–Thyne, *Global Instances of Coups*, August 29 2026 update: https://jonathanmpowell.com/coups/ ; research article: Powell & Thyne (2011), DOI 10.1177/0022343310397436. Event-level original CSV `powell_thyne_20260829.csv`; SHA-256 `1e8f933b22f4b9a77d0ba5eb59bf0d8158adcaab27746adcf345195be87a9012`. Redistribution rights for full raw file have **not** been asserted.
- Uppsala Conflict Data Program, UCDP Intrastate Conflict Onset v25.1 (1946–2024): https://ucdp.uu.se/downloads/olddw.html ; CSV `ucdp_intrastate_conflict_onset_251.csv`; SHA-256 `a5a64b749693c85fd3b50a1311608a44c0846d528352baeb3767f25e50d52fe1`. UCDP source dataset is CC BY 4.0 with attribution.

Derived annual and five-year counts and exact result metrics **are** tracked under `reference/research/mundane_outer_saturn_transfer_20261011/`.
