"""Rules for repeated probes that measure one latent construct."""

from __future__ import annotations

import math
from collections.abc import Hashable, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field


class RedundantProbe(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    probe_id: str = Field(min_length=1)
    latent_construct_id: str = Field(min_length=1)
    behavioral_frame: str = Field(min_length=1)
    counts_as_independent_information: bool = False


def collapse_probe_answers(
    answers: Mapping[str, Hashable | None], probes: Sequence[RedundantProbe]
) -> dict[str, tuple[Hashable, ...]]:
    """Retain repeated evidence while exposing one value per latent construct."""
    grouped: dict[str, list[Hashable]] = {}
    known = {probe.probe_id for probe in probes}
    unknown = set(answers) - known
    if unknown:
        raise ValueError(f"answers contain unregistered probes: {sorted(unknown)}")
    for probe in probes:
        value = answers.get(probe.probe_id)
        if value is not None:
            grouped.setdefault(probe.latent_construct_id, []).append(value)
    return {key: tuple(values) for key, values in sorted(grouped.items())}


def structural_information_bits(
    candidate_latent_values: Sequence[Mapping[str, Hashable]],
) -> float:
    """Compute identity information from latent constructs, never probe count."""
    if not candidate_latent_values:
        raise ValueError("at least one candidate is required")
    keys = sorted({key for row in candidate_latent_values for key in row})
    fingerprints = [tuple(row.get(key) for key in keys) for row in candidate_latent_values]
    counts = {fingerprint: fingerprints.count(fingerprint) for fingerprint in set(fingerprints)}
    residual = (
        sum(math.log2(counts[fingerprint]) for fingerprint in fingerprints) / len(fingerprints)
    )
    return math.log2(len(fingerprints)) - residual


def structural_information_bits_from_probes(
    candidate_probe_values: Sequence[Mapping[str, Hashable]],
    probes: Sequence[RedundantProbe],
) -> float:
    """Collapse probe columns to dependency clusters before computing bits."""
    by_probe = {probe.probe_id: probe.latent_construct_id for probe in probes}
    if len(by_probe) != len(probes):
        raise ValueError("probe ids must be unique")
    collapsed: list[dict[str, Hashable]] = []
    for row in candidate_probe_values:
        unknown = set(row) - set(by_probe)
        if unknown:
            raise ValueError(f"candidate row contains unregistered probes: {sorted(unknown)}")
        latent: dict[str, Hashable] = {}
        for probe_id, value in row.items():
            construct = by_probe[probe_id]
            previous = latent.setdefault(construct, value)
            if previous != value:
                raise ValueError(
                    f"redundant probes disagree on structural value for {construct}"
                )
        collapsed.append(latent)
    return structural_information_bits(collapsed)
