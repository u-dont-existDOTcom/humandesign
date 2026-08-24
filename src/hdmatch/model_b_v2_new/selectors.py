"""Pure evaluation of preregistered detailed selectors.

Selectors inspect only candidate chart structure.  They have no access to birth
truth, ranks, answer keys, or evaluation outcomes.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from hdmatch.chart.bodygraph import CHANNELS, GATE_TO_CENTER
from hdmatch.model_b.types import ChartPredicate, ConditioningDimension

from .artifacts import (
    CompleteChannelSelector,
    DefinitionSelector,
    DetailedSelector,
    ExactActivationSelector,
    ExactNodeSelector,
    ParentDimension,
    ProminentActivationSelector,
    QualifiedHangingPersonalityEdgeSelector,
    RepeatedGateSelector,
    selector_anchor_id,
)

CANONICAL_CHANNELS = frozenset(channel.identifier for channel in CHANNELS)


@dataclass(frozen=True, slots=True)
class ActivationRecord:
    side: str
    body: str
    gate: int
    line: int

    @property
    def position(self) -> str:
        return f"{self.side}:{self.body}"


@dataclass(frozen=True, slots=True)
class SelectorPredicate(ChartPredicate):
    selector: DetailedSelector

    def matches(self, chart: object) -> bool:
        return selector_matches(chart, self.selector)


@dataclass(frozen=True, slots=True)
class ParentDimensionExtractor(ConditioningDimension):
    dimension: ParentDimension

    @property
    def dimension_id(self) -> str:
        return self.dimension.value

    def value(self, chart: object) -> str:
        field = (
            "channels"
            if self.dimension is ParentDimension.COMPLETE_CHANNELS
            else self.dimension.value
        )
        raw = _read(chart, field)
        if raw is None:
            raise ValueError(f"chart is missing conditional dimension {self.dimension.value}")
        if self.dimension is ParentDimension.DEFINED_CENTERS:
            values: tuple[str, ...]
            if isinstance(raw, str):
                values = (raw,)
            else:
                try:
                    values = tuple(str(item) for item in raw)
                except TypeError as error:
                    raise ValueError("defined_centers must be iterable") from error
            return ",".join(sorted(_enum_value(item) for item in values))
        if self.dimension is ParentDimension.COMPLETE_CHANNELS:
            channels: tuple[str, ...]
            if isinstance(raw, str):
                channels = (raw,)
            else:
                try:
                    channels = tuple(str(item) for item in raw)
                except TypeError as error:
                    raise ValueError("channels must be iterable") from error
            unknown = set(channels) - CANONICAL_CHANNELS
            if unknown:
                raise ValueError(f"chart contains noncanonical channels: {sorted(unknown)}")
            return ",".join(sorted(channels, key=_channel_sort_key))
        return _enum_value(raw)


def validate_selector_mechanics(selector: DetailedSelector) -> None:
    """Reject structurally impossible selectors before compilation."""

    if isinstance(selector, CompleteChannelSelector):
        _require_channel(selector.channel)
        return
    if isinstance(selector, QualifiedHangingPersonalityEdgeSelector):
        _require_channel(selector.channel)
        return


def selector_matches(chart: object, selector: DetailedSelector) -> bool:
    """Evaluate one frozen selector against one chart, fail-closing malformed charts."""

    if isinstance(selector, CompleteChannelSelector):
        _require_channel(selector.channel)
        return selector.channel in _channels(chart)

    if isinstance(selector, ExactActivationSelector):
        activation = _activation_by_position(chart).get(f"{selector.side}:{selector.body}")
        if activation is None:
            raise ValueError(
                f"chart is missing required activation {selector.side}:{selector.body}"
            )
        gate_matches = selector.gate is None or activation.gate == selector.gate
        line_matches = selector.line is None or activation.line == selector.line
        gate_center_defined = GATE_TO_CENTER[activation.gate].value in _defined_centers(chart)
        return gate_matches and line_matches and gate_center_defined

    if isinstance(selector, DefinitionSelector):
        definition = _read(chart, "definition")
        if definition is None:
            raise ValueError("chart is missing Definition")
        return _enum_value(definition) == selector.definition

    if isinstance(selector, RepeatedGateSelector):
        activations = _activations(chart)
        count = sum(item.gate == selector.gate for item in activations)
        personality_count = sum(
            item.gate == selector.gate and item.side == "personality" for item in activations
        )
        center_defined = GATE_TO_CENTER[selector.gate].value in _defined_centers(chart)
        return count >= selector.minimum_occurrences and personality_count >= 1 and center_defined

    if isinstance(selector, ExactNodeSelector):
        activation = _activation_by_position(chart).get(f"{selector.side}:{selector.body}")
        if activation is None:
            raise ValueError(f"chart is missing required Node {selector.side}:{selector.body}")
        return activation.gate == selector.gate and (
            selector.line is None or activation.line == selector.line
        )

    if isinstance(selector, ProminentActivationSelector):
        activation = _activation_by_position(chart).get(f"{selector.side}:{selector.body}")
        if activation is None:
            raise ValueError(f"chart is missing prominent position {selector.side}:{selector.body}")
        center_defined = GATE_TO_CENTER[selector.gate].value in _defined_centers(chart)
        return activation.gate == selector.gate and center_defined

    if isinstance(selector, QualifiedHangingPersonalityEdgeSelector):
        _require_channel(selector.channel)
        activations = _activations(chart)
        active_on_personality = any(
            item.side == "personality" and item.gate == selector.active_gate for item in activations
        )
        all_gates = {item.gate for item in activations}
        defined_centers = _defined_centers(chart)
        active_center = GATE_TO_CENTER[selector.active_gate].value
        return (
            active_on_personality
            and selector.missing_complement_gate not in all_gates
            and active_center in defined_centers
        )

    raise AssertionError(f"unsupported selector type: {type(selector).__name__}")


def selector_predicate(selector: DetailedSelector) -> SelectorPredicate:
    return SelectorPredicate(selector=selector)


def parent_dimension_extractors(
    dimensions: tuple[ParentDimension, ...],
) -> tuple[ParentDimensionExtractor, ...]:
    return tuple(ParentDimensionExtractor(dimension=item) for item in dimensions)


def active_gate_counts(chart: object) -> Mapping[int, int]:
    """Expose deterministic counts for diagnostics without revealing response data."""

    return dict(sorted(Counter(item.gate for item in _activations(chart)).items()))


def structural_signature(chart: object, selectors: tuple[DetailedSelector, ...]) -> tuple[str, ...]:
    """Stable identity of matching V2 anchors for cache/ranking discrimination."""

    return tuple(
        sorted(
            selector_anchor_id(selector)
            for selector in selectors
            if selector_matches(chart, selector)
        )
    )


def _channels(chart: object) -> frozenset[str]:
    raw = _read(chart, "channels")
    if raw is None:
        raise ValueError("chart is missing channels")
    if isinstance(raw, str):
        result = frozenset({raw})
    else:
        try:
            result = frozenset(str(item) for item in raw)
        except TypeError as error:
            raise ValueError("chart channels must be iterable") from error
    unknown = result - CANONICAL_CHANNELS
    if unknown:
        raise ValueError(f"chart contains noncanonical channels: {sorted(unknown)}")
    return result


def _defined_centers(chart: object) -> frozenset[str]:
    raw = _read(chart, "defined_centers")
    if raw is None:
        raise ValueError("chart is missing defined_centers")
    if isinstance(raw, str):
        values = (raw,)
    else:
        try:
            values = tuple(raw)
        except TypeError as error:
            raise ValueError("defined_centers must be iterable") from error
    return frozenset(_enum_value(item) for item in values)


def _activation_by_position(chart: object) -> dict[str, ActivationRecord]:
    result = {item.position: item for item in _activations(chart)}
    if len(result) != len(_activations(chart)):
        raise ValueError("chart activation positions must be unique")
    return result


def _activations(chart: object) -> tuple[ActivationRecord, ...]:
    raw = _read(chart, "activations")
    if not isinstance(raw, Mapping):
        raise ValueError("chart activations must be a mapping")
    result: list[ActivationRecord] = []
    for key, value in raw.items():
        side = _read(value, "side")
        body = _read(value, "body")
        if side is None or body is None:
            key_side, separator, key_body = str(key).partition(":")
            if not separator:
                raise ValueError(f"activation {key!r} lacks side/body metadata")
            side = side or key_side
            body = body or key_body
        gate = _required_int(value, "gate", key)
        line = _required_int(value, "line", key)
        if str(side) not in {"personality", "design"}:
            raise ValueError(f"activation {key!r} has invalid side")
        if not 1 <= gate <= 64 or not 1 <= line <= 6:
            raise ValueError(f"activation {key!r} has invalid gate/line {gate}.{line}")
        result.append(
            ActivationRecord(side=str(side), body=_enum_value(body), gate=gate, line=line)
        )
    return tuple(sorted(result, key=lambda item: (item.side, item.body)))


def _required_int(value: object, field: str, key: object) -> int:
    raw = _read(value, field)
    if raw is None or isinstance(raw, bool):
        raise ValueError(f"activation {key!r} is missing a valid {field}")
    try:
        return int(raw)
    except (TypeError, ValueError) as error:
        raise ValueError(f"activation {key!r} has non-integer {field}") from error


def _read(value: object, field: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(field)
    return getattr(value, field, None)


def _enum_value(value: object) -> str:
    raw = getattr(value, "value", value)
    return str(raw).strip()


def _require_channel(channel: str) -> None:
    if channel not in CANONICAL_CHANNELS:
        raise ValueError(f"selector uses a noncanonical Human Design channel: {channel}")


def _channel_sort_key(value: str) -> tuple[int, int]:
    left, right = value.split("-")
    return int(left), int(right)
