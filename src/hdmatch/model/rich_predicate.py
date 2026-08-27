"""Typed predicates for richer structural Human Design features.

These predicate classes only expose deterministic chart structure already present
in ``StructuralChartFeatures``.  They do not add behavioral mappings or weights.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SetPredicateOperator(StrEnum):
    CONTAINS_ANY = "contains_any"
    CONTAINS_ALL = "contains_all"
    NOT_CONTAINS_ANY = "not_contains_any"


class EqualityPredicateOperator(StrEnum):
    EQUALS_ANY = "equals_any"


ActivationSide = Literal["any", "personality", "design"]
ActivationBody = Literal[
    "sun",
    "earth",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
    "north_node",
    "south_node",
]


class ActivationGatePredicate(_FrozenModel):
    """Match active gates globally or within a personality/design/body scope."""

    kind: Literal["activation_gate"] = "activation_gate"
    operator: SetPredicateOperator
    gates: tuple[int, ...] = Field(min_length=1)
    side: ActivationSide = "any"
    bodies: tuple[ActivationBody, ...] = ()

    @field_validator("gates")
    @classmethod
    def canonical_gates(cls, gates: tuple[int, ...]) -> tuple[int, ...]:
        if any(gate < 1 or gate > 64 for gate in gates):
            raise ValueError("activation gates must be integers from 1 through 64")
        return tuple(sorted(set(gates)))

    @field_validator("bodies")
    @classmethod
    def canonical_bodies(
        cls, bodies: tuple[ActivationBody, ...]
    ) -> tuple[ActivationBody, ...]:
        return tuple(sorted(set(bodies)))

    def matches(self, chart: Mapping[str, Any] | object) -> bool:
        raw_activations = _chart_field(chart, "activation_gates")
        present: set[int] = set()
        if isinstance(raw_activations, Mapping):
            body_filter = set(self.bodies)
            for raw_key, raw_gate in raw_activations.items():
                parsed = _parse_activation_key(str(raw_key))
                if parsed is None:
                    continue
                side, body = parsed
                if self.side != "any" and side != self.side:
                    continue
                if body_filter and body not in body_filter:
                    continue
                try:
                    gate = int(raw_gate)
                except (TypeError, ValueError):
                    continue
                if 1 <= gate <= 64:
                    present.add(gate)
        return _match_set(self.operator, set(self.gates), present)

    def anchor_id_fragment(self) -> str:
        bodies = ",".join(self.bodies) if self.bodies else "*"
        gates = ",".join(str(gate) for gate in self.gates)
        return (
            f"activation_gate:{self.operator.value}:side={self.side}:"
            f"bodies={bodies}:gates={gates}"
        )


class ChannelPredicate(_FrozenModel):
    """Match complete channel identifiers already present on the bodygraph."""

    kind: Literal["channel"] = "channel"
    operator: SetPredicateOperator
    channels: tuple[str, ...] = Field(min_length=1)

    @field_validator("channels")
    @classmethod
    def canonical_channels(cls, channels: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sorted({_canonical_channel(channel) for channel in channels}))

    def matches(self, chart: Mapping[str, Any] | object) -> bool:
        raw_channels = _chart_field(chart, "channels")
        if raw_channels is None:
            present: set[str] = set()
        elif isinstance(raw_channels, str):
            try:
                present = {_canonical_channel(raw_channels)}
            except ValueError:
                present = set()
        else:
            present = set()
            try:
                for raw_channel in raw_channels:
                    try:
                        present.add(_canonical_channel(str(raw_channel)))
                    except ValueError:
                        continue
            except TypeError:
                present = set()
        return _match_set(self.operator, set(self.channels), present)

    def anchor_id_fragment(self) -> str:
        return f"channel:{self.operator.value}:{','.join(self.channels)}"


class DefinitionPredicate(_FrozenModel):
    """Match definition topology without changing the legacy coarse predicate schema."""

    kind: Literal["definition"] = "definition"
    operator: EqualityPredicateOperator = EqualityPredicateOperator.EQUALS_ANY
    definitions: tuple[str, ...] = Field(min_length=1)

    @field_validator("definitions")
    @classmethod
    def canonical_definitions(cls, definitions: tuple[str, ...]) -> tuple[str, ...]:
        normalized = {_normalize_token(value) for value in definitions}
        if "" in normalized:
            raise ValueError("definition values must contain letters or digits")
        return tuple(sorted(normalized))

    def matches(self, chart: Mapping[str, Any] | object) -> bool:
        raw_definition = _chart_field(chart, "definition")
        return _normalize_token(raw_definition) in set(self.definitions)

    def anchor_id_fragment(self) -> str:
        return f"definition:{self.operator.value}:{','.join(self.definitions)}"


RichChartPredicate = Annotated[
    ActivationGatePredicate | ChannelPredicate | DefinitionPredicate,
    Field(discriminator="kind"),
]


def _chart_field(chart: Mapping[str, Any] | object, field: str) -> Any:
    if isinstance(chart, Mapping):
        return chart.get(field)
    return getattr(chart, field, None)


def _parse_activation_key(raw_key: str) -> tuple[str, str] | None:
    side, separator, body = raw_key.partition(":")
    if not separator or side not in {"personality", "design"}:
        return None
    normalized_body = re.sub(r"[^a-z0-9]+", "_", body.casefold()).strip("_")
    if not normalized_body:
        return None
    return side, normalized_body


def _canonical_channel(raw_channel: str) -> str:
    match = re.fullmatch(r"\s*(\d{1,2})\s*[-/]\s*(\d{1,2})\s*", raw_channel)
    if match is None:
        raise ValueError(f"invalid channel identifier: {raw_channel!r}")
    left, right = (int(match.group(1)), int(match.group(2)))
    if not 1 <= left <= 64 or not 1 <= right <= 64 or left == right:
        raise ValueError(f"invalid channel gates: {raw_channel!r}")
    first, second = sorted((left, right))
    return f"{first}-{second}"


def _normalize_token(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).casefold()).strip("_")


def _match_set(
    operator: SetPredicateOperator, expected: set[Any], present: set[Any]
) -> bool:
    if operator is SetPredicateOperator.CONTAINS_ANY:
        return bool(expected & present)
    if operator is SetPredicateOperator.CONTAINS_ALL:
        return expected.issubset(present)
    if operator is SetPredicateOperator.NOT_CONTAINS_ANY:
        return not bool(expected & present)
    raise AssertionError(f"unsupported set predicate operator: {operator}")
