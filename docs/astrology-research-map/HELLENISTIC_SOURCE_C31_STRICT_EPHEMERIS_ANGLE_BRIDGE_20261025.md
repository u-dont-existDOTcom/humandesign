# C31 — Strict natal astronomy bridge and bounded Ascendant comparison

**25 October 2026. OWNER GOAL OPEN:** reconstruct source-defined natal/timing methods across the sixteen traditions, then freeze falsifiable person-level predictions before collecting untouched consenting human responses; compare against independent nonastrology and matched-chart baselines. The Hellenistic contribution remains a *development* lane. No participant birth record, real military outcome, retrospective biography, scoring deployment, or preregistration was used.

## Actual integrated work: reuse rather than invent astronomy

The C30 Dorothean **Lot of Expedition** needs three separate ecliptic longitudes: Ascendant, Moon, Saturn. The `humandesign` project already contains `hdmatch.chart.ephemeris.SwissEphemerisProvider`, a **fail-closed** Swiss source-file provider that hashes its local `.se1` files and verifies **FLG_SWIEPH** and the actual used ephemeris-file identity after each planetary calculation. Rather than reimplement that ephemeris, C31's [source bridge](hellenistic_c31_expedition_chart_bridge.py) calls the existing strict provider for Moon and Saturn, retaining source hashes, Swiss version, and exact returned decimal longitudes.

A live read-only **synthetic-only** test ran on five arbitrary, explicitly listed UTC time/location tuples using installed `pyswisseph` version **2.10.03** and the pinned local Swiss files:

| Declared file | SHA-256 of actual local bytes |
|---|---|
| `sepl_18.se1` | `ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66` |
| `semo_18.se1` | `1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7` |

The machine-readable [C31 synthetic astronomy receipt](HELLENISTIC_C31_SYNTHETIC_STRICT_ASTRONOMY_EVIDENCE_V1.json) records, for each anonymous/synthetic tuple: actual file-verified Moon/Saturn values, an explicitly **UNCERTIFIED** Swiss-computed Ascendant/MC, and the resulting purely documentary C30 lot condition. Its SHA-256 is `eb6c64f3a231e94a784225a975acab8a3d123fbd73d6e4e97a5bd4c5c91faa31`. [Reproduction script](generate_hellenistic_c31_synthetic_evidence.py) accepts an explicitly chosen directory of authorized Swiss files and makes **no network requests**.

**None of the five tuples represents a subject or an outcome validation.** They were chosen to probe calculations, not based on whether anyone served in a military campaign.

## The blocking angle was not silently promoted

The incumbent `hdmatch.relationship.western.placidus_houses` derives Ascendant and MC from a timezone-resolved UTC instant and lat/lon via `swisseph.houses_ex`. The project's live `tasks/ACTIVE-TASK.json` (`participant-session-v1`) and `docs/astronomy-reference-ablation-v1.md` explicitly preserve a **previous Ascendant/MC discrepancy** and bar angles/houses from strong confirmatory prediction until a full independent reference audit.

C31 keeps this **real owner/project boundary**: the Swiss houses output can be used for a **diagnostic Lot computation**, but the result is tagged `SWISS_HOUSES_ANGLE_NOT_INDEPENDENTLY_CERTIFIED`, `eligible_for_human_prediction=false`, and `actual_human_outcomes_evaluated=false`. The bridge explicitly rejects an unlabelled angle, an unverified mock planetary provider or an angle falsely described as certified. It did not change any production runner, real participant session or root task lock.

## Bounded independent geometry comparison

I separately coded a plain spherical-horizon intersection that does **not** call Swiss `houses`, `sidtime` or `julday`. It uses a Gregorian JD, mean-sidereal-time polynomial and mean obliquity. Both Ascendant and MC were calculated on five generic coordinate/date tuples, then compared with the Swiss `houses_ex` results:

- Max absolute **Ascendant** discrepancy: **0.32367 arcminutes**.
- Max absolute **MC** discrepancy: **0.20641 arcminutes**.

