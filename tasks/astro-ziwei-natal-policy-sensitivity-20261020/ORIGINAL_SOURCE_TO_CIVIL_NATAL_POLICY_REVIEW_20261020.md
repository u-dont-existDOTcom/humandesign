# Pinned-source Zi Wei birth-clock policies — four synthetic full mechanics tests, 20 October 2026

**Status: historical-source/chart engineering, NOT human predictions.** Four strictly **invented** local clocks were constructed to expose genuine source-convention and zone/calendar disagreements. The accepted original-transcription Zi Wei source text, 14-principal-star position mechanics and civil-time conversion code are used from the exact separately accepted parent Chinese engine commit `fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4`. Twenty-two exact source-engine/code/HKO witness files were SHA256 verified before execution; old Wikitext `紫微斗數全書 卷二` revision oldid1963110 is transmitted Chinese text, NOT authenticated original Ming printed woodblock. The 14-major-star layer is not a complete astrological chart.

Two **independently implemented Chinese-calendar libraries**, explicitly pinned `lunar_python 1.4.8` and `sxtwl 2.0.7`, were recovered from the existing local research environment without additional downloading or network access; runtime source-code tree/binary checksums for both were pinned. These independently agree on the 48 calendar inputs used here but this is not a full original-calendar historical proof. Only 30/48 source calendars have direct archived original **Hong Kong Observatory HKO date response bytes** corroborated against both implementations; 18/48 have two-software agreement **without direct archived official HKO date evidence**. Do not group them as 48 independent official original observed dates; they are 48 assumptions applied to only four artificial clocks.

## Named assumptions: 4 clocks × 2 calendar reference days × 2 hour methods × 3 leap schools

The method distinguishes **(a)** the Chinese reference calendar day as the *same UTC instant on fixed UTC+08:00* vs *birthplace's historical IANA local civil Gregorian date*, and **(b)** the two-hour Earthly Branch from the *recorded civil wall clock* vs *local mean solar longitude* (longitude explicit, east-positive). Three leap-month policies are compared as a **sensitivity menu** only: transmitted Quan Shu always-as-next, modern same-month and modern first-15 same then next. Neither policy is opportunistically selected after seeing behavior. Zi Wei year boundary is Chinese Lunar New Year for this engine, **not** BaZi Li Chun. Full apparent (true) solar time, alternative 23:00 Zi-day turnover and interval propagation for uncertain clocks remain *unsupported/fail closed*.

Synthetic outcomes under the **original source's always-next leap policy** (no human subject):

| Artificial case | Number of distinct Life-palace major-star configurations among four calendar/hour conventions | Key observation |
|---|---:|---|
| Dakar/West Africa, fictional clock 2026-02-16 21:30 | **4** | Fixed-UTC8 day/recorded hour -> TianJi+JuMen; fixed-UTC8/local mean -> TaiYin; birthplace civil day/recorded -> WuQu+TianXiang; birthplace/local mean -> TaiYang+TianLiang. Two different lunar years straddle New Year |
| Hong Kong, fictional 2023-03-22 midday first leap-month day | **1** | Hour/date variants agree, but alternate leap-month rules change full 14-star chart: original always-next gives TaiYang alone in Life palace Xu; same-month/first-half modern schemes give Life palace You, no major star |
| New York, fictional 2026-10-20 13:30 | **4** | UTC+8 calendar sees 2026-10-21 vs local 2026-10-20; recorded hour Wei vs local-mean Wu; source Life stars TianXiang/TaiYang/TianJi+JuMen/QiSha |
| Hong Kong, fictional 1965-07-01 00:30 during historical DST | **2** | Recorded local civil day 1965-07-01 vs fixed UTC+8 reference day 1965-06-30; Life palace Wei but source star changes TianXiang to TianLiang. DST is not automatically the same as fixed UTC+8 |

The apparent agreement or disagreement here is **mathematics of declared inputs**, not evidence these source rules correspond to physical traits, actual personality, marriage, health, career or other real-life outcomes. The four provisional source-to-behavior anchors (WuQu, LianZhen, TianLiang, PoJun) are not a complete profile; policy choice changes which hypothetical model terms can even be applied. Full source conditional/co-star rules are unresolved.

## Explicit fail-closed negative conditions

All seven unsupported tests failed without generating a usable natal chart:

- The lunar date 2057-09-28 has **inconsistent calendar oracles**, `lunar_python` says lunar 8/30 while `sxtwl` says lunar 9/1.
- New York spring DST gap 2026-03-08 02:30 does not exist; autumn 2026-11-01 01:30 is ambiguous without explicit fold.
- Nonzero stated recorded birth-clock uncertainty is not silently rounded away; the accepted time bridge requires exact zero or a not-yet-implemented set/interval of possible charts.
- The historical alternative Zi-day turnover at 23:00, true apparent solar time and Li Chun annual-stem convention are not implemented and cannot be selected by guessing.

All application stages preserve the source's own qualifications and false/unknown results. If a human has an uncertain historical birth clock, a single chosen attractive chart is **not** valid evidence. A future model must either propagate all plausible chart states and only predict invariant features, or abstain. The present engine has not implemented that full interval propagation, and no user consent/recruitment occurred.

## Provenance/reproducibility

- `PINNED_ENGINE_FILE_MANIFEST_V1.json`: original engine SHA/byte receipts from immutable accepted Git commit, including pinned 1647? **NO**: this is a Chinese transmitted traditional source with separate HKO raw date references, NOT Lilly's 1647 book.
- `run_pinned_natal_policy_sensitivity.py`: builds a fresh temp source-engine tree from 22 exact accepted Git files without editing other worktrees or old source ledgers. It requires two unbundled, exact-version AND source/binary-SHA-pinned lunar calendar reference libraries.
- `worker_compute_synthetic_policy_variants.py`: only the four explicitly fictional civil clocks; 48 predetermined policy permutations and seven unsupported-condition tests.
- `PINNED_ENGINE_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1.json`: complete star placements, HKO provenance quality, policy, declared IANA zone, TZif source SHA and failure status for all synthetic calculations.
- `test_pinned_synthetic_natal_policy.py`: focused original-source/entrypoint/environment/timing and negative-control regressions (18 passed before portable archive).
- The external lunar packages contain non-user code, not copied into the repo or archive. The portable study is reproducible where independently installed exact pinned versions/binaries and matching TZif/zoneinfo data are available; it is **not** an all-platform standalone binary.
- Source historic annotations across independent branches remain Western Lilly13236/Ptolemy1066 and Chinese BaZi210/ZiWei586, aggregate 15098 documentary observations, **not 15098 real-human predictions**.

**Next meaningful scientific step**: verify an ancient Zi Wei Life/14-star chart interpretation selection using *source-defined conjunction/negative/mitigation conditions*, and implement a bounded **birth-time uncertainty → set of possible computed charts** mechanism for documented finite intervals and declared calendar/solar-hour conventions (rather than silently selecting a chart). Keep higher-order astrology outcome mapping, control questionnaires and real-person consent frozen prerequisites before studying actual untouched humans. Human predictive validation count still zero.
