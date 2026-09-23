# Claude Opus 5.5 independent V4.3 remap — v2 result — 2026-09-23

Status: **COMPLETED POST-RESULT DEVELOPMENT EXPERIMENT**.

This experiment does not overwrite or upgrade the frozen v1 calibration. The v1 V4.3 result was already known before v2 was conceived. The v2 mapping and result are therefore development diagnostics only.

## Frozen chronology

- neutral profile SHA-256: `7dc6333e42510c0fad145c2a90a6385051b20637b82da30281f6bc80361320a7`;
- isolated Opus input packet SHA-256: `84078b3bd9afc3170b71d34e6ded8fe1743f7646c50755e7befd8abf14947c0c`;
- semantic Opus translation SHA-256: `37f70ca7da4aaf6a5e4224f4136d2198e562233471f45e8ab0c2d120ee45fb5e`;
- adapter-compatible scorer-input SHA-256: `f93c331c748f6faaa7c252b2b12cad517cff088bf87c4dd64f11e2f3e78b669b`;
- v2 scorer result SHA-256: `4b081b8e57deaa9d02fb6ac1c558b4d8e5bc64d7329d99b9e0daadc2255c88f1`.

The Opus model was exact `claude-opus-5-5`, max effort, isolated from prior GPT translation, birth/chart data, candidate states, and prior ranking results. The 19-row result passed structural validation before scorer execution.

## Mapping change

GPT v1 instantiated 19 chart mappings. Opus v2 instantiated 27 candidate-unexposed mappings and still 0 contradiction mappings.
Opus newly supported five observables that GPT v1 left unestablished: `AUTHORITY_SOMATIC`, `ENTERPRISE_PERSUASION_PATTERN`, `NEEDS_SENSITIVITY`, `PROFILE_LINE6_PHASES`, and `VALUES_RESPONSIBILITY`. It also raised `PROFILE_24` and `RESOURCE_SOVEREIGNTY` by one confidence step.

## Rerun result

The rank-1 interval is unchanged:

- **#1:** `2013-01-28T07:59:21.282340Z` → `2013-01-29T03:11:29.192601Z`;
- NetInformation `5.280159`;
- DetailedSupport `49.812`.

Best interval intersecting the recorded Philadelphia local birth date:

- **#204:** `1985-01-28T22:57:16.635098Z` → `1985-01-29T08:10:03.560047Z`;
- NetInformation `3.615523`;
- DetailedSupport `36.025`.

Interval containing the exact recorded moment `1985-01-29T10:25Z`:

- **#1943:** `1985-01-29T08:10:03.560047Z` → `1985-01-29T11:41:42.420035Z`;
- NetInformation `2.834018`;
- DetailedSupport `33.900`.
## What changed versus v1

The best recorded-local-date rank improved from **#872 to #204** (about 4.27× fewer intervals ahead of it), showing that the first translation materially affected the ranking distribution.

However, the diagnostic score gap to the 2013 winner did **not** improve:

- v1: `4.182918 - 2.518282 = 1.664636` bits;
- v2: `5.280159 - 3.615523 = 1.664636` bits.

The Opus-added evidence increased both the 2013 winner and the best 1985-date interval by exactly `+1.097241` bits. Thus the apparent rank improvement is a reshuffling of other candidates, not increased separation favoring the recorded date over the persistent 2013 winner.

The exact recorded-moment interval moved from #1562 to #1943 and its gap to the winner widened from `1.865118` to `2.446141` bits.

## Interpretation

The GPT v1 remap was too conservative in a decision-relevant sense: a stronger independent remapper recovered more survey-to-observable support and substantially altered rank density. But the unchanged 2013-vs-best-1985 score gap is strong evidence that remapping quality alone does not explain the core mismatch inside this frozen 19-observable V4.3 architecture.

No v2 judgment will be retuned after this reveal.