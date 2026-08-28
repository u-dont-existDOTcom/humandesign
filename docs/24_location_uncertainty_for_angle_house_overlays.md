# 24 — Location uncertainty for angle and house overlays

Status: reusable calculation/interpretation rule for AstroHD; contains no participant birth data.

When a birthplace is a small village whose spelling or current administrative district is ambiguous, do not silently substitute a nearby city and present the resulting Ascendant/houses as exact.

## Resolution ladder

1. Search official administrative-unit records for the village name and spelling variants.
2. Cross-check a geocoded nearby locality or village cluster from an independent mapping source.
3. Preserve any discrepancy between historical and current district boundaries rather than treating it as a different birthplace automatically.
4. If the exact village coordinate is unavailable but a tight local cluster is identified, calculate a location-sensitivity envelope that includes the matched village cluster plus any explicitly supplied nearby city/district proxy.
5. Report Ascendant/MC and house placements as usable only if the interpretation is stable across that envelope.

## Stability rule

For each plausible coordinate:

- recompute Ascendant and MC;
- recompute all house cusps under the declared house system;
- recompute natal planet houses and reciprocal synastry house overlays;
- record the maximum angular shift of ASC/MC/cusps;
- flag any planet or angle that changes houses or crosses the descriptive aspect-orb boundary.

If no house placements change and angle shifts are small relative to the stated interpretation/orb, report the invariant result and state the remaining coordinate uncertainty. If any relevant assignment changes, report the alternatives instead of choosing the preferred narrative.

## Privacy

Do not commit third-party birth data, exact timestamps, or relationship records to the public repository when only the reusable method needs preservation.