"""Source distinctions and exact turning arithmetic, not prognostic accuracy."""

import unittest

import lilly_third_house_reference as reference


class AbsentRelativeReferenceTests(unittest.TestCase):
    def test_complete_inclusive_rotation_for_each_source_origin(self):
        expected = {
            "brother": (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2),
            "father": (4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3),
            "child": (5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4),
            "servant": (6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5),
        }
        for relationship, houses in expected.items():
            with self.subTest(relationship=relationship):
                result = reference.absent_relative_house_reference(relationship)
                self.assertEqual(result["turned_houses"], dict(enumerate(houses, 1)))
                self.assertEqual(result["relative_ascendant_house"], houses[0])
                self.assertEqual(result["querent_house"], 1)

    def test_source_examples_and_editorial_sibling_alias_are_distinguished(self):
        brother = reference.absent_relative_house_reference("brother")
        sibling = reference.absent_relative_house_reference("sibling")
        self.assertEqual(sibling["turned_houses"], brother["turned_houses"])
        self.assertEqual(sibling["source_relationship"], "brother")
        self.assertIs(sibling["editorial_alias"], True)
        self.assertIs(brother["editorial_alias"], False)
        for name in ("child", "son", "daughter"):
            with self.subTest(name=name):
                result = reference.absent_relative_house_reference(name)
                self.assertEqual(result["relative_ascendant_house"], 5)
                self.assertEqual(result["relation_source"], {"pdf_page": 226, "printed_page": 192})
                self.assertEqual(result["source_relationship"], name)
                self.assertIs(result["editorial_alias"], False)

    def test_original_figure_exception_does_not_overwrite_turned_houses(self):
        for name in ("brother", "father", "child", "servant"):
            with self.subTest(name=name):
                result = reference.absent_relative_house_reference(name)
                figure = result["original_figure_references"]
                self.assertEqual(figure["houses"], {6: "infirmity", 8: "death", 12: "imprisonment"})
                self.assertEqual(figure["source"], {"pdf_page": 226, "printed_page": 192})
                for relative in (6, 8, 12):
                    self.assertNotEqual(result["turned_houses"][relative], relative)
                self.assertIsNone(result["frame_precedence"])
                self.assertTrue(result["frame_coexistence_note"])
                self.assertEqual(result["query_context"], "absent_relative")
                self.assertIs(result["interpretive_judgement_computed"], False)
                self.assertIs(result["is_forecast"], False)

    def test_unrelated_or_unspecified_person_never_defaults_to_seventh(self):
        for name in ("unrelated", "stranger", "spouse", "mother", "general_absent", "", "Brother"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                reference.absent_relative_house_reference(name)
        for value in (None, True, 3, ["brother"]):
            with self.subTest(value=value), self.assertRaises(TypeError):
                reference.absent_relative_house_reference(value)
        with self.assertRaises(TypeError):
            reference.absent_relative_house_reference()

    def test_mutating_one_return_cannot_corrupt_either_frame(self):
        result = reference.absent_relative_house_reference("brother")
        result["turned_houses"][12] = 7
        result["original_figure_references"]["houses"][6] = "other"
        result["turning_source"]["pdf_pages"].clear()
        fresh = reference.absent_relative_house_reference("brother")
        self.assertEqual(fresh["turned_houses"][12], 2)
        self.assertEqual(fresh["original_figure_references"]["houses"][6], "infirmity")
        self.assertEqual(fresh["turning_source"]["pdf_pages"], [223, 225, 226])


class QuestionTimeReferenceTests(unittest.TestCase):
    def test_hearing_proposal_and_advice_beginning_are_distinct_anchors(self):
        contexts = {
            "news_heard_by_self": ("first_hearing", 227, 193),
            "news_proposed_by_another": ("question_proposal", 227, 193),
            "advice_visit": ("advice_communication_begins", 228, 194),
        }
        anchors = set()
        for context, (anchor, page, printed) in contexts.items():
            with self.subTest(context=context):
                result = reference.question_time_reference(context)
                self.assertEqual(result["anchor"], anchor)
                self.assertEqual(result["source"], {"pdf_page": page, "printed_page": printed})
                self.assertIs(result["actual_timestamp_chosen"], False)
                self.assertIs(result["chart_time_computed"], False)
                self.assertIsNone(result["modern_interface_mapping"])
                self.assertIs(result["is_forecast"], False)
                anchors.add(result["anchor"])
        self.assertEqual(len(anchors), 3)

    def test_context_is_required_and_modern_interfaces_are_not_inferred(self):
        for context in ("auto", "news", "message_received", "ai_request", "visit_arrival", ""):
            with self.subTest(context=context), self.assertRaises(ValueError):
                reference.question_time_reference(context)
        for value in (None, False, 227, ["advice_visit"]):
            with self.subTest(value=value), self.assertRaises(TypeError):
                reference.question_time_reference(value)
        with self.assertRaises(TypeError):
            reference.question_time_reference()


if __name__ == "__main__":
    unittest.main()
