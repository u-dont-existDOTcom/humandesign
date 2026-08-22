"""Frozen zodiac-to-Rave-Mandala gate and line mapping.

Source notes
------------
* The project protocol requires a frozen offset, sequence, widths, and boundary
  convention: ``reference/core/human_design_reverse_matching_protocol_v4_1.md``
  section 18.4.
* Gate 41 beginning at exactly tropical longitude 302 degrees, and equal
  5.625-degree gate sectors, are tabulated at
  https://definedself.com/gates (retrieved 2026-08-21).
* Equal 0.9375-degree lines and the leading sequence
  ``41, 19, 13, 49, ...`` are independently described at
  https://www.gethumandesign.com/fr/docs/background/the-rave-mandala/
  (retrieved 2026-08-21).
* The rest of the cycle was cross-checked gate-by-gate against the dated wheel
  table at https://www.psychotronics.org/pub/dtr/gene-keys-by-birth-date.pdf
  (retrieved 2026-08-21).

The complete sequence below is the standard 64-position Rave wheel sequence.
The constants are data needed to reproduce a symbolic hypothesis; their
presence is not evidence that Human Design predicts human behavior.

The interval convention is half-open: a longitude exactly on a boundary belongs
to the new gate/line, i.e. ``[start, end)``.  Advanced Color/Tone/Base is
explicitly unavailable until independently validated constants are frozen.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from hashlib import sha256
from typing import Final, Literal

RAVE_MANDALA_VERSION: Final[str] = "rave-mandala-v1"
RAVE_MANDALA_START_DEGREES: Final[float] = 302.0
GATE_WIDTH_DEGREES: Final[float] = 360.0 / 64.0
LINE_WIDTH_DEGREES: Final[float] = GATE_WIDTH_DEGREES / 6.0

RAVE_GATE_ORDER: Final[tuple[int, ...]] = (
    41,
    19,
    13,
    49,
    30,
    55,
    37,
    63,
    22,
    36,
    25,
    17,
    21,
    51,
    42,
    3,
    27,
    24,
    2,
    23,
    8,
    20,
    16,
    35,
    45,
    12,
    15,
    52,
    39,
    53,
    62,
    56,
    31,
    33,
    7,
    4,
    29,
    59,
    40,
    64,
    47,
    6,
    46,
    18,
    48,
    57,
    32,
    50,
    28,
    44,
    1,
    43,
    14,
    34,
    9,
    5,
    26,
    11,
    10,
    58,
    38,
    54,
    61,
    60,
)

AdvancedSubstructureStatus = Literal["unavailable_unvalidated"]


@dataclass(frozen=True, slots=True)
class MandalaPosition:
    """A gate/line location using the frozen half-open wheel convention."""

    longitude: float
    gate: int
    line: int
    gate_index: int
    fraction_through_line: float
    color: None = None
    tone: None = None
    base: None = None
    advanced_substructure_status: AdvancedSubstructureStatus = "unavailable_unvalidated"


def normalize_longitude(longitude: float) -> float:
    """Return a finite longitude in the half-open interval ``[0, 360)``."""

    if not math.isfinite(longitude):
        raise ValueError("longitude must be finite")
    return longitude % 360.0


def longitude_to_gate_line(longitude: float) -> MandalaPosition:
    """Map tropical ecliptic longitude to an exact gate and line.

    Floating-point inputs that are mathematically exact boundaries (all frozen
    constants are exactly representable binary fractions) deterministically
    enter the new half-open sector.
    """

    normalized = normalize_longitude(longitude)
    relative = (normalized - RAVE_MANDALA_START_DEGREES) % 360.0
    gate_index = min(63, math.floor(relative / GATE_WIDTH_DEGREES))
    within_gate = relative - gate_index * GATE_WIDTH_DEGREES
    line_index = min(5, math.floor(within_gate / LINE_WIDTH_DEGREES))
    within_line = within_gate - line_index * LINE_WIDTH_DEGREES
    return MandalaPosition(
        longitude=normalized,
        gate=RAVE_GATE_ORDER[gate_index],
        line=line_index + 1,
        gate_index=gate_index,
        fraction_through_line=within_line / LINE_WIDTH_DEGREES,
    )


def line_boundary_longitudes() -> tuple[float, ...]:
    """Return all 384 normalized line-boundary longitudes in sorted order."""

    return tuple(
        sorted(
            (RAVE_MANDALA_START_DEGREES + index * LINE_WIDTH_DEGREES) % 360.0
            for index in range(384)
        )
    )


def gate_boundary_longitudes() -> tuple[float, ...]:
    """Return all 64 normalized gate-boundary longitudes in sorted order."""

    return tuple(
        sorted(
            (RAVE_MANDALA_START_DEGREES + index * GATE_WIDTH_DEGREES) % 360.0 for index in range(64)
        )
    )


def mandala_constants_sha256() -> str:
    """Hash the complete, version-relevant Mandala constant set."""

    payload = json.dumps(
        {
            "boundary_convention": "half_open_new_sector",
            "gate_order": RAVE_GATE_ORDER,
            "gate_width_degrees": GATE_WIDTH_DEGREES,
            "line_width_degrees": LINE_WIDTH_DEGREES,
            "start_degrees": RAVE_MANDALA_START_DEGREES,
            "substructure": "unavailable_unvalidated",
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload).hexdigest()


if len(RAVE_GATE_ORDER) != 64 or set(RAVE_GATE_ORDER) != set(range(1, 65)):
    raise RuntimeError("RAVE_GATE_ORDER must contain every gate exactly once")
