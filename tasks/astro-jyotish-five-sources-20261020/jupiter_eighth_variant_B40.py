"""BPHS 26.12: source-claimed Jupiter 8th sign vs modern commentary repair.

Research comparison only. Neither variant is adopted for human forecasts.
"""
from bphs_special_aspect_B39 import bphs_sphuta_special

VERSIONS = frozenset({'sanskrit_literal', 'wilhelm_editorial_repair'})


def jupiter_aspect_virupas(angle: float, *, version: str) -> float:
    """Angle is the oriented (target - Jupiter) zodiacal separation [0, 360)."""
    if version not in VERSIONS:
        raise ValueError('Explicit source-version required')
    baseline = bphs_sphuta_special(angle, planet='Jupiter')
    d = float(angle)
    if version == 'wilhelm_editorial_repair' and 240 <= d < 270:
        return 15 + 1.5 * (270 - d)
    return baseline
