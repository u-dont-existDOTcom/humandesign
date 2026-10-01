# Historical timing guess freeze

Date: 2026-10-01
Status: development-only guesses. Do not inspect actual historical labels before ranking.

## Relationship high-pressure model

Targets:
- natal Venus;
- natal 7th ruler;
- ASC/DSC as one axis.

Timing:
- transiting Saturn, Uranus, Pluto: conjunction/square/opposition <=1 degree;
- secondary-progressed Mars: conjunction/square/opposition <=0.5 degree;
- solar-arc Mars, Saturn, Uranus, Pluto: conjunction/square/opposition <=0.5 degree.

Weights:
- Pluto transit 3.0; Uranus transit 2.5; Saturn transit 2.0;
- progressed Mars 2.0;
- solar-arc Mars/Pluto 2.5; solar-arc Saturn/Uranus 2.0;
- x1.2 monthly bonus when at least two timing families qualify.

Scan 2003-01 through 2026-09. This ranks symbolic relationship-pressure periods only.

## Child/family event model

Targets:
- natal 5th-house cusp;
- natal 5th-house ruler;
- natal Moon;
- natal Jupiter.

Timing:
- transiting Jupiter, Saturn, Uranus, Neptune, Pluto: major aspects <=1 degree;
- secondary-progressed Sun, Moon, Venus, Mars: major aspects <=0.5 degree;
- solar-arc Moon, Venus, Jupiter, ASC, MC: major aspects <=0.5 degree.

Weights:
- contact to 5th cusp or 5th ruler: 2.0;
- contact to Moon or Jupiter: 1.25;
- x1.3 in a 5th-house annual profection year;
- otherwise x1.15 when the annual ruler is Venus, Moon, or Jupiter;
- x1.2 monthly bonus when at least two timing families qualify.

Scan 2003-01 through 2026-09 and return the highest candidate period.

## Dependency controls

- Angle axes count once.
- Do not duplicate secondary-progressed Sun with solar-arc Sun.
- Same method/body/target/aspect counts once per month.
