"""B53 source-only audit of printed 1929 Sarvartha Cintamani readings.

All functions are diagnostic mathematical / provenance fixtures, not natal
predictions or Sanskrit critical-edition adjudications. No participant data.
"""
from __future__ import annotations
from dataclasses import dataclass

YEAR = 1929
EDITION = "Mahidhara Sharma bhasha-tika (Bombay, archived DLI 2015.312429)"
PDF_SHA256 = "8fc0e8a5a212d1b3312363135347c47846671a3d184232eaf276ea0c96f57624"

@dataclass(frozen=True)
class VerseWitness:
    locator: str
    physical_pdf_pages: tuple[int, ...]
    printed_pages: tuple[int, ...]
    source_layer: str
    source_family: str
    visual_read: bool
    independent_manuscript: bool = False

    def __post_init__(self):
        if not self.physical_pdf_pages or len(self.physical_pdf_pages) != len(self.printed_pages):
            raise ValueError("Map every PDF page to a printed page")
        if not self.visual_read:
            raise ValueError("B53 entries must be physically inspected, not OCR-only")


def source_witnesses() -> tuple[VerseWitness, ...]:
    return (
        VerseWitness("8.1.2-3", (166,167), (148,149), "PRINTED_SANSKRIT", "BOMBAY_PRINT_FAMILY", True),
        VerseWitness("8.1.16", (168,), (150,), "PRINTED_SANSKRIT", "BOMBAY_PRINT_FAMILY", True),
        VerseWitness("8.1.24", (169,), (151,), "PRINTED_SANSKRIT", "BOMBAY_PRINT_FAMILY", True),
        VerseWitness("8.3.2", (171,), (153,), "PRINTED_SANSKRIT", "BOMBAY_PRINT_FAMILY", True),
        VerseWitness("8.3.10", (172,), (154,), "PRINTED_SANSKRIT", "BOMBAY_PRINT_FAMILY", True),
    )


def adverse_work_planets(tenth_lord: str) -> dict[str, object]:
    if tenth_lord not in {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}:
        raise ValueError("Choose one of seven classical rulers")
    return {"bhasin_english_v3": sorted({tenth_lord,"Jupiter","Mercury"}),
            "printed_sanskrit_v3": sorted({"Mercury","Jupiter","Venus"}),
            "score_allowed":False}


def sun_orders(sun_tenth: bool, mars_with_sun: bool, tenth_lord_angular: bool) -> dict[str, object]:
    if not all(type(v) is bool for v in (sun_tenth,mars_with_sun,tenth_lord_angular)):
        raise TypeError("Symbolic booleans required")
    return {"bhasin_english_and":sun_tenth and mars_with_sun and tenth_lord_angular,
            "sanskrit_va_candidate":(sun_tenth or mars_with_sun) and tenth_lord_angular,
            "sanskrit_grammar_arbitrated":False,"score_allowed":False}


def eleventh_conflict(malefic_in_11: bool, lord_11_in_angle_or_trine: bool) -> dict[str,object]:
    if not all(type(v) is bool for v in (malefic_in_11, lord_11_in_angle_or_trine)):
        raise TypeError("Symbolic booleans required")
    gains=malefic_in_11 or lord_11_in_angle_or_trine
    loses=malefic_in_11
    return {"v2_gain":gains,"v10_loss":loses,"overlap":gains and loses,
            "precedence_known":False,"score_allowed":False}


def reputation_versions(weak_afflicted_tenth_lord: bool) -> dict[str,object]:
    if type(weak_afflicted_tenth_lord) is not bool:
        raise TypeError("Symbolic bool required")
    return {"printed_1929": "FAVORABLE" if weak_afflicted_tenth_lord else "NOT_TRIGGERED",
            "bhasin_english":"UNFAVORABLE" if weak_afflicted_tenth_lord else "NOT_TRIGGERED",
            "canonical_conjectural_emendation":None,"score_allowed":False}


def source_scope() -> dict[str,object]:
    return {"independently_edited_sanskrit_manuscripts_verified":0,
            "physical_print_witnesses_verified":1,
            "translation_or_copy_reuses_count_as_independent_human_forecasts":False,
            "human_predictions_tested":0,"production_rules_promoted":0,
            "model_scoring_allowed":False}
