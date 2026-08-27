from __future__ import annotations

from hdmatch.evaluation.redundancy import (
    RedundantProbe,
    structural_information_bits_from_probes,
)


def test_repeating_probe_cannot_inflate_structural_bits() -> None:
    probes = (
        RedundantProbe(probe_id="a", latent_construct_id="profile", behavioral_frame="life"),
        RedundantProbe(probe_id="b", latent_construct_id="profile", behavioral_frame="relations"),
    )
    candidates = ({"a": "1/3"}, {"a": "2/4"}, {"a": "2/4"})
    repeated_candidates = tuple({**row, "b": row["a"]} for row in candidates)
    once = structural_information_bits_from_probes(candidates, probes)
    repeated = structural_information_bits_from_probes(repeated_candidates, probes)
    assert repeated == once
    assert all(not probe.counts_as_independent_information for probe in probes)
