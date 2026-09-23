# Survey-instantiated clean V4.3 / NetInformation result — 2026-09-23

Status: **COMPLETED DEVELOPMENT DIAGNOSTIC**. This is not untouched validation and is not a retuned post-result model.

## Freeze chain

- final neutral profile SHA-256: `7dc6333e42510c0fad145c2a90a6385051b20637b82da30281f6bc80361320a7`;
- frozen clean V4.3 translation SHA-256: `310a0aea90400d1adf97b935ac370e58fb4c5f99ca5f4df56a8a8072fe42b0f3`;
- search-result SHA-256: `077a5ad94e9647855ac7c3f68b1ed706a9b6febbbc5a5d322c36a68dd7d806a3`;
- scorer adapter was committed before search at `bbf0bee5beffd57eb3535e974e0c1e2d23c30975`.

Both scorer-family translations were frozen before this ranking was opened.

## Survey-instantiated scoring boundary

The primary run used only crosswalk-supported, candidate-unexposed V3.6/V4.3 mappings. It instantiated **19 mappings** and **0 contradiction mappings** from the frozen survey translation. Candidate-exposed Moon/Mars carrier refinements were excluded.

The historical V3.6 CoreFit block was not imported because the new survey crosswalk did not instantiate those old target assumptions. CoreFit was therefore constant/unavailable, and score-identical adjacent states were merged across changes in uninstantiated historical core fields before duration tie-breaking.

Ranking otherwise remained NetInformation descending, meaningful contradictions ascending, DetailedSupport descending, then stable duration.
## Result

Rank 1 remains the **2013-01-28/29** interval:

- `2013-01-28T07:59:21.282340Z` → `2013-01-29T03:11:29.192601Z`;
- NetInformation `4.182918`;
- DetailedSupport `51.786`;
- duration `19.202197 h`.

The best interval intersecting the recorded Philadelphia local birth date ranks **#872**:

- `1985-01-28T12:58:22.472936Z` → `1985-01-29T08:10:03.560047Z`;
- NetInformation `2.518282`;
- DetailedSupport `32.089`.

The exact recorded moment, `1985-01-29T10:25:00Z`, lies in the interval ranked **#1562**:

- `1985-01-29T08:10:03.560047Z` → `1985-01-30T06:19:18.040752Z`;
- NetInformation `2.317800`;
- DetailedSupport `35.125`.

## Interpretation boundary

This frozen new-survey translation does **not** preserve the old V3.6 target's clean V4.3 recoverability; the correct-date neighborhood falls far below its historical clean rank-2 position. Do not retune this translation after seeing the result.

This result does not by itself prove that the scenario survey failed as a general behavioral instrument. It shows that, after neutral measurement and the frozen crosswalk, the survey supplied much weaker evidence for the specific old V3.6 observable semantics used by this scorer. The historical clean V4.3 scorer also already failed exact-time recovery on the owner case, so scorer/crosswalk behavior remains a separate diagnostic from survey quality.