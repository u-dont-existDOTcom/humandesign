"""Assembled, frozen v1b literature model.

The model has one theory-neutral feature and an empty astrology surface by Pro
decision.  It is available for engineering and development evaluation only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .contract import FrozenLiteratureContract, load_frozen_contract
from .features import BirthRecord, PairFeatures, build_pair_features
from .outcome import responses_to_pair_distance


@dataclass(frozen=True, slots=True)
class LiteratureModelV1:
    """Validated v1b contract plus its only executable feature path."""

    contract: FrozenLiteratureContract

    @classmethod
    def load(cls, repository_root: Path | str | None = None) -> LiteratureModelV1:
        return cls(contract=load_frozen_contract(repository_root))

    @property
    def model_version(self) -> str:
        return str(self.contract.model["model_version"])

    @property
    def executable_feature_ids(self) -> tuple[str, ...]:
        return ("TN-001",)

    @property
    def executable_astrology_feature_ids(self) -> tuple[str, ...]:
        return ()

    def pair_features(self, left: BirthRecord, right: BirthRecord) -> PairFeatures:
        return build_pair_features(
            left,
            right,
            protocol_version=self.contract.protocol_version,
            base_seed=self.contract.base_seed,
        )

    @staticmethod
    def outcome_distance(
        left_responses: dict[int, int],
        right_responses: dict[int, int],
    ) -> float:
        return responses_to_pair_distance(left_responses, right_responses)
