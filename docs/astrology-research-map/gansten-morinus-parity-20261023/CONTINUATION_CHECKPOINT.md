# Gansten × Morinus research checkpoint — 23 October 2026

**Parent owner outcome:** Continue Gansten primary-directions method integration and independent software comparison without repeating earlier Kindle reading or promoting a predictive model.

**Task state:** OPEN — a bounded, concrete source-method comparison has completed; wider software/historical verification and empirical testing remain open.

**Upstream comparison program:** Morinus Special Edition, `IngenieriaAstrologica/Morinus`, source commit `020492d5fce1c7a3d6b81186cef6cf04d93fb694`.

**Authoritative first read in this branch:** `MORINUS_SE_SOURCE_PARITY_REPORT_20261023.md`; then `MORINUS_AODO_DIAGNOSIS.json`, `MORINUS_PARITY.json`, `diagnose_aodo.py`, `compare_morinus_source.py`.

**Completed, verified in synthetic northern/east/above-conjunction domain:**
- Prior Gansten sample: all three independent method arcs reproduced by unchanged Morinus source routines (42.17434402835047°, 42.20081504892782°, 46.449117851278395°).
- Two deterministic samples totaling 3,600: semi-arcs 3,600/3,600; Regiomontanus 3,600/3,600; under-pole 3,564/3,600.
- Under-pole 36 discrepancies perfectly coincide with negative eastern AODO at the RA zero-crossing, and the error magnitude is twice |AODO|. A signed-coordinate diagnostic restores 3,600/3,600. This is not an upstream patch and not a full GUI/ephemeris run.
- The six research files were published on this isolated branch and each was read back byte-for-byte through authenticated GitHub connector.

**Source-level defect candidate:** `Morinus/placidianutppd.py` line 1668 uses `math.fabs(...[AODO])`. Its intended sign semantics may differ in western cases; do not apply a blanket patch, silently change historical methods, or use vendor results as universal golden data.

**Next authorized, outcome-serving work:** Test Morinus program through the actual unmodified GUI or a pinned full runtime if feasible with explicit program options and reproducible synthetic or independently chosen dated chart data, followed by cross-quadrant/hemisphere/converse/latitude/time-key tests. Preserve discrepancies and strict software-version attribution. A full live program run is not established by the present source-level test. No birth-event fitting, mortality prediction, or external public bug report.

**Blinding and implementation boundary:** Historical book attributions, computational parity, and evidence of prediction remain separate. No user or third-party birth data was used, no secrets, production chart engine or mappings changed, and no human prediction validated.

**Parent branch:** `research/gansten-source-geometry-crosswalk-20261023`.
**This isolated branch:** `research/gansten-morinus-se-source-parity-20261023`.

**Owner direct artifact:** `~/Téléchargements/gansten-astro/Morinus_Gansten_Source_Parity_20261023.zip` (verified CRC/SHA on user's Zorin laptop; original Morinus source not redistributed).
