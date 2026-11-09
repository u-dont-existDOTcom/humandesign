import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("import_mastro", ROOT / "import_mastro.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ImportTest(unittest.TestCase):
    def test_utf8_bom_groups_and_scores(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "Trees.csv"
            path.write_text('\ufeff\nfixtureA|2000/01/01 12:00:00,calm,1.2,(sun)\nfixtureB|2001/01/01 12:00:00,bold,2.5,(moon)\n', encoding='utf-8')
            parsed = module.parse_trees(path)
            self.assertEqual(len(parsed), 2)
            converted = module.convert(parsed, {key: f"C{i}" for i, key in enumerate(parsed)})
            self.assertEqual(converted[0], {"chart_id": "C0", "keywords": [{"word": "calm", "weight": 1.2}]})
            self.assertNotIn("fixtureA", str(converted))

    def test_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "Trees.csv"
            path.write_text('fixture,calm,nan,(sun)\n')
            with self.assertRaisesRegex(ValueError, "Nonfinite"):
                module.parse_trees(path)

    def test_missing_map_rejected(self):
        with self.assertRaisesRegex(ValueError, "cover"):
            module.convert({"A": [], "B": []}, {"A": "C1"})

    def test_duplicate_opaque_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "cover"):
            module.convert({"A": [], "B": []}, {"A": "C1", "B": "C1"})
