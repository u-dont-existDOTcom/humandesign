# 19 — Base-Level Substructure Validation

Date: 2026-08-22

## Decision

**Reuse/adapt the existing verified PySwissEph chart stack; do not build a separate Base engine.**

The repository already has the correct production astronomy architecture: pinned Swiss Ephemeris files, explicit `SWIEPH` selection, returned-flag verification, deterministic Rave Mandala mapping, and fail-closed behavior when the requested ephemeris is unavailable. The missing piece is the currently disabled Color/Tone/Base subdivision layer plus independent parity validation.

Color/Tone/Base remains **disabled for authoritative output until the validation gates below pass**.

## Independent conception snapshot

Problem: daily transit and natal research sometimes needs sub-Line precision without false precision or silent ephemeris fallback.

Mechanism: once a tropical longitude is computed accurately, the Rave wheel is deterministically subdivided into Gate → Line → Color → Tone → Base. The astronomical problem and the symbolic wheel-subdivision problem should remain separate and independently testable.

Constraints:

- preserve the repository's frozen 302° Gate-41 wheel origin and half-open `[start, end)` boundary convention;
- use production Swiss Ephemeris data, never silent Moshier fallback;
- do not expose Color/Tone/Base until constants and boundary behavior are independently cross-checked;
- keep provenance, ephemeris flags, and precision status in outputs;
- distinguish exact transit timestamps from natal positions whose Base may be unstable under birth-time uncertainty.

Candidate insight: no proprietary Base-level service is required. The existing chart engine can provide Base-level output once the deterministic substructure and parity suite are added.

## Existing-work scan

### Reuse

1. **Swiss Ephemeris / PySwissEph** for geocentric tropical longitudes. Continue using the repository's pinned `.se1` files and fail-closed returned-flag checks.
2. **Existing `hdmatch.chart.rave_mandala` wheel constants** for Gate/Line origin, order, and half-open boundaries.

### Adapt / cross-check

1. **SharpAstrology.HumanDesign** exposes Human Design substructure including Color/Tone/Base and can use Swiss/JPL ephemeris data. Use it as one independent parity implementation, not as an unexamined source of constants.
2. **domalhambra/hd-chart-engine** explicitly implements the Gate → Line → Color → Tone → Base hierarchy and is useful for wheel/subdivision parity. Its own documentation warns that Base is sensitive to ephemeris precision, so it should not be treated as astronomical ground truth unless run against an adequately precise backend.

### Novel remainder

The project-specific work is small: integrate the validated substructure into the existing Python engine, preserve fail-closed status/provenance, and add boundary-heavy parity tests suitable for prospective transit experiments and reverse-matching research.

## Frozen subdivision candidate

Starting from the existing Line width:

```text
Gate  = 5.625°
Line  = Gate / 6 = 0.9375°
Color = Line / 6 = 0.15625°
Tone  = Color / 6 = 0.0260416666666667° = 93.75 arcsec
Base  = Tone / 5 = 0.00520833333333333° = 18.75 arcsec
```

Hierarchy:

```text
1 Gate
  → 6 Lines
    → 6 Colors per Line
      → 6 Tones per Color
        → 5 Bases per Tone
```

The candidate constants must remain marked `unvalidated` until the parity requirements below pass.

## Implementation target

Extend `MandalaPosition` with integer `color`, `tone`, and `base` only after validation. Preserve the existing half-open convention at every level:

```text
[boundary_n, boundary_n+1)
```

At an exact boundary, the position belongs to the newly entered substructure segment, consistent with current Gate/Line behavior.

Add deterministic helpers for:

- Color boundary longitudes;
- Tone boundary longitudes;
- Base boundary longitudes;
- fraction-through-Color/Tone/Base if needed for diagnostics;
- provenance/status indicating `validated`, `unvalidated`, or `unstable_due_to_input_time_uncertainty`.

Do not infer Base from rounded ephemeris tables.

## Validation gates

### 1. Astronomy gate

For every validation point:

- requested ephemeris = `SWIEPH`;
- returned ephemeris = `SWIEPH`;
- pinned ephemeris-file hashes match the manifest;
- no Moshier fallback;
- longitudes are retained at full floating-point precision before symbolic mapping.

### 2. Deterministic boundary gate

For every Color/Tone/Base boundary across the 360° wheel, test:

- exact boundary;
- immediately below boundary;
- immediately above boundary;
- wraparound at 0°/360°;
- stable half-open assignment;
- no off-by-one errors from floating-point rounding.

Use exact rational/integer substructure indexing where practical rather than repeated floating-point division.

### 3. Independent implementation parity

Cross-check a boundary-heavy fixture against at least two independently implemented references/settings. Minimum target:

- SharpAstrology.HumanDesign using Swiss/JPL-grade astronomy;
- a second independently implemented HD wheel/substructure mapper, with astronomical parity checked separately.

Disagreements must be classified as one of:

- astronomy longitude difference;
- node convention difference;
- Rave wheel origin/order difference;
- boundary inclusion convention;
- Color/Tone/Base subdivision convention;
- implementation defect.

No majority vote. Resolve the underlying convention before activation.

### 4. Golden-chart gate

Use known charts with trusted Base-level outputs where available. Include cases deliberately near substructure boundaries, not only ordinary interior points.

### 5. Prospective transit gate

Once the above passes, use exact transit timestamps as the cleanest Base-level test because the event time is known precisely. Store the predicted Base state before asking for the user's observation.

### 6. Natal uncertainty gate

Base is only ~18.75 arcsec wide. For fast bodies, especially the Moon, ordinary birth-time uncertainty can cross multiple Base boundaries. Natal reports must therefore propagate the documented time uncertainty and report a Base only when stable throughout that interval; otherwise return the set/range of possible substructure states.

## Activation rule

Color/Tone/Base may be enabled for authoritative transit or natal output only when:

1. Swiss Ephemeris fail-closed verification passes;
2. all deterministic boundary tests pass;
3. independent implementation parity passes or all disagreements are explicitly resolved;
4. golden/reference checks pass;
5. provenance and uncertainty fields are emitted by the engine.

Until then, keep the current `advanced_substructure_status = "unavailable_unvalidated"` behavior.

## Research interpretation

This work validates calculation reproducibility and convention parity only. It does not establish that Human Design substructure predicts behavior. Behavioral claims remain subject to the repository's prospective/blinded validation rules.
