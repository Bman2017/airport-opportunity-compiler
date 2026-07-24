import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("airport_carbon_compile", ROOT / "compile.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class TenRecordAirportCarbonSliceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads((ROOT / "records.json").read_text(encoding="utf-8"))
        cls.compiled = MODULE.compile_slice(payload)

    def test_exactly_ten_source_records(self):
        self.assertEqual(len(self.compiled["source_records"]), 10)
        self.assertEqual(len(self.compiled["evidence"]), 10)

    def test_relationships_are_evidence_governed(self):
        for relationship in self.compiled["relationships"]:
            self.assertTrue(relationship["evidence_ids"])
            self.assertGreaterEqual(relationship["confidence"], 0)
            self.assertLessEqual(relationship["confidence"], 1)

    def test_full_loop_materializes_once(self):
        self.assertEqual(len(self.compiled["opportunity_candidates"]), 1)
        self.assertEqual(len(self.compiled["canonical_opportunities"]), 1)
        self.assertEqual(len(self.compiled["projections"]["marketplace_cards"]), 1)
        self.assertEqual(len(self.compiled["projections"]["opportunity_experiences"]), 1)
        self.assertEqual(len(self.compiled["projections"]["build_seeds"]), 1)

    def test_validation_report_passes(self):
        report = self.compiled["validation_report"]
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["errors"], [])

    def test_build_preserves_provenance(self):
        opportunity = self.compiled["canonical_opportunities"][0]
        build = self.compiled["projections"]["build_seeds"][0]
        self.assertEqual(build["source_opportunity_id"], opportunity["id"])
        self.assertEqual(set(build["inherited_evidence_ids"]), set(opportunity["evidence_ids"]))


if __name__ == "__main__":
    unittest.main()
