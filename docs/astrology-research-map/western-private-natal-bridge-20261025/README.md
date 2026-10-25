# Private natal-to-direction bridge — fictional input verified with Swiss files

**25 October 2026.** This research-only module connects existing verified Swiss Ephemeris/primary-direction code to the earlier *separately named modern* prospective Western pilot. The real owner goal remains **OPEN**: compare independently frozen historically differentiated Western, Hellenistic, Jyotish, Chinese, Human Design and other astrology models against genuinely untouched human observations with independent controls. This branch does **not** claim the historical full Lilly/Argoli method, freeze an actual study, access a real person's birth data or predict a person's life events.

## What is implemented

`src/hdmatch/astrology/western_private_natal_bridge.py` reads only **externally supplied, previously normalized UTC** birth datetime, east-positive geographic coordinates, a nonidentifying pseudonymous label, recorded uncertainty in integer minutes, and a declared source-quality category. UTC normalization is NOT performed for unknown local timezones or historic DST; the tool fails closed on unnormalized local time. The accepted synthetic integration covers 1800–2399 and geographic latitudes −66° to +66° as supported by the underlying Swiss snapshot adapter.

It calculates **seven classical bodies from the pinned Swiss files**, checks **requested/returned SWIEPH mode** and the existing ephemeris file SHA-256s, projects the original four bodily and four zodiacal aspect-source candidates using the **Regiomontanian position-circle** research engine, modern software-direct sense and diagnostic **one degree/year** key. This is a *different* method from the previous proportional-semi-arc 96-chart occupancy analysis; its 0.4233% developmental coverage statistic is **not** applicable to the new Regiomontanian arm.

For every integer minute from negative through positive stated uncertainty, the tool recalculates and joins each uniquely named contact by source rule, aspect and ray branch. The full possible age span is preserved. Any contact that disappears at one sampled birth time or belongs to one of six unresolved source-status groups has **`timing = null`**, keeping possible range only for independent review. The discrete minute grid does not certify possible contacts throughout the *continuous* uncertainty interval. Two occupational body contacts retain **tentative** timing ranges, not validated predictions.

## Private input and keyed commitment

**The low entropy of a birth datetime makes bare SHA-256 unsafe as pseudonymization.** This adapter HMACs the entire normalized private record and all calculated natal feature vectors with an **external high-entropy secret of at least 32 bytes**, supplied through a local owner-only key file. Plain DOB, location, RA, declination, and calculated calendar date are **never written** into the receipt or the repository. The tool also records hashes of the source rule files, method config and calculation modules; the output includes only a pseudonym, source/method provenance, symbolic ages, source statuses and HMAC commitments.

For future authorized use, the private JSON must exist **outside Git**, with exactly this declared schema, using the recipient's independently verified normalized UTC coordinates:

```json
{
  "schema": "PRIVATE_WESTERN_NATAL_INPUT_V0",
  "pseudonymous_participant_id": "SYNTHETIC_TEST_CASE_001",
  "birth_utc": "2000-01-01T12:00:00+00:00",
  "latitude_deg": 40.0,
  "longitude_east_deg": -75.0,
  "birth_time_uncertainty_minutes": 1,
  "birth_time_quality": "unknown_or_rectified"
}
```

**All values above are deliberately fictional.** The file and the separate secret key must be created in an owner-only local directory outside the source checkout; `chmod 600` is enforced for both. Never commit those files. A pseudonym must be nonidentifying. The adapter requires a private absolute output path outside Git that does not already exist, creates the *sanitized* receipt with permissions `0600`, rejects symlinks and refuses an overwrite.

```sh
export PYTHONPATH="$PWD/src"
$HOME/humandesign/.venv/bin/python -m hdmatch.astrology.western_private_natal_bridge \
  --private-input /ABSOLUTE/PRIVATE/input.json \
  --secret-key-file /ABSOLUTE/PRIVATE/random-32-byte-key.bin \
  --ephemeris-dir "$HOME/.local/share/hdmatch/ephemeris/1800-2399" \
  --external-receipt /ABSOLUTE/PRIVATE/sanitized-receipt.json
```

The CLI does **not** print birth values, coordinates, planets or participant labels. Its synthetic-only tests exercise actual official Swiss files and verify the output cannot be written to a repository path. SHA-256 keys for public source files do *not* substitute for the private HMAC secret. No private key or real natal record was created in this research.

## What this does *not* establish

Generating a receipt **does not create an authenticated external timestamp or independent preregistration**, or certify consent, verified birth-time quality, confirmed local timezone, occupational eligibility, event detection, an N×N participant-by-chart score, or exchangeability of shuffled labels. The previous modern-pilot null calculator and source candidate register remain separate and unchanged. The complete authentic historical natal strength/converse rules are still under investigation. The original 1644 edition is uncollated.

**Engineering status:** strict Swiss + fictional natal adapter; unit/integration checks. **Human predictive accuracy: UNTESTED.** Continue from `CONTINUATION_CHECKPOINT.md` without using anyone's actual private birth/event history as a validation case.


## Completed verification

The private-input adapter's **15 synthetic-only focused tests** and the complete inherited **235-test Western source/method suite** passed with the actual pinned Swiss files. Ruff and mypy passed. Neither code nor tests required or inspected a real person's natal records. This is calculation, provenance and privacy-boundary verification, **not a measured predictive success rate**.

The README, method contract, exact code tests and checkpoint are included in the integrity manifest; the finished file packet has its own separate ZIP digest. The next participant-facing step requires independently authorized data/consent and actual blind scoring, not another unblinded test using development stories.
