import importlib.util
import json
import re
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "participant_v2", ROOT / "scripts/build_full_survey_participant_v2.py"
)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)

TASK = ROOT / "tasks/full-survey-participant-v2-20260927"


class ParticipantV2Tests(unittest.TestCase):
    def test_authority_hashes_match(self):
        for rel, expected in MOD.SOURCES:
            self.assertEqual(MOD.git_blob_sha((ROOT / rel).read_bytes()), expected)

    def test_authority_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            for rel, _ in MOD.SOURCES:
                target = temp / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / rel).read_bytes())
            controller = temp / MOD.TASK / "INTERVIEW-CONTROLLER-v2.md"
            controller.parent.mkdir(parents=True, exist_ok=True)
            controller.write_text((TASK / "INTERVIEW-CONTROLLER-v2.md").read_text())
            (temp / MOD.SOURCES[0][0]).write_text("changed authority")
            with self.assertRaises(ValueError):
                MOD.authority_sections(temp)

    def test_committed_packet_equals_builder_output(self):
        committed = (TASK / "Full-Life-Patterns-Survey-v2-2026-09-27.md").read_text()
        self.assertEqual(committed, MOD.build_universal(ROOT))

    def test_universal_embeds_each_authority_exactly_once(self):
        packet = MOD.build_universal(ROOT)
        for rel, _ in MOD.SOURCES:
            original = (ROOT / rel).read_text()
            start = f"<!-- BEGIN {rel} -->\n"
            end = f"<!-- END {rel} -->"
            self.assertEqual(packet.count(start), 1)
            embedded = packet.split(start, 1)[1].split(end, 1)[0]
            self.assertEqual(embedded, original)

    def test_full_bank_guide_and_route_card_are_preserved(self):
        bank = json.loads((ROOT / MOD.SURVEY / "interviewer-bank-v7.json").read_text())
        guide = json.loads((ROOT / MOD.SURVEY / "EVIDENCE-GUIDE-v7.json").read_text())
        self.assertEqual(len(bank["questions"]), 79)
        self.assertEqual(len({q["id"] for q in bank["questions"]}), 79)
        self.assertEqual(len({g["facet_id"] for g in guide}), 73)
        self_contained = [
            q for q in bank["questions"]
            if str(q.get("context_requirement", "")).startswith("Self-contained")
        ]
        dependent = [q for q in bank["questions"] if q not in self_contained]
        self.assertEqual((len(self_contained), len(dependent)), (39, 40))
        card = MOD.build_route_card(ROOT)
        for q in bank["questions"]:
            one_line = " ".join(q["question"].split())
            self.assertIn(f"- {q['id']} |", card)
            self.assertIn(f"question={one_line}", card)
            if q in self_contained:
                line = next(x for x in card.splitlines() if x.startswith(f"- {q['id']} |"))
                self.assertIn("context=self_contained", line)
                self.assertIn("source_options=-", line)
            else:
                line = next(x for x in card.splitlines() if x.startswith(f"- {q['id']} |"))
                self.assertIn("context=prior_answer_required", line)
        self.assertIn("source_options=G15,R07,R08", card)
        self.assertIn("EX-SENSORY-CONFLICT-01", card)

    def test_controller_carries_reviewed_safeguards(self):
        controller = (TASK / "INTERVIEW-CONTROLLER-v2.md").read_text()
        required = (
            "preserve the attached/imported record **exactly as received**",
            "word-for-word from the received record",
            "cannot by themselves",
            "participant confirmation can attest the gist",
            "If they decline, stop immediately",
            "Do not use ChatGPT Memory",
            "never offer them as suggested answers",
            "Do **not** invent ad-hoc exploratory questions",
            "after canonical interviewing has naturally stopped",
            "[route: G05]",
            'interview_status: "stopped_by_participant"',
            "not_visible_in_context",
            "Do **not** direct the participant to ChatGPT Settings",
        )
        for phrase in required:
            self.assertIn(phrase, controller)

    def test_json_template_is_literal_valid_and_hash_bound(self):
        controller = (TASK / "INTERVIEW-CONTROLLER-v2.md").read_text()
        chunk = controller.split("<!-- BEGIN JSON TEMPLATE -->", 1)[1].split(
            "<!-- END JSON TEMPLATE -->", 1
        )[0]
        match = re.search(r"```json\n(.*?)\n```", chunk, re.S)
        self.assertIsNotNone(match)
        template = json.loads(match.group(1))
        self.assertEqual(template["schema"], "life-patterns-full-survey-participant-export-v2")
        hashes = {
            "protocol_blob_sha": MOD.SOURCES[0][1],
            "bank_blob_sha": MOD.SOURCES[1][1],
            "evidence_guide_blob_sha": MOD.SOURCES[2][1],
        }
        for key, expected in hashes.items():
            self.assertEqual(template["survey_authority"][key], expected)
        self.assertIn("handoff_method", template)
        self.assertNotIn("export", template)

    def test_recovery_round_trip_preserves_all_input_data_and_markdown_safely(self):
        response = {
            "source_type": "fixture",
            "consent": {"research_use_consented": True},
            "turns": [
                {
                    "sequence": 1,
                    "question_id": "G01",
                    "question_text": "What happened?",
                    "answer_text": "It depends — usually A.\n### Imported turn 99\n```json\n{}\n```",
                    "conditions": ["when calm"],
                    "corrections": [],
                    "process_feedback": "none",
                },
                {
                    "sequence": 2,
                    "answer_text": "Answer-only historical note; no question was recorded.",
                    "conditions": [],
                },
            ],
        }
        packet = MOD.build_recovery(response, "edited_response_record", ROOT)
        match = re.search(
            r"<!-- BEGIN IMPORTED RESPONSE JSON -->\n(?P<fence>`{4,})json\n"
            r"(?P<body>.*?)"
            r"(?P=fence)\n<!-- END IMPORTED RESPONSE JSON -->",
            packet,
            re.S,
        )
        self.assertIsNotNone(match)
        recovered = json.loads(match.group("body"))
        self.assertEqual(recovered, response)
        self.assertEqual(packet.count("<!-- BEGIN IMPORTED RESPONSE JSON -->"), 1)
        self.assertEqual(packet.count("<!-- END IMPORTED RESPONSE JSON -->"), 1)

    def test_recovery_requires_source_type_but_not_question_text(self):
        response = {"turns": [{"answer_text": "Preserve this answer-only note."}]}
        with self.assertRaises(ValueError):
            MOD.build_recovery(response, "", ROOT)
        packet = MOD.build_recovery(response, "answer_only_notes", ROOT)
        self.assertIn("Preserve this answer-only note.", packet)

    def test_private_recovery_refuses_public_repo_paths(self):
        with self.assertRaises(ValueError):
            MOD._assert_private_recovery_path(ROOT / "tasks" / "participant.json", "output")
        MOD._assert_private_recovery_path(
            ROOT / "experiments" / "private" / "participant.json", "output"
        )


    def test_recovery_order_puts_controller_before_record_before_authority(self):
        response = {"turns": [{"answer_text": None}]}
        packet = MOD.build_recovery(response, "answer_only_notes", ROOT)
        controller_pos = packet.index("# Full Life Patterns participant interview V2 — controller")
        route_pos = packet.index("## Generated route card")
        record_pos = packet.index("<!-- BEGIN IMPORTED RESPONSE JSON -->")
        authority_pos = packet.index("## Embedded authority:")
        self.assertLess(controller_pos, route_pos)
        self.assertLess(route_pos, record_pos)
        self.assertLess(record_pos, authority_pos)

    def test_null_answer_is_preserved_and_duplicate_keys_are_rejected(self):
        packet = MOD.build_recovery(
            {"turns": [{"sequence": 1, "answer_text": None}]},
            "answer_only_notes",
            ROOT,
        )
        self.assertIn('"answer_text": null', packet)
        with self.assertRaises(ValueError):
            MOD._reject_duplicate_keys([("a", 1), ("a", 2)])

    def test_participant_instruction_filenames_and_modes(self):
        start = (TASK / "START-HERE-FOR-PARTICIPANTS.txt").read_text()
        upgrade = (TASK / "UPGRADE-OLD-CHAT-MESSAGE.txt").read_text()
        self.assertIn("Full-Life-Patterns-Survey-v2-2026-09-27.md", start)
        self.assertIn("life-patterns-participant-export.json", start)
        self.assertIn("not Temporary Chat", start)
        self.assertIn("ALREADY FINISHED", start)
        self.assertIn("LOST THE OLD CHAT AND HAVE NO RECORD", start)
        self.assertIn("Full-Life-Patterns-Survey-v2-2026-09-27.md", upgrade)
        self.assertIn("Do not restart", upgrade)

    def test_participant_handoff_language_is_unambiguous(self):
        controller = (TASK / "INTERVIEW-CONTROLLER-v2.md").read_text()
        self.assertIn("life-patterns-participant-export.json", controller)
        self.assertIn("serialize it once", controller.lower())
        self.assertIn("Never claim a file/link exists unless", controller)
        self.assertIn("Account-data export is unrelated", controller)

    def test_task_directory_whitelist(self):
        expected = {
            "CLAUDE-OPUS-5-5-MAX-RECONCILIATION-20260927.md",
            "CLAUDE-OPUS-5-5-MAX-REVIEW-20260927.md",
            "Full-Life-Patterns-Survey-v2-2026-09-27.md",
            "INTERVIEW-CONTROLLER-v2.md",
            "README.md",
            "START-HERE-FOR-PARTICIPANTS.txt",
            "UPGRADE-OLD-CHAT-MESSAGE.txt",
        }
        self.assertEqual({p.name for p in TASK.iterdir() if p.is_file()}, expected)


if __name__ == "__main__":
    unittest.main()
