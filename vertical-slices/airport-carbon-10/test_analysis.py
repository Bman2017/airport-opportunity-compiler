import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("airport_carbon_analysis", ROOT / "analyze.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class TenRecordAirportCarbonAnalysisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.analysis = MODULE.analyze()

    def test_graph_summary(self):
        graph = self.analysis["graph_summary"]
        self.assertEqual(graph["entity_count"], 16)
        self.assertEqual(graph["relationship_count"], 14)
        self.assertEqual(graph["assertion_counts"], {"asserted": 6, "inferred": 8})
        self.assertAlmostEqual(graph["average_relationship_confidence"], 0.928)

    def test_combination_counts(self):
        summary = self.analysis["combination_summary"]
        self.assertEqual(summary["raw_nonempty_tech_ip_combinations"], 7)
        self.assertEqual(summary["supported_tech_ip_combinations"], 4)
        self.assertEqual(summary["build_variants"], 16)
        self.assertEqual(
            summary["build_variant_tiers"],
            {
                "deployable_carbon_system": 4,
                "research_validation": 4,
                "waste_reduction_only": 8,
            },
        )
        self.assertEqual(summary["carbon_claim_eligible_variants"], 4)
        self.assertEqual(summary["funding_ready_variants"], 8)

    def test_venture_and_market_outputs(self):
        self.assertEqual(len(self.analysis["venture_designs"]), 6)
        self.assertEqual(len(self.analysis["target_market_entities"]), 7)

    def test_analysis_retains_synthetic_limits(self):
        self.assertTrue(self.analysis["limitations"])
        self.assertTrue(any("synthetic" in item.lower() for item in self.analysis["limitations"]))


if __name__ == "__main__":
    unittest.main()
