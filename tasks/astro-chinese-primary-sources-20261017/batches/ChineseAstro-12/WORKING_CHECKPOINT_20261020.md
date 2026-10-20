# ChineseAstro-12 — independent full-chart implementation parity (working research)

From verified parent `29f76089739271dab0695f8699081d52600cb10b`. Source registries immutable (13,044 Lilly +1,066 Ptolemy +210 BaZi +220 Zi Wei historical annotations). No predictive validation.

Goal: compare our independently original-verse-implemented 14 main Zi Wei stars, life/body, bureau against an outside full Zi Wei codebase `SylarLong/iztro`, without importing or copying iztro's code into HumanDesign. Use pinned npm version and synthetic dates/hours, no personal participant records. Separate original Chinese Quan Shu rule variants from iztro modern defaults and leap-month handling. Preserve mismatches, no silent overwrite.

Upstream docs: https://docs.iztro.com/en_US/quick-start and https://github.com/SylarLong/iztro/blob/main/src/astro/astro.ts . Not an independent historical manuscript, astronomical calendar ground truth or real-person prediction verification.

Next: immutable package version/date inputs, independent sample chart outputs, mechanical comparison and explicit negatives. No runtime promotion.

## Independent outside engine: pinned iztro@2.6.0, 312 synthetic charts

The original `iztro` npm package was installed *only* to a temporary local directory outside the repository, with reproducible npm `package-lock.json` SHA `77f95d231b6237bae0b972badb7ecb619171de70043805153f52fee8fef65b96`. No third-party vendor code or binaries copied to humandesign. New `tests/iztro_2_6_0_oracle_bridge.cjs` drives the outside unmodified package with explicit `default`/normal year/forward day and records exact fourteen stars, Life/Body palaces and elemental bureau.

New `tests/audit_source_against_iztro_2_6_0.py` compares frozen original HKO lunar dates (10), 12 hour branches, male/female, and for 3 leap-month dates both iztro `fixLeap` options: **312 fully specified synthetic charts**, no real personal participants. `IZTRO_2_6_0_FULL_312_CHART_COMPARISON_V1.json` contains all 312 source and vendor outputs and all 120 mismatches, exact overall comparison stream digest `37a5a7f18203b92a218a1b33adee36818928cfc2148558e083aa17793016ffdb`. Source default follows original Quan Shu 'leap as next'; vendor uses optional 'leap same month' or 'first half current/second half next'. With original source school convention **192/312 complete matches**, **120 mismatches**, **168/168 nonleap full agreement**, **24/144 leap full agreement**. All 120 source-default disagreements are leap-only; 120 affect Life palace and Body palace, 60 change bureau and the fourteen principal-star positions. Preserve *all* such negative differences, not silently correct historical rule.

When deliberately applying an **explicit comparison-only policy normalizer** to emulate each of iztro's two leap-month switches, the same 312 synthetic inputs reproduce **312/312** external positions and Life/Body/bureau; this is a test of *whether algorithms match given identical conventions*, NOT independent astrology predictive validation. Original source default **unchanged**, earlier 120 disagreements retained and require policy selection in any actual full-chart workflow. No independent first-edition original classic reproduction verified, no authentic human natal chart/forward behavior scored.

Offline `tests/test_ziwei_iztro_source_parity.py`: seven test cases check immutable frozen SHA, 312 exact source-vendor outputs, all disagreement negative fields, leap/nonleap splits, counterfactual aligned replay all 312 positions, gender invariance of major star layout and zero blind human claim. Initial focus 7/7 green.

## Unfinished root gates

Chinese reference-day converter still explicitly requires already-resolved official Hong Kong Chinese lunar-day convention and independently established birth hour; does not convert real birth locality/time zone into the correct astronomical day or true solar time. Li Chun 10-stem BaZi year/month and full calendar historical era parity unverified. Full Zi Wei minor stars, Si Hua, timing, original print provenance and human predictions unverified. Western original Lilly next R13045 Chapter CLXXXI; BaZi Di Tian Sui next BZI-R0211; Zi Wei new source next ZWD-R0221 on isolated worktrees, never duplicate accepted records. Need freeze modern source models and actually test real consented untouched human participants forward and reverse versus decoys and nonastrology baseline. Current independently predictive human tests **zero**.

**DO NOT RERUN** the initial 312 vendor call without source, dependency version or test set changing: read the checked original frozen outputs and seven offline tests. No new historical annotation IDs admitted in this batch.

## Accepted research-only engineering verification (post-comparison)

The finalized, offline source/iztro fixture replay preserves 312 case-level examples, 120 original cross-variant negative results, and the policy-normalized 312/312 mechanical matches without altering any frozen original responses. Independent of the 7 focused tests, inherited Zi Wei + calendar + new source/iztro regression run passed **66/66** in 4.119 s with optional lunar_python/sxtwl available. The JS vendor adapter passed node syntax, reconciliation JSON parsed, and git staged diff checked for whitespace errors. The test-budget observer was used; full century data recomputation and 312 live vendor replays were not repeated unchanged.

The accepted source counts remain Chinese V9 **430** and Western original source **14,110**; this research batch adds **0** source annotations. No verified real human forecasts; runtime promotions **0**. Historical source original authenticity and initial leap-month school variant remain distinctly unresolved.
