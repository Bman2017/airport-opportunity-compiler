import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("compile_real", ROOT / "compile_real.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

class RealMSPSliceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiled = MODULE.compile_real(json.loads((ROOT / "real_records.json").read_text()))

    def test_exactly_ten_public_records(self):
        self.assertEqual(len(self.compiled["source_records"]), 10)
        self.assertTrue(all(r["permitted_use"] == "public" for r in self.compiled["source_records"]))
        self.assertTrue(all(r["claim_status"] == "verified_public_source" for r in self.compiled["source_records"]))

    def test_relationships_are_evidence_governed(self):
        self.assertEqual(len(self.compiled["relationships"]), 16)
        for relationship in self.compiled["relationships"]:
            self.assertTrue(relationship["evidence_ids"])
            self.assertGreaterEqual(relationship["confidence"], 0)
            self.assertLessEqual(relationship["confidence"], 1)

    def test_opportunity_preserves_non_claims(self):
        candidate = self.compiled["opportunity_candidates"][0]
        self.assertEqual(len(candidate["non_claims"]), 4)
        self.assertIn("No UMN license availability is claimed", candidate["non_claims"])
        self.assertIn("No carbon credit eligibility is claimed", candidate["non_claims"])

    def test_five_ranked_build_variants(self):
        self.assertEqual(len(self.compiled["build_variants"]), 5)
        self.assertEqual(self.compiled["build_variants"][0]["readiness"], "highest")
        self.assertEqual(self.compiled["build_variants"][-1]["readiness"], "longer-term validation")

    def test_readiness_score_reflects_missing_rights_and_site(self):
        candidate = self.compiled["opportunity_candidates"][0]
        self.assertLess(candidate["score_components"]["rights_and_site_readiness"], 0.5)
        self.assertGreater(candidate["score"], 0.75)
        opportunity = self.compiled["canonical_opportunities"][0]
        self.assertGreaterEqual(len(opportunity["missing_ingredients"]), 7)

    def test_validation_passes(self):
        self.assertTrue(self.compiled["validation_report"]["valid"])
        self.assertEqual(self.compiled["validation_report"]["counts"]["source_records"], 10)
        self.assertEqual(self.compiled["validation_report"]["counts"]["build_variants"], 5)

if __name__ == "__main__":
    unittest.main()
