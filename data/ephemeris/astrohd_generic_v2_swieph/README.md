# AstroHD generic ephemeris cache v2 (SWIEPH)

Reusable coarse-scan longitude cache for HD / Western / AstroHD reverse matching. It starts ~101 days before the declared 100-year scan so HD Design times are covered. Houses are intentionally not cached because they are birthplace-specific and cheap to calculate.

Sampling: Moon 1h; Sun/Mercury/Venus/Mars/true Node 3h; Jupiter/Saturn 6h; Uranus/Neptune/Pluto 12h. Every calculation requests SWIEPH and checks returned ephemeris flags; any Moshier fallback aborts the build. Finalists and exact boundaries must be recalculated directly with the production ephemeris rather than trusted to interpolation.
