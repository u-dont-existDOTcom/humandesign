"""Versioned mapping-library wrapper for richer structural chart predicates.

``mapping-library-v1`` remains untouched and continues to hash and parse exactly as
before.  This v2 wrapper is the opt-in schema for future independently supported
mappings over gates, channels, activations and definition topology.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from pydantic import Field

from hdmatch.model.mapping_library import ChartPredicate, MappingLibrary, MappingRule
from hdmatch.model.rich_predicate import RichChartPredicate


class RichMappingRule(MappingRule):
    chart_feature_predicate: ChartPredicate | RichChartPredicate | None = None

    @property
    def anchor_id(self) -> str:
        """Stable structural anchor while preserving every legacy v1 anchor ID."""

        predicate = self.chart_feature_predicate
        if predicate is None:
            raise ValueError("unresolved mappings have no structural anchor")
        if isinstance(predicate, ChartPredicate):
            values = ",".join(
                sorted(_normalize_feature(value) for value in predicate.values)
            )
            return f"{predicate.feature}:{predicate.operator.value}:{values}"
        return predicate.anchor_id_fragment()


class RichMappingLibrary(MappingLibrary):
    schema_version: Literal["mapping-library-v2"] = "mapping-library-v2"
    model_version: Literal["V4/V3.2-symbolic-v2-rich-structure"] = (
        "V4/V3.2-symbolic-v2-rich-structure"
    )
    mappings: tuple[RichMappingRule, ...] = Field(min_length=1)


def load_rich_mapping_library(path: str | Path) -> RichMappingLibrary:
    source = Path(path)
    return RichMappingLibrary.model_validate(json.loads(source.read_text(encoding="utf-8")))


def _normalize_feature(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).casefold())