This suggests no gross sign/degree implementation error for those five **synthetic** reference points. It is **NOT** a full independent modern-angle certification: the second procedure treats UTC as UT1, does not model nutation/EOP, has an explicitly bounded 1583–2200 Gregorian horizon, has not been tested against the repository's previously disputed real case, and has not validated timezone folds or historical town locations. Small five-point errors do not permit declaring the full birth-coordinate chain correct.


## Birth-uncertainty handling now uses conservative closed enclosures

C30 correctly refused to infer stability from a finite sample of birth times. C31 adds `closed_lot_indicator_envelope`, which takes **continuous, unwrapped, closed bounds** for each of Ascendant, Moon, and Saturn and conservatively propagates them:

```text
LOT_MIN = ASC_MIN + MOON_MIN - SATURN_MAX
LOT_MAX = ASC_MAX + MOON_MAX - SATURN_MIN
```

The method checks *all zodiac sign bins crossed by the entire resulting interval*, rather than its endpoints only. It can therefore distinguish a positive indicator that remains positive over the **Capricorn→Aquarius** boundary from an unresolved **Sagittarius→Capricorn** boundary, or a **Pisces→Aries** 360° wrap. A span covering 360° is ambiguous. But the algorithm **does not itself create certified longitudes or prove that external envelopes cover all allowed birth timestamps/locations**. Without separately documented guaranteed bounds, output is **conditional**; even with an asserted bounds-certification flag, the C31 research pathway always returns `real_person_claim_allowed=false` while the angle audit remains open. This is not a silent alternate predictor.

The existing project already has separate source files and architecture for birth-time uncertainty and astronomical boundary solving. C31's interval operation is a narrowly scoped arithmetic adapter for the Dorothean lot, not a replacement chart engine, individual prediction model, or new mandatory owner gate.

## Owner-outcome readiness at this checkpoint

| Requirement | C31 admission |
|---|---|
| Literal Dorothean lot calculation and four-sign positive condition | **Implemented source-only** (C30) |
| Moon and Saturn from real pinned Swiss files with fallback rejection | **Executed and verified on five synthetic instants** |
| Ascendant from existing Swiss house code | **Executed for synthetic diagnostics; independent certification open** |
| Independent GMT/geometry sanity comparison | **Five synthetic checks, partial only** |
| Full IANA timezone/fold, UT1/EOP, geographic coordinates, and known disputed angle case | **OPEN** |
| Rigorous angle/birth-time range enclosure for an actual person | **OPEN** |
| Frozen prospective military campaign outcome operationalization with cohort and controls | **Draft, not preregistered** |
| Untouched human predictions/evaluation | **0** |
| Production model/scorer modifications | **0** |

The next useful engineering action is to locate and resolve the **known disputed Ascendant/MC reference case** using a genuinely independent astronomical algorithm with documented Earth-rotation, timezone and coordinate policies, then extend that parity across the intended study horizon and input-uncertainty range. Separately, assess whether military campaign participation can be reliably and ethically ascertained in a cohort with enough independent birth records and matched historical war exposure. If not, retain the C30 historical claim as an unvalidated development candidate and advance a different source-faithful measurable event—not a retrospectively tuned correction.

**No manuscript-search reset, no user-biography fitting, no task-lock mutation, no deployment, and no claims of measured human prediction.**


## Exact C31 validation receipt

- Full C31 `pyswisseph` environment: **17/17 new focused tests PASS**, including five live Swiss-angle synthetic comparisons and two source-only evidence replay checks.
- Full inherited + new Hellenistic source suite: **308/308 PASS** (**291** C30 inherited, **17** C31).
- Ordinary Python lacking optional `pyswisseph`: 17 tests still load, with the real Swiss-angle comparison explicitly **SKIPPED**; the machine evidence was previously generated from the real pinned provider.
- The synthetic file generator was rerun from the same two declared `.se1` files and produced **byte-identical JSON**; its SHA-256 stayed `eb6c64f3a231e94a784225a975acab8a3d123fbd73d6e4e97a5bd4c5c91faa31`.
- All these are **engineering, source-provenance and synthetic astronomical diagnostics**. Predictive validation on untouched consenting humans **remains 0**, and the independently disputed Asc/MC audit is explicitly **OPEN**.
