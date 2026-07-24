import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("build_federated_projection", ROOT / "build_federated_projection.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class FederatedProjectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "source_registry.json").read_text(encoding="utf-8"))
        cls.policy = json.loads((ROOT / "selection_policy.json").read_text(encoding="utf-8"))
        cls.projection = MODULE.build_projection(cls.registry, cls.policy)

    def test_exactly_500_slots(self):
        self.assertEqual(len(self.projection["slots"]), 500)
        self.assertEqual(len({slot["slot_id"] for slot in self.projection["slots"]}), 500)

    def test_existing_corpus_is_primary_source(self):
        self.assertEqual(
            self.projection["summary"]["source_channel_quotas"]["existing-technology-corpus"],
            300,
        )
        self.assertEqual(self.projection["summary"]["existing_corpus_share"], 0.6)

    def test_external_public_sources_are_material(self):
        self.assertEqual(self.projection["summary"]["external_public_source_share"], 0.4)
        self.assertGreaterEqual(self.projection["summary"]["source_channel_count"], 8)

    def test_governance_non_claims_are_enabled(self):
        governance = self.projection["governance"]
        self.assertTrue(governance["no_partnership_inference"])
        self.assertTrue(governance["no_license_availability_inference"])
        self.assertTrue(governance["no_buyer_commitment_inference"])
        self.assertTrue(governance["public_output_requires_evidence"])

    def test_selection_policy_requires_institution_and_domain_diversity(self):
        self.assertGreaterEqual(self.projection["institution_requirements"]["minimum_distinct_institutions"], 30)
        self.assertGreaterEqual(self.projection["domain_requirements"]["minimum_distinct_domains"], 15)
        self.assertTrue(self.projection["domain_requirements"]["required_outliers"])

    def test_every_slot_is_unfilled_and_gated(self):
        for slot in self.projection["slots"]:
            self.assertEqual(slot["selection_status"], "unfilled")
            self.assertEqual(slot["evidence_state"], "not_acquired")
            self.assertTrue(slot["required_gates"])


if __name__ == "__main__":
    unittest.main()
