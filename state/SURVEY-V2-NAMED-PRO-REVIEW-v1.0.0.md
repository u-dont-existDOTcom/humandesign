# Survey-v2 Named Pro Review v1.0.0

- Review: `SURVEYV2-HUMAN-MEASUREMENT-AND-SCORING-FREEZE-v1.PRO-RULING-v1.0.0`
- Decision: `BLOCKING_DEFECTS`
- Owner decision required: `NO`
- Reviewed draft PR: `#20`
- Reviewed base: `b7660b8c9bcf52cbb14bc5442c13a3a8635aad32`
- Reviewed head: `74ddb10fdba87fd477275ff20123ffd51aa4b6a6`

## Exact reviewed hashes

- contract: `53e88db86e6a64c2fc572a5db80ea0694914601ad63b6ea045f18e2ec0e3801c`
- classifier prompt: `0462ab593e523d5fe08b24e838d4aea4a8fd651f7d3226c435fe542c235bf343`
- classifier output schema: `8df8fd59c2bbe03f059c786622b60d8df24bb826fb31558fbe7def71cd8e561f`
- 49-fixture specification: `030c64ed67a4686888d8728332161e9155939fb6b7a59ca3e4b994f5c784c0fd`
- methods check: `1f8e4427cd6d9d78dc6ca8f8fe00b09d1654f06205b2f21a5c08e4bd63d32f7e`
- freeze manifest: `1ec4ba1d31348910a1fc0badc201d4622f088c8dd83c143a5bc75f6082e71a9c`

## Typed adequacy ruling

- Operational alignment: `PASS FOR THIS NAMED REVIEW ONLY`.
- Scientific adequacy: `NOT ADEQUATE FOR EXACT FREEZE` until B1–B4 are corrected.
- Release adequacy: `CLOSED / NOT ADEQUATE`.
- Circularity/leakage: direct candidate and true-state leakage controls passed, but
  complete scientific closure failed because of classifier-controlled missingness,
  the non-executable H1 contamination branch, and duplicate structural weighting.

## Required corrections

- `SV2-FREEZE-B1`: require unique request job identities and an exact ordered
  request/result bijection; any missing, extra, duplicate, or mismatched result is
  `TECHNICAL_FAIL` with no score or rank; forbidden-input output is empty.
- `SV2-FREEZE-B2`: give support, mandatory contrast, and counterevidence distinct
  typed custody; a contrast need not support the selected label and becomes
  counterevidence only under an explicit contradiction rule.
- `SV2-FREEZE-B3`: add a separately manifest-hashed, blind H1 exposure-adjudication
  contract, prompt, strict output schema, custody boundary, and named fixtures.
- `SV2-FREEZE-B4`: freeze an exhaustive field-to-source dependency map; assign every
  field one dependency cluster; exact-rational macro-average eligible members and
  count the cluster once.

## Authorized route

Correct only B1–B4; regenerate the exact hash-bound candidate; retain
`runtime_behavior_passed=0` and every implementation/release/human-execution gate;
run exact-head validation and CI; return the corrected exact diff/hash packet to the
existing Issue #18 / Extra High boundary.

No deployment, merge, participant use, recruitment, spending, or additional Pro
review is authorized by this ruling.
