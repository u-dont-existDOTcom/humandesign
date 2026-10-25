"""G35 source-qualified Gene Keys / Human Design chart-geometry crosswalk.

This is NOT an independently verified official Gene Keys chart, an extraction
of proprietary 64 Shadow/Gift/Siddhi texts, a genetic mechanism, or a
personality prediction. Reuse the incumbent HD Rave Mandala and the
incumbent exact 88° pre-natal solar-arc chart data, preserving that the
official Gene Keys webpages alternate between '88 degrees' and '88 days'.

Core Golden Path 11 spheres are mapped directly from official Gene Keys
birth/design planetary correlations, three optional spheres separately
marked non-core. DO NOT count this as a statistically independent 17th
astronomical tradition relative to Human Design.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Iterable

_ROOT = Path(__file__).resolve().parents[2]
_SOURCE = str(_ROOT / "src")
if _SOURCE not in sys.path:
    sys.path.insert(0, _SOURCE)

from hdmatch.chart.bodygraph import GateActivation
from hdmatch.chart.calculator import ChartComputation
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.rave_mandala import (
    RAVE_GATE_ORDER, longitude_to_gate_line, mandala_constants_sha256
)


@dataclass(frozen=True)
class SphereSpec:
    slug: str
    title: str
    birth_layer: str
    body: CelestialBody
    sequences: tuple[str, ...]
    source_status: str


# Official Gene Keys mappings: https://genekeys.com/docs/
# what-planets-does-each-sphere-of-the-golden-path-profile-correlate-to/
CORE_11: tuple[SphereSpec, ...] = (
    SphereSpec("lifes_work","Life's Work / Brand","personality",CelestialBody.SUN,
               ("activation","pearl"),"core"),
    SphereSpec("evolution","Evolution","personality",CelestialBody.EARTH,
               ("activation",),"core"),
    SphereSpec("radiance","Radiance","design",CelestialBody.SUN,
               ("activation",),"core"),
    SphereSpec("purpose","Purpose","design",CelestialBody.EARTH,
               ("activation","venus"),"core"),
    SphereSpec("attraction","Attraction","design",CelestialBody.MOON,
               ("venus",),"core"),
    SphereSpec("iq","IQ","personality",CelestialBody.VENUS,
               ("venus",),"core"),
    SphereSpec("eq","EQ","personality",CelestialBody.MARS,
               ("venus",),"core"),
    SphereSpec("sq","SQ","design",CelestialBody.VENUS,
               ("venus",),"core"),
    SphereSpec("core_vocation","Core / Vocation","design",CelestialBody.MARS,
               ("venus","pearl"),"core"),
    SphereSpec("culture","Culture","design",CelestialBody.JUPITER,
               ("pearl",),"core"),
    SphereSpec("pearl","Pearl","personality",CelestialBody.JUPITER,
               ("pearl",),"core"),
)

# Official page also includes these after the 11 traditional Golden Path
# spheres, but separately notes future sequences. Do not silently treat
# additional spheres as one of the 11 original.
SUPPLEMENTARY_3: tuple[SphereSpec, ...] = (
    SphereSpec("creativity","Creativity","design",CelestialBody.URANUS,
               ("supplementary",),"extended"),
    SphereSpec("relating","Relating","personality",CelestialBody.MERCURY,
               ("supplementary",),"extended"),
    SphereSpec("stability","Stability","design",CelestialBody.SATURN,
               ("supplementary",),"extended"),
)

CORE_SEQUENCE_ORDER = {
    "activation": ("lifes_work","evolution","radiance","purpose"),
    "venus": ("purpose","attraction","iq","eq","sq","core_vocation"),
    "pearl": ("core_vocation","culture","lifes_work","pearl"),
}


def canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf8")


def digest(obj: dict) -> str:
    return sha256(canonical(obj)).hexdigest()


def wheel_programming_partner(gate: int) -> int:
    """The same wheel's directly opposite hexagram is not independent."""
    if type(gate) is not int or gate not in RAVE_GATE_ORDER:
        raise ValueError("integer gate 1..64 required")
    idx = RAVE_GATE_ORDER.index(gate)
    return RAVE_GATE_ORDER[(idx + 32) % 64]


