# HumanDesign historical Western natal ephemeris parity, new isolated source-only engine research

**OPEN.** Starting from durable `fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4` 20 October 2026 after Chinese IANA/time research. The prior actual original Western source B07ax English Merchant Nativity contains exactly seven natal longitude positions in real 1647 and separately typeset 1659 printed editions, birth **19 September 1616**, printed **2 h 24 m 39 P.M.**, latitude **53°**. The exact birthplace/longitude, source local solar-time clock, Julian/Gregorian original birth-date time basis and biographical birth certificate remain unverified. The source author already knew the merchant; this is NEVER blind future prediction evidence.

Objective: compare the immutable seven printed 1647/1659 natal zodiac longitudes against an independently calculated modern astronomy ephemeris under two PREDECLARED Julian and Gregorian birth-calendar hypotheses. Preserve every residual; do not fit unknown longitude or UT to retrospectively improve outcomes. Compute one reference interpretation `14:24:39 UT` transparently as an unverified time-basis *hypothesis* (not claim this is the recorded true UT), with a declared ±2h sensitivity sample to establish which residuals remain unexplained within that bounded range.

SwissEph source: https://github.com/aloistr/swisseph, official April 2026 DE441 600-year 1200–1799 files `sepl_12.se1` and `semo_12.se1`, raw GitHub URLs pinned by SHA:
- /tmp/hd-western-swe-1616-20261020/sepl_12.se1 sha256 `8dccace2557601a223d5f8a7cf64de4e6bbb8a82b9b130b95a54d49adfbe546d`
- /tmp/hd-western-swe-1616-20261020/semo_12.se1 sha256 `1c65fdbb854f350d3de36afc3e4ac126a53f360ae4f6dcb57beed7c690e7eb61`.
Free `.se1` files are only downloaded outside repo; do not commit third-party binary/licensed ephemeris. Python swisseph `2.10.03` is already in owner venv `/home/joel/humandesign/.venv/bin/python`. REQUIRED: `swe.FLG_SWIEPH` requested and returned, `swe.FLG_MOSEPH` absent; silent fallbacks must fail. The very first attempt before official file provisioning returned only MOSEPH despite requesting SWIEPH; this status recorded as a source/provenance bug trap. Official two files subsequently downloaded and their SHA/bytes verified.

Original source witness `tasks/astro-source-audit-multipass-20261005/batches/B07ax/MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json` original seven exact body/sign/degree/minute values. Full first 1647 original Wellcome PDF hash `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b` preserved only as prior batch source record; no full original PDF or binary redistribution required.

Historical source registry accepted Lilly **13,044**, Ptolemy **1,066**, Chinese BaZi **210**, Zi Wei **220**. New source annotation count **0**, real human predictive validations **0**, model promotions **0**. Next Western source text **R13045 CLXXXI Marriage** remains open on a distinct source-only branch. Next BaZi **BZI-R0211**, Zi Wei **ZWD-R0221** unaltered.

Do not treat a calendar/longitude consistency check on a source-retrospective native as proof astrology describes actual people, predicts life outcomes or beats statistical/decoy baselines.

## Final computed original-versus-astronomy diagnostic

Modern Swiss Ephemeris `pyswisseph 2.10.03` + exact SHA-pinned Swiss planetary/Moon DE441 .se1 binaries recalculated **2 calendar interpretations ×7 printed classical planets ×5 assumed UT clock offsets = 70 positions**. **Every one** returned bitwise `FLG_SWIEPH`, none `FLG_MOSEPH`. A deliberate unit test forces Moshier fallback to ensure that is rejected. Swiss readme last updated 2026-04-14 https://github.com/aloistr/swisseph/blob/master/readme.md identifies these updated .se1 files as DE441-based. Do not claim that a requested flag alone confirms source use; returned flags and binary hashes are required. Downloaded ephemeris files remain in `/tmp/hd-western-swe-1616-20261020/`, NOT in the project repo.

Source original 1647/1659 printed 19 Sept 1616 2:24:39 PM, latitude53, but precise birth city, longitude, Julian Old Style confirmation on an independent birth certificate and original time-of-day basis all UNKNOWN. Calculation treats 14:24:39 UT as an illustrative UNVERIFIED clock interpretation. Sensitivity ±2 hours, no search for a best-fit subjective birth time.

Original printed Western planet values from `B07ax` photographic source:
- Saturn Taurus 9°02′; Julian modern residual −1.75788 arcminutes; Gregorian modern residual +31.14565′.
- Jupiter Sagittarius 21°55′; Julian −3.95534′; Gregorian −73.51489′.
- Mars Leo 0°54′; Julian −9.27809′; Gregorian −360.61536′ (computed Cancer).
- Sun Libra 6°37′; Julian **+6.68878′**; Gregorian **−583.13896′** (computed Virgo).
- Venus Libra 6°54′; Julian **+64.29367′**; Gregorian **−684.56841′** (computed Virgo).
- Mercury Libra 3°34′; Julian **+93.35419′**; Gregorian **−990.92589′** (computed Virgo).
- Moon Gemini 1°44′; Julian −1.00358′; Gregorian −8699.00683′ (computed Capricorn).

**7/7 zodiac signs match a Julian reading versus only 2/7 Gregorian**. Julian median absolute residual **6.68878′**, Gregorian median **583.13896′** at explicitly assumed 14:24:39 UT. For Mercury and Venus the original-versus-modern disagreement remains **greater than 50 arcminutes** for **all five ±2h positions**. These are meaningful *historical table/parity differences*, not a discovered actual person date of birth or verified 17th-century birth clock. Precise ephemeris settings, old book print and true UT are distinct unsolved uncertainty sources. The still-open original antiscion source conflict is independent: 1647+1659 print Mercury at Libra3°34′ but Pisces26°06′ antiscion where simple solstitial-axis arithmetic gives Pisces26°26′; do not merge this 20′ table error with the unrelated +93′ natal versus modern longitude residual.

Source and calculation evidence are `MERCHANT_1616_SOURCE_VS_SWISS_TROPICAL_V1.json` including exact 70 returned flags, all seven original source longitudes and seven×five residual grids, file hashes, date hypotheses, and explicit no-prediction flags. Script `compute_1616_merchant_swe_parity.py` recomputes only with exact original binary hashes and true SWIEPH flags. `test_merchant_swieph_source_1616.py` focused tests **13/13 passed**, including an original manually SHA-frozen 1647 source witness, printed Mercury antiscion mismatch, 70 flags, force-fallback failure and exact modern ephemeris recomputation. Source/identity/behavioral validity remains ZERO. No new historical annotations, no runtime promotions.
