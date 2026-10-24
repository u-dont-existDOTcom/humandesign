"""Source-scoped constraints for historical primary-direction interpretations.

This registry is research EVIDENCE, not a forecast selector, model permission
system, or modification of any previously calculated geometric arcs.

Three different layers are kept apart:
1. Tycho Brahe, De Nova Stella (1573), Latin text preserved in the critical
   transcription edited by J.L.E. Dreyer: tekstnet /010/ folio G1r-G1v.
2. Placidus de Titis, Tabulae primi mobilis (1657): original edition catalogued,
   but original Latin folios not inspected in this checkpoint.
3. John Cooper's edited English translation Primum Mobile (1814),
   printed pp.23-25, PDF pp.40-42 in the Google-digitized edition:
   https://iapsop.com/ssoc/1814__cooper___primum_mobile.pdf

Cooper's 1814 translation says its Placidus thesis 61 excludes zodiacal rays
in converse, and thesis 60 excludes directing angles in converse. Therefore
the generic role-reversal + zodiacal-ray algorithm previously implemented is
NOT a historically source-supported *Placidus 1814* variant. We keep the math
available for other traditions but must not silently attribute it to Placidus.

Tycho's 1573 text supports variable TRUE daily movement and mapping an
equatorial arc to a symbolic year; the preserved Latin paragraph does not
specify the specific local-true-midnight sampling endpoints used in our
Brahe-labelled 2009-Gansten reconstruction.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class WitnessStatus(StrEnum):
    COMPATIBLE_SELECTED_RULE = "compatible_selected_rule"
    INCOMPATIBLE_WITNESS = "incompatible_witness"
    PARTIAL_SOURCE_SUPPORT = "partial_source_support"
    NOT_ESTABLISHED = "not_established"


@dataclass(frozen=True, slots=True)
class HistoricalWitnessAssessment:
    source_id: str
    status: WitnessStatus
    evidence: str
    limit: str

    def to_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "status": self.status.value,
            "evidence": self.evidence,
            "limit": self.limit,
        }


BRAHE_1573 = "tycho_brahe_de_nova_stella_1573_latin_critical_transcription"
PLACIDUS_1814 = "placidus_1657_via_cooper_1814_english_edited_translation"


def solar_key_source_assessment(profile: str) -> HistoricalWitnessAssessment:
    """Return exactly what the inspected passages support or leave uncertain."""
    if profile == "brahe_true_midnight_birth_day":
        return HistoricalWitnessAssessment(
            source_id=BRAHE_1573,
            status=WitnessStatus.PARTIAL_SOURCE_SUPPORT,
            evidence=(
                "Folio G1r: Brahe distinguishes true and varying planetary "
                "daily motion from uniform motion, and states a solar daily "
                "motion convention for equatorial year measures."
            ),
            limit=(
                "The inspected 1573 passage does NOT specify enclosing "
                "local true-solar midnight samples. Those endpoints and "
                "modern true-equator RA are a Gansten-informed reconstruction, "
                "not a verbatim procedure recovered from 1573."
            ),
        )
    if profile == "placidus_cumulative_true_solar_ra":
        return HistoricalWitnessAssessment(
            source_id=PLACIDUS_1814,
            status=WitnessStatus.COMPATIBLE_SELECTED_RULE,
            evidence=(
                "Cooper's edited translation printed pp.23-25, theses 58 "
                "and 65: the first subsequent solar day governs the first "
                "year, the second day the second year, etc., and the Sun's "
                "ascension in the direct sphere measures each interval."
            ),
            limit=(
                "This is the 1814 English edited translation, not a checked "
                "Latin 1657 transcription. Exact TT/UT, sidereal and "
                "calendar conventions of the original historical method "
                "remain unverified."
            ),
        )
    raise ValueError(f"unsupported inspected solar timing profile: {profile}")


def placidus_1814_role_assessment(
    construction: str, regime: str, *, moving_angle: bool = False
) -> HistoricalWitnessAssessment:
    """Witness appraisal WITHOUT restricting generic mathematical calculations.

    The actual engine keeps geometrical candidates independent of which author
    is later claimed to have accepted them. Future frozen historical profiles
    may require a stronger author-specific gate; this function is an evidence
    note and does not silently disable a working mathematical arm.
    """
    source = PLACIDUS_1814
    if regime == "traditional_role_reversed_converse" and moving_angle:
        return HistoricalWitnessAssessment(
            source_id=source,
            status=WitnessStatus.INCOMPATIBLE_WITNESS,
            evidence=(
                "Cooper translation printed p.23, thesis 60, forbids directing angles in converse."
            ),
            limit="Original 1657 Latin not checked.",
        )
    if regime == "traditional_role_reversed_converse" and construction == "zodiacal_promissor_ray":
        return HistoricalWitnessAssessment(
            source_id=source,
            status=WitnessStatus.INCOMPATIBLE_WITNESS,
            evidence=(
                "Cooper translation printed pp.23-24, theses 61-62, "
                "expressly excludes zodiacal rays in converse; "
                "only mundane rays/parallels are permitted in that account."
            ),
            limit=(
                "This is Placidus as represented by Cooper's 1814 edition. "
                "A generic role-reversed zodiacal ray is still a valid "
                "mathematical candidate, but must not be called "
                "'Placidus-compliant' on this witness."
            ),
        )
    if regime == "modern_reverse_rotation_diagnostic":
        return HistoricalWitnessAssessment(
            source_id=source,
            status=WitnessStatus.NOT_ESTABLISHED,
            evidence=(
                "Cooper translation thesis 59 distinguishes direct and "
                "converse, but does not describe our exact modern 360° "
                "complement model."
            ),
            limit="Absence of an attested modern rule is not proof it was historically impossible.",
        )
    return HistoricalWitnessAssessment(
        source_id=source,
        status=WitnessStatus.NOT_ESTABLISHED,
        evidence=(
            "No author-specific complete construction for this exact "
            "method/role pair was independently reconstructed in this pass."
        ),
        limit=(
            "Do not upgrade a broad geometric model to a historically "
            "endorsed Placidus profile without the relevant original canon."
        ),
    )