def _normalize(activations: Iterable[GateActivation],
               *, supplementary: bool) -> dict:
    specs = CORE_11 + (SUPPLEMENTARY_3 if supplementary else ())
    if len({s.slug for s in specs}) != len(specs):
        raise AssertionError("duplicate official sphere slug")
    seen: dict[tuple[str,CelestialBody], GateActivation] = {}
    for activation in activations:
        if not isinstance(activation, GateActivation):
            raise ValueError("only existing GateActivation typed input")
        key=(activation.side,activation.body)
        if key in seen:
            raise ValueError("duplicate same-body/same-side input")
        # Do not accept labels inconsistent with exact repository mandala.
        expected=longitude_to_gate_line(activation.longitude)
        if (activation.gate,activation.line)!=(expected.gate,expected.line):
            raise ValueError("gate or line conflicts with source longitude")
        seen[key]=activation
    missing=[s.slug for s in specs
             if (s.birth_layer,s.body) not in seen]
    if missing:
        raise ValueError("missing required profile sphere activations: " +
                         ",".join(missing))
    spheres=[]
    for spec in specs:
        a=seen[(spec.birth_layer,spec.body)]
        spheres.append({
            "slug":spec.slug,
            "title":spec.title,
            "planetary_layer":spec.birth_layer,
            "body":spec.body.value,
            "gate_gene_key_number":a.gate,
            "line":a.line,
            "source_status":spec.source_status,
            "sequences":list(spec.sequences),
            "reuse_original_hd_gate_and_line":True,
            "gk_interpretative_phrases_not_licensed_or_included":True,
        })
    byslug={x["slug"]:x for x in spheres}
    for lhs,rhs in (("lifes_work","evolution"),
                    ("radiance","purpose")):
        a,b=byslug[lhs],byslug[rhs]
        if wheel_programming_partner(a["gate_gene_key_number"]) != b["gate_gene_key_number"]:
            raise ValueError("Sun/Earth 180-degree partner relationship violated")
        if a["line"]!=b["line"]:
            raise ValueError("Sun/Earth opposition requires matching lines")
        A=seen[(a["planetary_layer"],CelestialBody.SUN)].longitude
        B=seen[(b["planetary_layer"],CelestialBody.EARTH)].longitude
        diff=abs((((B-A)%360)-180))
        if diff>1e-7:
            raise ValueError("Sun and Earth not physically antipodal")
    seq={key:[
        {"sphere":slug,
         "gate_gene_key_number":byslug[slug]["gate_gene_key_number"],
         "line":byslug[slug]["line"]}
        for slug in slugs
    ] for key,slugs in CORE_SEQUENCE_ORDER.items()}
    body={
        "schema":"HUMANDESIGN_G35_HD_TO_GENEKEYS_GEOMETRIC_CROSSWALK_V1",
        "record_kind":"ASTRONOMICAL_SOURCE_CROSSWALK_NOT_OFFICIAL_PROFILE_PARITY",
        "source_system":"Gene Keys by Richard Rudd; natal/HD derived inputs",
        "source_planet_mapping":"Official Gene Keys 11 Golden Path spheres",
        "source_planet_mapping_url":"https://genekeys.com/docs/what-planets-does-each-sphere-of-the-golden-path-profile-correlate-to/",
        "official_design_day_degree_wording_inconsistent_and_unresolved":True,
        "design_time_is_incumbent_HD_88_degree_solar_arc_NOT_proved_gene_keys_official_time":True,
        "official_gene_keys_profile_website_comparison_performed":False,
        "same_64_wheel_and_longitudes_as_existing_Human_Design":True,
        "independent_astrological_evidence_count":0,
        "distinct_rudd_contemplative_interpretation_not_equivalent_to_HD_interpretation":True,
        "shadow_gift_siddhi_labels_are_contemplative_not_measured_frequencies":True,
        "gk_copyrighted_full_key_descriptions_copied":False,
        "mandala_constants_sha256":mandala_constants_sha256(),
        "core_sphere_count":len(CORE_11),
        "supplementary_sphere_count":len(SUPPLEMENTARY_3) if supplementary else 0,
        "spheres":spheres,
        "sequences":seq,
        "two_sun_earth_oppositions_not_four_independent_factors":True,
        "human_predictions_made":0,
        "human_validation_results":0,
        "production_scorer_modified":False,
        "scientific_status":"PROVISIONAL_INTERPRETATION_SOURCE_MAPPING_ONLY",
    }
    return {**body,"source_crosswalk_sha256":digest(body)}


def crosswalk_from_activations_for_synthetic_only(
    activations: Iterable[GateActivation], *,
    include_supplementary: bool=False
) -> dict:
    """Raw activations allowed for pure synthetic TEST fixtures only.

    This entrypoint cannot attest Swiss used files, source birth, or origin.
    """
    out=_normalize(activations,supplementary=include_supplementary)
    return {**out,"input_provenance":"SYNTHETIC_UNVERIFIED_ACTIVATION_TEST",
            "human_predictions_made":0}


def crosswalk_from_incumbent_verified_chart(
    chart: ChartComputation, *,
    include_supplementary: bool=False
) -> dict:
    """Accept the actual chart-engine type, no invented planet positions."""
    if type(chart) is not ChartComputation:
        raise ValueError("must be incumbent ChartComputation")
    meta=chart.metadata
    if meta.ephemeris.provider!="swiss_ephemeris_local_files":
        raise ValueError("incumbent verified Swiss files required")
    if not all(x.sha256 and x.size_bytes>0 for x in meta.ephemeris.files):
        raise ValueError("missing verified ephemeris source hashes")
    if "SEFLG_SWIEPH" not in meta.ephemeris.calculation_flags:
        raise ValueError("Swiss returned flags not evidenced")
    if meta.mandala_constants_sha256!=mandala_constants_sha256():
        raise ValueError("unrecognized mandated wheel")
    if meta.design_target_arc_degrees!=88.0:
        raise ValueError("HD design solar-arc convention must be 88 degrees")
    out=_normalize(chart.activations,supplementary=include_supplementary)
    return {**out,
      "input_provenance":"INCUMBENT_HD_CHART_ENGINE_GATES_SHARED",
      "incumbent_chart_engine_version":meta.chart_engine_version,
      "incumbent_chart_feature_sha256":chart.chart_features_sha256,
      "incumbent_swiss_ephemeris_hashes":sorted(
          {x.sha256 for x in meta.ephemeris.files}),
      "incumbent_design_time_and_birth_UTC_NOT_EXPORTED":True,
      "official_profile_parity_certified":False,
      "human_predictions_made":0,
    }
