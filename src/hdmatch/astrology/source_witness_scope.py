"""Source-scoped primary-direction interpretation, edition separated.

Primary inspected witnesses:
* Brahe De Nova Stella (1573), Dreyer critical Latin transcription; Sun's
  variable daily motion, but natal local true-midnight endpoints not proved.
* Placidus Tabulae Primi Mobilis (1657), actual LATIN ORIGINAL PHOTO,
  BNC Rome copy, Internet Archive item bub_gb_3RHgMAUa5fMC:
  printed p11 (image leaf30), thesis 58, 60, 61, 62, 65.
  Printed p19 (image leaf48), directional-converse role canon.
* John Cooper's edited English Placidus translation (1814),
  printed pp23-25 (PDF pp40-42), previously independently inspected.

The original Latin directly confirms that Placidus's fixed significator
converse directions EXCLUDE zodiacal rays and directed angles, and that the
solar daily right-ascension advances are successive-year measures.
No author-specific interpretation is silently imposed on generic algorithms.

This registry is historical evidence, not a forecast model, a new geometric
method, or a production validation gate.
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
PLACIDUS_1657_LATIN = "placidus_tabulae_primi_mobilis_1657_original_latin_photographed"


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
            source_id=PLACIDUS_1657_LATIN,
            status=WitnessStatus.COMPATIBLE_SELECTED_RULE,
            evidence=(
                "The original Latin first edition, photographed printed p11, "
                "thesis 65, gives the Sun's first subsequent daily ascension "
                "in the direct sphere for year one, second day for year two, "
                "and so on. Thesis 58 relates successive natal days to years. "
                "The inspected 1814 Cooper edition agrees on these points."
            ),
            limit=(
                "Original 1657 Latin printed p11 was directly inspected in "
                "the Rome copy, not the complete original work. Its wording "
                "does not specify modern SWIEPH TT/UT, geographic timezone, "
                "or all fractional-day/calendar conventions. The earlier "
                "1814 translation remains an independent comparison."
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
            limit=(
                "The 1657 photographed Latin original p11, thesis 60, "
                "agrees; this assessment remains explicitly tied to "
                "the separate 1814 English edition."
            ),
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
                "The independently inspected 1657 original Latin printed "
                "p11, theses 61-62, corroborates the exclusion. "
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


def placidus_1657_latin_role_assessment(
    construction: str, regime: str, *, moving_angle: bool = False
) -> HistoricalWitnessAssessment:
    """Appraise one motion construction against the DIRECT Latin 1657 edition.

    Based on photographed 1657 printed p11 (theses 59-65) and p19
    (direction canon), not only on the edited 1814 English rendering.
    This does not prohibit mathematically meaningful arms for other authors.
    """
    if regime == "traditional_role_reversed_converse" and moving_angle:
        return HistoricalWitnessAssessment(
            source_id=PLACIDUS_1657_LATIN,
            status=WitnessStatus.INCOMPATIBLE_WITNESS,
            evidence=(
                "First-edition 1657 Latin printed p11, thesis 60: "
                "'motu conuerso non possunt dirigi Cardines'."
            ),
            limit=(
                "Applies to Placidus's specific motion rules in his 1657 text, "
                "not to the general mathematical possibility of moving a natal "
                "zodiacal degree in other systems."
            ),
        )
    if regime == "traditional_role_reversed_converse" and construction == "zodiacal_promissor_ray":
        return HistoricalWitnessAssessment(
            source_id=PLACIDUS_1657_LATIN,
            status=WitnessStatus.INCOMPATIBLE_WITNESS,
            evidence=(
                "First-edition Latin 1657 printed p11, theses 61-62: "
                "converse permits rays and parallels in mundo, but "
                "'nullo modo in zodiaco'."
            ),
            limit=(
                "Specific to Placidus 1657. The separately implemented "
                "generic reverse-role zodiacal ray remains a mathematical "
                "candidate, not an authenticated Placidus configuration."
            ),
        )
    if regime == "modern_reverse_rotation_diagnostic":
        return HistoricalWitnessAssessment(
            source_id=PLACIDUS_1657_LATIN,
            status=WitnessStatus.NOT_ESTABLISHED,
            evidence=(
                "The photographed 1657 first-edition printed p19 describes "
                "the significator moving toward fixed promissor in converse. "
                "It does not supply the modern no-role-swap 360-degree "
                "complement model."
            ),
            limit="No inferred universal claim about later or other traditions.",
        )
    return HistoricalWitnessAssessment(
        source_id=PLACIDUS_1657_LATIN,
        status=WitnessStatus.NOT_ESTABLISHED,
        evidence=(
            "Theses 58-65 and the p19 canon were inspected; a complete "
            "author-specific algorithm for this specific geometry has not "
            "been fully established from this subset."
        ),
        limit=(
            "Do not present a generic geometry profile as fully authenticated "
            "Placidus without checking all relevant original canons."
        ),
    )
