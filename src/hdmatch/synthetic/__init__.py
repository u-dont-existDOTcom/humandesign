"""Frozen-model synthetic case generation and declared noise tiers."""

from .generator import BlindSyntheticBundle, SyntheticGenerator
from .noise import NoiseTier, apply_noise

__all__ = ["BlindSyntheticBundle", "NoiseTier", "SyntheticGenerator", "apply_noise"]
