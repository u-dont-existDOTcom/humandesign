"""Pure detailed-feature extraction for the frozen Model B structural policy."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from hdmatch.chart.bodygraph import Definition
from hdmatch.model_b.artifacts import (
    SALIENCE_BY_LAYER,
    DetailedAnchor,
    DetailedLayer,
    ModelBArtifact,
)
from hdmatch.util import sha256_json


@dataclass(frozen=True, slots=True)
class _ActivationRecord:
    side: str
    body: str
    gate: int
    line: int

    @property
    def position(self) -> str:
        return f"{self.side}:{self.body}"


def extract_detailed_anchors(
    chart: Mapping[str, Any] | object,
    artifact: ModelBArtifact,
    *,
    include_unresolved_candidates: bool = True,
) -> tuple[DetailedAnchor, ...]:
    """Extract every declared detailed structure without creating behavioral support.

    Unresolved repeated/Node/hanging families can be emitted for transparent auditing
    and future source work.  Every returned anchor still carries
    ``behavioral_mapping_status=unresolved`` and therefore cannot score by itself.
    """

    anchors: list[DetailedAnchor] = []
    activations = _activations(chart)
    channels = _channels(chart)
    unknown_channels = channels - set(artifact.channel_catalog)
    if unknown_channels:
        raise ValueError(f"chart has channels outside frozen catalog: {sorted(unknown_channels)}")
    active_gates = {item.gate for item in activations}
    mechanically_complete = {
        channel
        for channel in artifact.channel_catalog
        if all(int(gate) in active_gates for gate in channel.split("-"))
    }
    if channels != mechanically_complete:
        raise ValueError(
            "chart channels are inconsistent with activation gates: "
            f"declared={sorted(channels)}, derived={sorted(mechanically_complete)}"
        )
    for channel in sorted(channels, key=_channel_sort_key):
        left, right = channel.split("-")
        anchors.append(
            _anchor(
                "MBF-COMPLETE-CHANNEL",
                DetailedLayer.COMPLETE_CHANNEL,
                f"complete_channel:{channel}",
                {"operator": "channel_present", "channel": channel},
                (f"channel:{channel}", f"gate:{left}", f"gate:{right}"),
            )
        )

    by_position = {item.position: item for item in activations}
    for position in artifact.cardinal_positions:
        activation = by_position.get(position)
        if activation is None:
            raise ValueError(f"chart is missing frozen cardinal position {position}")
        cardinal_dependency = f"cardinal_position:{position}"
        profile_dependency = f"profile_role_line:{activation.side}:{activation.line}"
        anchors.extend(
            (
                _anchor(
                    "MBF-CARDINAL-ACTIVATION",
                    DetailedLayer.CARDINAL_ACTIVATION,
                    f"cardinal_gate:{position}:{activation.gate}",
                    {
                        "operator": "activation_gate_equals",
                        "side": activation.side,
                        "body": activation.body,
                        "gate": activation.gate,
                    },
                    (
                        cardinal_dependency,
                        f"activation:{position}:gate:{activation.gate}",
                        f"gate:{activation.gate}",
                    ),
                ),
                _anchor(
                    "MBF-CARDINAL-ACTIVATION",
                    DetailedLayer.CARDINAL_ACTIVATION,
                    f"cardinal_line:{position}:{activation.line}",
                    {
                        "operator": "activation_line_equals",
                        "side": activation.side,
                        "body": activation.body,
                        "line": activation.line,
                    },
                    (
                        cardinal_dependency,
                        f"activation:{position}:line:{activation.line}",
                        profile_dependency,
                    ),
                ),
                _anchor(
                    "MBF-CARDINAL-ACTIVATION",
                    DetailedLayer.CARDINAL_ACTIVATION,
                    f"cardinal_gate_line:{position}:{activation.gate}.{activation.line}",
                    {
                        "operator": "activation_gate_line_equals",
                        "side": activation.side,
                        "body": activation.body,
                        "gate": activation.gate,
                        "line": activation.line,
                    },
                    (
                        cardinal_dependency,
                        f"activation:{position}:gate:{activation.gate}:line:{activation.line}",
                        f"gate:{activation.gate}",
                        profile_dependency,
                    ),
                ),
            )
        )

    definition = str(_read(chart, "definition") or "").strip()
    allowed_definitions = {item.value for item in Definition}
    if definition not in allowed_definitions:
        raise ValueError(f"chart has unknown Definition: {definition!r}")
    anchors.append(
        _anchor(
            "MBF-DEFINITION",
            DetailedLayer.DEFINITION,
            f"definition:{definition}",
            {"operator": "definition_equals", "value": definition},
            (f"definition:{definition}",),
        )
    )

    if include_unresolved_candidates:
        anchors.extend(_repeated_gate_candidates(activations, artifact))
        anchors.extend(_node_candidates(activations, artifact))
        anchors.extend(_prominent_candidates(activations, artifact))
        anchors.extend(_hanging_gate_candidates(activations, artifact))

    return tuple(sorted(anchors, key=lambda item: item.anchor_id))


def detailed_feature_sha256(
    chart: Mapping[str, Any] | object,
    artifact: ModelBArtifact,
    *,
    include_unresolved_candidates: bool = True,
) -> str:
    anchors = extract_detailed_anchors(
        chart,
        artifact,
        include_unresolved_candidates=include_unresolved_candidates,
    )
    return sha256_json([item.model_dump(mode="json") for item in anchors])


def matches_anchor(chart: Mapping[str, Any] | object, anchor: DetailedAnchor) -> bool:
    """Evaluate one emitted anchor against another chart deterministically."""

    predicate = anchor.predicate
    operator = predicate.get("operator")
    if operator == "channel_present":
        return str(predicate["channel"]) in _channels(chart)
    if operator == "definition_equals":
        return str(_read(chart, "definition")) == str(predicate["value"])
    if operator == "activation_gate_line_equals":
        return any(
            item.side == predicate["side"]
            and item.body == predicate["body"]
            and item.gate == predicate["gate"]
            and item.line == predicate["line"]
            for item in _activations(chart)
        )
    if operator == "activation_gate_equals":
        return any(
            item.side == predicate["side"]
            and item.body == predicate["body"]
            and item.gate == predicate["gate"]
            for item in _activations(chart)
        )
    if operator == "activation_line_equals":
        return any(
            item.side == predicate["side"]
            and item.body == predicate["body"]
            and item.line == predicate["line"]
            for item in _activations(chart)
        )
    if operator == "activation_gate_count_at_least":
        count = sum(item.gate == predicate["gate"] for item in _activations(chart))
        return count >= _predicate_int(predicate, "minimum_occurrences")
    if operator == "hanging_channel_edge":
        gates = {item.gate for item in _activations(chart)}
        active_gate = _predicate_int(predicate, "active_gate")
        missing_gate = _predicate_int(predicate, "missing_gate")
        return active_gate in gates and missing_gate not in gates
    raise ValueError(f"unknown Model B predicate operator: {operator!r}")


def _repeated_gate_candidates(
    activations: tuple[_ActivationRecord, ...], artifact: ModelBArtifact
) -> tuple[DetailedAnchor, ...]:
    counts = Counter(item.gate for item in activations)
    minimum = artifact.repeated_gate_minimum_occurrences
    return tuple(
        _anchor(
            "MBF-REPEATED-GATE",
            DetailedLayer.REPEATED_GATE,
            f"repeated_gate:{gate}:count_at_least:{minimum}",
            {
                "operator": "activation_gate_count_at_least",
                "gate": gate,
                "minimum_occurrences": minimum,
                "scoring_eligibility": "unresolved",
            },
            (f"gate:{gate}", f"repeated_gate:{gate}"),
        )
        for gate, count in sorted(counts.items())
        if count >= minimum
    )


def _node_candidates(
    activations: tuple[_ActivationRecord, ...], artifact: ModelBArtifact
) -> tuple[DetailedAnchor, ...]:
    by_position = {item.position: item for item in activations}
    result: list[DetailedAnchor] = []
    for position in artifact.node_positions:
        activation = by_position.get(position)
        if activation is None:
            raise ValueError(f"chart is missing frozen Node position {position}")
        result.append(
            _anchor(
                "MBF-THEMATIC-NODE",
                DetailedLayer.THEMATIC_NODE,
                f"node:{position}:{activation.gate}.{activation.line}",
                {
                    "operator": "activation_gate_line_equals",
                    "side": activation.side,
                    "body": activation.body,
                    "gate": activation.gate,
                    "line": activation.line,
                    "thematic_status": "unresolved",
                },
                (
                    f"activation:{position}:gate:{activation.gate}:line:{activation.line}",
                    f"gate:{activation.gate}",
                    f"node:{position}",
                ),
            )
        )
    return tuple(result)


def _prominent_candidates(
    activations: tuple[_ActivationRecord, ...], artifact: ModelBArtifact
) -> tuple[DetailedAnchor, ...]:
    result: list[DetailedAnchor] = []
    allowlist = set(artifact.prominent_activation_allowlist)
    for activation in activations:
        if activation.position not in allowlist:
            continue
        result.append(
            _anchor(
                "MBF-PROMINENT-ACTIVATION",
                DetailedLayer.PROMINENT_ACTIVATION,
                f"prominent:{activation.position}:{activation.gate}.{activation.line}",
                {
                    "operator": "activation_gate_line_equals",
                    "side": activation.side,
                    "body": activation.body,
                    "gate": activation.gate,
                    "line": activation.line,
                },
                (
                    f"activation:{activation.position}:gate:{activation.gate}:line:{activation.line}",
                    f"gate:{activation.gate}",
                ),
            )
        )
    return tuple(result)


def _hanging_gate_candidates(
    activations: tuple[_ActivationRecord, ...], artifact: ModelBArtifact
) -> tuple[DetailedAnchor, ...]:
    active_gates = {item.gate for item in activations}
    result: list[DetailedAnchor] = []
    for channel in artifact.channel_catalog:
        left, right = (int(item) for item in channel.split("-"))
        if (left in active_gates) == (right in active_gates):
            continue
        active, missing = (left, right) if left in active_gates else (right, left)
        result.append(
            _anchor(
                "MBF-HANGING-GATE",
                DetailedLayer.HANGING_GATE,
                f"hanging_gate:{active}:toward:{missing}",
                {
                    "operator": "hanging_channel_edge",
                    "active_gate": active,
                    "missing_gate": missing,
                    "channel": channel,
                    "scoring_eligibility": "unresolved",
                },
                (f"gate:{active}", f"channel-edge:{channel}"),
            )
        )
    return tuple(result)


def _anchor(
    family_id: str,
    layer: DetailedLayer,
    anchor_id: str,
    predicate: dict[str, object],
    dependency_keys: tuple[str, ...],
) -> DetailedAnchor:
    return DetailedAnchor(
        anchor_id=anchor_id,
        family_id=family_id,
        layer=layer,
        predicate=predicate,
        dependency_keys=dependency_keys,
        structural_salience=SALIENCE_BY_LAYER[layer],
    )


def _channels(chart: Mapping[str, Any] | object) -> set[str]:
    raw = _read(chart, "channels") or ()
    return {str(item) for item in raw}


def _activations(chart: Mapping[str, Any] | object) -> tuple[_ActivationRecord, ...]:
    raw = _read(chart, "activations")
    if not isinstance(raw, Mapping):
        raise ValueError("chart activations must be a mapping")
    result: list[_ActivationRecord] = []
    for key, value in raw.items():
        side = _read(value, "side")
        body = _read(value, "body")
        if side is None or body is None:
            key_side, separator, key_body = str(key).partition(":")
            if not separator:
                raise ValueError(f"activation {key!r} lacks side/body metadata")
            side = side or key_side
            body = body or key_body
        gate = int(_required(value, "gate", key))
        line = int(_required(value, "line", key))
        if not 1 <= gate <= 64 or not 1 <= line <= 6:
            raise ValueError(f"activation {key!r} has invalid gate/line {gate}.{line}")
        result.append(_ActivationRecord(side=str(side), body=str(body), gate=gate, line=line))
    positions = [item.position for item in result]
    if len(positions) != len(set(positions)):
        raise ValueError("chart activation positions must be unique")
    return tuple(sorted(result, key=lambda item: (item.side, item.body)))


def _required(value: Mapping[str, Any] | object, field: str, key: object) -> Any:
    result = _read(value, field)
    if result is None:
        raise ValueError(f"activation {key!r} is missing {field}")
    return result


def _predicate_int(predicate: Mapping[str, object], field: str) -> int:
    value = predicate.get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"predicate {field} must be an integer")
    return value


def _read(value: Mapping[str, Any] | object, field: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(field)
    return getattr(value, field, None)


def _channel_sort_key(value: str) -> tuple[int, int]:
    left, right = value.split("-")
    return int(left), int(right)
