Most of the plan is ready to freeze. I found four things to fix first. I only had this message to go on: I didn't have the packet, the event lists or `scripts/partner_future_pilot.py`, so I couldn't recompute any numbers.

## Fix before freezing

**1. The 2040–41 window runs past what the timing generator covers.**
The generator ran for 2026–2040, so 2041 has no computed events. Either rerun it through the end of 2041 or cut the window to 2040. The 2020–2024 window has a related gap. Its dates, including the 2023-03-06 Saturn return, come from an earlier run. Regenerate that window with the same pinned script, ephemeris files, orbs and target list as 2026–2040, so all windows are built the same way. Freeze the full event lists (all 326 transit and 46 progression events, plus 2020–24 and 2041), with a hash, not just the key dates.

**2. Part of the 2026–27 window has already happened.**
Today is 2026-10-03, so January to early October 2026 is in the past, the same as 2020–2024. Split that window at the freeze date, or label the elapsed part retrospective-blind. Otherwise any match there would be counted as a correct forecast when it was really a look back.

**3. The fusion step can double-count age-driven markers.**
- The Saturn return in 2023, Pinnacle 2→6 at age 29 (which happens at 36 minus a Life Path of 7), and the Period change around age 27–30 in 2024 all happen at roughly the same age for everyone born near this date. They are not independent evidence, and they shouldn't count as convergence just because they cluster in 2023–24.
- The same applies to timing. You already treat Moon, Venus, Jupiter and the MC as one group in the natal chart. A single transit or progression over the MC/IC axis also hits the Moon conjunction, the Venus opposition and the Jupiter square. Count that as one hit when deciding window strength, not three or four.

**4. Some dates depend on the exact birth time, but nothing flags that.**
- The angle contacts are very tight (Moon conjunct MC is 0.555°). The MC moves about 1° every 4 minutes of birth time.
- In secondary progressions, 1° of the angles is roughly a year, so a few minutes' error moves progressed-angle dates by about a year.
- Add the birth-time source and its accuracy to the freeze. Mark any of the 46 progression events that involve the ASC or MC, and the angle contacts, as birth-time sensitive, with a ± range of dates.
- This doesn't apply to sidereal Mercury at 29.56 Capricorn, which is correctly labelled convention-sensitive.

## Wording fix only, not a recalculation

V1.4 gives a flat −1 to Mercury, Venus and Mars, and that score can stay as frozen. But Venus is 2.6° from the Sun, which counts as combust in the usual convention (within about 8.5°), not merely "under the beams" (within about 17°). Base each planet's label on its actual distance from the Sun so the text doesn't blur the two states.

## No issue found

Points 1, 3, 5, 6, 7, 8 and 9 are consistent as you've stated them. That includes the ≤1° conjunction rule, the 3rd-house +1, Jupiter and Saturn as transit targets, no dasha, Lahiri only, no Lot of Fortune, and the Decoz timing (Period change in 2024, Pinnacle change in 2023). Once the four items above are fixed, I see nothing else material blocking the freeze.
