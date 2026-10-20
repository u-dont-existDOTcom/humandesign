# Conservative Zi Wei source-to-behavior eligibility and adjacent-hour stress test

**Status:** source-verified synthetic mechanics only. Not a preregistration, natal horoscope, psychological study, behavioral prediction or claim of a historically correct ancient printed edition.

## Evidence

The preceding accepted four-source-anchor candidate mapping (WuQu ZWD-R0287, LianZhen ZWD-R0330, TianLiang ZWD-R0464 and PoJun ZWD-R0505) remains unchanged, and the independently published Zi Wei chart-source/iztro 2.6.0 synthetic comparison is read from pinned Git commit and exact SHA. It has 312 comparisons, but only **120 distinct synthetic SOURCE chart states**: 10 specifically chosen modern calendar dates ×12 Earthly hour branches; computational male/female and alternative vendor leap options are duplicate comparisons, NOT independent people or natal prevalence.

The earlier review found exactly 12 states with a chosen star as the **sole** principal star in the Life palace, among the 120. Two had historically original always-next leap-month placement that did **not** match any Iztro raw vendor setting in this old comparison; ten had all compared vendor outputs matching.

### Explicit conservative statuses (mutually exclusive)

| Machine-supported / abstention status | States |
|---|---:|
| No selected principal star in Life palace | **86** — abstain; no inverse personality claim |
| Two of the four selected stars together | **3** — abstain; interaction unresolved |
| Exactly one selected star plus a different principal star | **19** — abstain; historical co-star rules unresolved |
| Selected star alone, but raw vendor leap-calculation disagrees | **2** — abstain; original school cannot be chosen post hoc |
| Selected star alone, all raw original-vendor variants agree | **10** — source mechanics only; NOT proof of behavior |

The ten mechanics-only candidates are PoJun6, TianLiang3, LianZhen1, WuQu0. These numbers describe only the chosen ten-day synthetic study; the original source does not assert that only single-star charts can exhibit such traits, nor that an unrepresented star means the opposite trait.

**No birth time, actual place, or human respondent data were used in this batch.** The conservative sole-star rule is a temporary **methodological restriction**, not a discovered classical injunction. Source translations are provisional and quantitative psychological prediction magnitudes are not established. Combined-star source interpretation must be specified *before* observing any real answers.

### Adjacent two-hour branch stress test

For each of the **12** structurally sole-selected original-source cases, the audit held the **same artificial reference calendar date** and compared its star-in-Life configuration to the immediately preceding and following Earthly two-hour branches. **Zero of twelve** retain the identical sole-selected principal-star configuration in both adjacent cyclic branches. **Ten** cases have both neighboring branches on the same notional calendar date; the other **two** are original Zi/Hai midnight wrap cases, where keeping the date fixed is not equivalent to a physically adjacent chronological birth instant. The time sensitivity result must NOT be translated into a risk for a real recorded birth clock: that requires modeling how many minutes of uncertainty cross a branch boundary, timezone ambiguity, local mean vs apparent solar choices and source day turnover. No such probability or verified actual birth-time calibration exists.

The ten source+vendor identical cases' selected-hour branches also do not establish that they would remain stable against uncertainty. The supported action is to **abstain or propagate an explicit set of possible charts**, not select the most appealing branch based on the interview. The accepted separate modern civil-time bridge currently fails closed on nonzero birth-time uncertainty and unsupported 23:00 Zi-day/apparent-solar policies; that is preferable to inventing a result.

## Scientific implications and boundaries

1. A **historically source-grounded individual main-star phrase** does not imply a validated trait, a calibrated probability or a deterministic chart preference among distinct co-star configurations.
2. A synthetic vendor school's 14-star placement match is a mathematical result under named conventions, **not** actual-person behavioral support.
3. Source leap-month disagreements must be reported; a mixed favorable school chosen after seeing responses is model leakage.
4. Source status is **conditional on a specific chart layout**. Uncertain birth time near a 2-hour star boundary needs interval evaluation. At midnight wrap, the adjacent real date itself may differ; this audit deliberately does not convert a fixed-date branch comparison into an adjacent UTC instant.
5. The full original life-palace source contains conditioning terms and mitigations; the next substantive research work is to code a source-first, preregistered co-location/contradiction resolver or preserve abstention, and independently verify calendar/time conversion. Excluded persons cannot be quietly reintroduced after seeing outcomes.

### Reproducibility

- `audit_conservative_feature_states.py`: pure standard-library source-locked classification and time-branch check, importing only its accepted predecessor's standard-library oracle verification.
- `FOUR_ANCHOR_SOURCE_FEATURE_HOUR_SENSITIVITY_V1.json`: 120 row-level machine states and twelve source-only hour-neighbor comparisons.
- `test_source_hour_stability.py`: 18 negative and positive checks, including tamper/changing source school/relabeling human outcomes.
- Parent original comparison SHA `01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5` pinned to commit `6f4a75febc1624e44b54d724422804a05f31fd12`. Previous eligibility audit SHA `f571b1c17db513f868bc2e645fb2a51ee21f91e5a287537f4e733a6d998f2c99`.
- All data and code are development-only synthetic. **Actual blinded human predictions tested: 0.**
