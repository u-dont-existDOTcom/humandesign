"""Bounded references from Lilly's third-house section, 1647 Wellcome witness.

PDF223 and 225–226 (printed189 and 191–192) describe absent relatives;
PDF227–228 (printed193–194) distinguish news and advice question times.
These functions return source metadata and inclusive house arithmetic only.
They do not judge anyone's condition, assess a report, or calculate a chart.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import MappingProxyType


SOURCE_ID = "LILLY1647_WELLCOME_B30338724"

# Reuse the retained integer helper without changing its source or loading data.
# A standalone packet must preserve the sibling B02f/B02h directory structure.
_HELPER = Path(__file__).resolve().parent.parent / "B02f" / "lilly_presence_ship_reference.py"
_SPEC = importlib.util.spec_from_file_location("retained_lilly_house_arithmetic", _HELPER)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Cannot load retained house arithmetic: {_HELPER}")
_GEOMETRY = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_GEOMETRY)

_RELATIVES = MappingProxyType({
    "brother": (3, 223, 189, "brother"),
    "sibling": (3, 223, 189, "brother"),
    "father": (4, 225, 191, "father"),
    "child": (5, 226, 192, "child"),
    "son": (5, 226, 192, "son"),
    "daughter": (5, 226, 192, "daughter"),
    "servant": (6, 226, 192, "servant"),
})
_QUESTION_TIMES = MappingProxyType({
    "news_heard_by_self": (
        "first_hearing", "moment the questioner first hears the news or rumour", 227, 193
    ),
    "news_proposed_by_another": (
        "question_proposal", "exact moment another proposes the news question", 227, 193
    ),
    "advice_visit": (
        "advice_communication_begins",
        "moment the visitor first begins communicating the advice", 228, 194
    ),
})


def absent_relative_house_reference(relationship: str) -> dict:
    """Return both source frames for the named absent-relative inquiry only.

    ``turned_houses`` maps each relative house (1..12) to the original figure.
    The relative's own first house is counted inclusively. The original-figure
    sixth/eighth/twelfth references remain separate, as directed on PDF226.
    The source's instruction to vary rules is not an executable precedence
    rule here. ``sibling`` is an editorial input alias for the source's brother;
    child, son and daughter are all expressly named on PDF226.
    """
    if not isinstance(relationship, str):
        raise TypeError("relationship must be an explicit absent-relative name")
    if relationship not in _RELATIVES:
        raise ValueError(f"No absent-relative reference for {relationship!r}")
    origin, page, printed, source_name = _RELATIVES[relationship]
    return {
        "source_id": SOURCE_ID,
        "query_context": "absent_relative",
        "relationship": relationship,
        "source_relationship": source_name,
        "editorial_alias": relationship == "sibling",
        "querent_house": 1,
        "relative_ascendant_house": origin,
        "relation_source": {"pdf_page": page, "printed_page": printed},
        "turned_houses": {
            relative: _GEOMETRY.turned_house(origin, relative)
            for relative in range(1, 13)
        },
        "turning_convention": "inclusive_relative_house_to_original_figure",
        "turning_source": {"pdf_pages": [223, 225, 226], "printed_pages": [189, 191, 192]},
        "original_figure_references": {
            "houses": {6: "infirmity", 8: "death", 12: "imprisonment"},
            "source": {"pdf_page": 226, "printed_page": 192},
        },
        "frame_precedence": None,
        "frame_coexistence_note": (
            "PDF226 acknowledges each house's own sixth, eighth and twelfth, "
            "then assigns infirmity, death and imprisonment to the figure's "
            "sixth, eighth and twelfth. Both references are retained. How to "
            "vary the rules, and their interpretive precedence, remain unresolved."
        ),
        "interpretive_judgement_computed": False,
        "is_forecast": False,
    }


def question_time_reference(context: str) -> dict:
    """Describe a selected historical timing convention; do not select a time.

    Context must be explicit. These three source passages do not supply an
    implemented AI, message-receipt, timezone or civil-time conversion rule.
    """
    if not isinstance(context, str):
        raise TypeError("context must be an explicit source question context")
    if context not in _QUESTION_TIMES:
        raise ValueError(f"No question-time reference for {context!r}")
    anchor, description, page, printed = _QUESTION_TIMES[context]
    return {
        "source_id": SOURCE_ID,
        "context": context,
        "source": {"pdf_page": page, "printed_page": printed},
        "anchor": anchor,
        "anchor_description": description,
        "actual_timestamp_chosen": False,
        "chart_time_computed": False,
        "modern_interface_mapping": None,
        "is_forecast": False,
    }
