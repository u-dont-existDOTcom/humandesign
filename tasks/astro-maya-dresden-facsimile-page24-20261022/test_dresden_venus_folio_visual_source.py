#!/usr/bin/env python3
"""Original Förstemann 1892 source-visual evidence checks, NOT glyph decipherment."""
from pathlib import Path
from hashlib import sha256
import json,struct,subprocess,unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[1]
HOME=Path("/home/joel/Téléchargements")
DOC=B/"DRESDEN_VENUS_P24_P46_VISUAL_SOURCE_WITNESS_V1.json"
PRIOR=ROOT/"tasks/astro-maya-dresden-original-folio-20261022/DRESDEN_FOLIO_SOURCE_WINDOWS_V1.json"

def sha(b:bytes)->str:return sha256(b).hexdigest()
def load(p:Path)->dict:return json.loads(p.read_text(encoding="utf-8"))
def locate_image(name:str)->Path:
    extracted=B/"evidence"/name
    return extracted if extracted.is_file() else HOME/name
def dimensions(raw:bytes)->tuple[int,int]:
    if raw[:8]!=b"\x89PNG\r\n\x1a\n":raise ValueError("Not a PNG")
    return struct.unpack(">II",raw[16:24])

class FirstFolioVisualWitness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=load(DOC)
        cls.source=cls.doc["source_witnesses"]
        cls.previous=load(PRIOR)

    def test_previous_discovery_preserved_and_not_retroactively_changed(self):
        self.assertFalse(self.previous["candidate_folio_windows"][0]["original_image_canvas_seen"])
        self.assertFalse(self.previous["primary_manuscript"]["authenticated_original_glyph_folio_extracted"])
        self.assertEqual(len(self.previous["candidate_folio_windows"]),3)

    def test_current_two_original_folio_witnesses_and_distinct_pdf_page_range(self):
        a,b=self.source
        self.assertEqual(len(self.source),2)
        self.assertNotEqual(a["pdf_source_url"],b["pdf_source_url"])
        self.assertEqual((a["pdf_pages"],a["pdf_page_index_1_based"]),(12,12))
        self.assertEqual((b["pdf_pages"],b["pdf_page_index_1_based"]),(14,1))
        self.assertIn("p.24",a["historical_edition_page"])
        self.assertIn("p.46",b["historical_edition_page"])

    def test_exact_downloaded_pdfs_source_sha_and_size(self):
        for a in self.source:
            with self.subTest(folio=a["id"]):
                path=HOME/a["original_facsimile_pdf"]
                self.assertTrue(path.is_file(),str(path))
                raw=path.read_bytes()
                self.assertEqual((len(raw),sha(raw)),(a["pdf_byte_count"],a["pdf_sha256"]))
                result=subprocess.run(["pdfinfo",str(path)],check=True,capture_output=True,text=True)
                pages=int(next(s.split(":",1)[1].strip() for s in result.stdout.splitlines() if s.startswith("Pages:")))
                self.assertEqual(pages,a["pdf_pages"])

    def test_png_original_render_sha_dimensions(self):
        for a in self.source:
            with self.subTest(folio=a["id"]):
                f=locate_image(a["page_png"])
                self.assertTrue(f.is_file(),str(f))
                raw=f.read_bytes()
                self.assertEqual(sha(raw),a["render_sha256"])
                self.assertEqual(dimensions(raw),(a["rendered_width"],a["rendered_height"]))

    def test_original_1880s_facsimile_not_new_original_manuscript_photograph(self):
        for row in self.source:
            self.assertIn("1892 Förstemann",row["photographic_source_kind"])
            self.assertIn("NOT authenticated present SLUB original photograph",row["photographic_source_kind"])
        self.assertFalse(self.doc["verified_original_held_codex_high_resolution_photographs"])
        self.assertTrue(self.doc["Förstemann_1892_FAMSI_pdf_original_facsimile_source_verified"])

    def test_source_image_observed_but_no_glyphic_transcription_claim(self):
        self.assertEqual(self.doc["independently_transcribed_Maya_hieroglyph_signs"],0)
        self.assertTrue(all(a["source_readiness"]=="FACSIMILE_IMAGE_VISUALLY_INSPECTED_GLYPHS_NOT_DECIPHERED" for a in self.source))
        self.assertFalse(self.doc["scholarly_derived_mathematical_claims"]["independent_original_Venus_glyph_number_decipherment_completed"])

    def test_four_different_scholarly_and_original_source_link_classes(self):
        refs=self.doc["interpretive_bibliography"]
        self.assertEqual(len(refs),4)
        self.assertTrue(any("slub-dresden.de" in x["url"] for x in refs))
        self.assertTrue(any("famsi.org" in x["url"] for x in refs))
        self.assertTrue(any("scielo.org.mx" in x["url"] for x in refs))
        self.assertTrue(any("escholarship.org" in x["url"] for x in refs))

    def test_venus_table_derived_arithmetic_and_non_tropical_year(self):
        x=self.doc["scholarly_derived_mathematical_claims"]
        self.assertEqual(x["derived_table_row_days"],5*584)
        self.assertEqual(x["derived_full_table_days"],13*2920)
        self.assertEqual(x["derived_full_table_days"],104*365)
        self.assertEqual(x["derived_full_table_days"],146*260)
        self.assertEqual(x["derived_full_table_days"],65*584)
        self.assertTrue(x["counts_as_104_Haab_years_not_104_tropical_Gregorian_years"])
        self.assertNotEqual(x["derived_full_table_days"],104*365.2422)

    def test_academic_four_phase_candidate_not_independently_deciphered(self):
        x=self.doc["scholarly_derived_mathematical_claims"]
        self.assertEqual(x["Venus_phase_interval_candidate_from_scholarly_reading_days"],[236,90,250,8])
        self.assertEqual(sum(x["Venus_phase_interval_candidate_from_scholarly_reading_days"]),584)
        self.assertIn("NOT independent new glyph-decipherment",x["source_of_phase_intervals"])

    def test_calendar_correlation_not_pinned_for_personal_birth_sign(self):
        x=self.doc["scholarly_derived_mathematical_claims"]
        self.assertFalse(x["Maya_GMT_Long_Count_correlation_pinned_or_verified"])
        self.assertFalse(x["birth_day_traits_original_to_question_mapping_completed"])
        self.assertEqual(x["Maya_natal_oracular_rules_promoted"],0)

    def test_no_personality_death_medical_or_human_prediction_promotions(self):
        self.assertEqual(self.doc["independently_authenticated_Maya_natal_personality_claims"],0)
        self.assertEqual(self.doc["independent_real_human_blind_predictions"],0)
        self.assertEqual(self.doc["runtime_astrology_rules_promoted"],0)
        self.assertIn("0",str(self.doc["runtime_astrology_rules_promoted"]))

if __name__=="__main__":
    unittest.main()
