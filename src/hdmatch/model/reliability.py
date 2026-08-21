"""Measurement reliability primitives from V4 phase 1."""

from __future__ import annotations


def effective_confidence(behavioral_confidence: float, measurement_reliability: float) -> float:
    """Downweight established behavior by current measurement accessibility.

    Both inputs are bounded proportions. Multiplication means reliability can only
    preserve or remove evidence; it can never turn a mismatch into support.
    """

    for name, value in (
        ("behavioral_confidence", behavioral_confidence),
        ("measurement_reliability", measurement_reliability),
    ):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be in [0, 1]")
    return behavioral_confidence * measurement_reliability
