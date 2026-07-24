import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTRACT = json.loads((ROOT / "core-system-v1.json").read_text(encoding="utf-8"))


class CoreSystemV1ContractTest(unittest.TestCase):
    def test_contract_is_frozen(self):
        self.assertEqual(CONTRACT["status"], "frozen")
        self.assertEqual(CONTRACT["primaryUnitOfInvention"], "Configuration")

    def test_lifecycle_order_is_preserved(self):
        expected = [
            "Source",
            "Evidence",
            "CanonicalObject",
            "CanonicalRelationship",
            "Configuration",
            "Opportunity",
            "VentureProjection",
            "Build",
            "Deployment",
            "Outcome",
            "Learning",
        ]
        self.assertEqual(CONTRACT["lifecycle"], expected)

    def test_eight_engines_are_present(self):
        self.assertEqual(len(CONTRACT["engines"]), 8)
        self.assertEqual(
            CONTRACT["engines"],
            [
                "EvidenceAcquisitionEngine",
                "CanonicalUnderstandingEngine",
                "KnowledgeGraphEngine",
                "ConfigurationEngine",
                "OpportunityEngine",
                "VentureEngine",
                "DeploymentEngine",
                "LearningEngine",
            ],
        )

    def test_required_contracts_cover_full_loop(self):
        expected = {
            "Evidence",
            "CanonicalObject",
            "CanonicalRelationship",
            "IngredientInterface",
            "Configuration",
            "Opportunity",
            "VentureProjection",
            "Build",
            "Outcome",
        }
        self.assertEqual(set(CONTRACT["requiredContracts"]), expected)
        for name, fields in CONTRACT["requiredContracts"].items():
            self.assertTrue(fields, f"{name} has no required fields")
            self.assertEqual(len(fields), len(set(fields)), f"{name} repeats a required field")

    def test_relationship_governance_is_mandatory(self):
        relationship_fields = set(CONTRACT["requiredContracts"]["CanonicalRelationship"])
        self.assertTrue(
            {
                "sourceEntityId",
                "type",
                "targetEntityId",
                "assertionType",
                "confidence",
                "evidenceIds",
                "reviewState",
                "visibility",
            }.issubset(relationship_fields)
        )
        governance = CONTRACT["governance"]
        self.assertTrue(governance["everyRelationshipRequiresEvidence"])
        self.assertTrue(governance["everyInferredRelationshipRequiresConfidence"])

    def test_evidence_cannot_be_collapsed_into_canonical_truth(self):
        lifecycle = CONTRACT["lifecycle"]
        self.assertLess(lifecycle.index("Evidence"), lifecycle.index("CanonicalObject"))
        self.assertIn("Evidence", CONTRACT["rootObjectTypes"])
        self.assertIn("CanonicalObject", CONTRACT["requiredContracts"])

    def test_configuration_is_between_graph_and_opportunity(self):
        lifecycle = CONTRACT["lifecycle"]
        self.assertLess(lifecycle.index("CanonicalRelationship"), lifecycle.index("Configuration"))
        self.assertLess(lifecycle.index("Configuration"), lifecycle.index("Opportunity"))
        self.assertTrue(CONTRACT["governance"]["configurationIsPrimaryUnitOfInvention"])
        self.assertTrue(CONTRACT["governance"]["opportunityIsEvaluatedConfiguration"])

    def test_public_projection_rules_are_strict(self):
        governance = CONTRACT["governance"]
        self.assertFalse(governance["semanticSimilarityIsProof"])
        self.assertFalse(governance["publicProjectionMayExceedEvidence"])

    def test_configuration_recipes_v1_are_bounded(self):
        self.assertEqual(
            CONTRACT["configurationRecipesV1"],
            [
                "DirectTechnologyDeployment",
                "TechnologyPlusEnablingSoftware",
                "PatentBackedTechnologyBundle",
                "CrossCampusCombination",
                "FederalToMarketCombination",
                "CarbonSystemConfiguration",
            ],
        )

    def test_reference_targets_match_frozen_model(self):
        targets = CONTRACT["referenceAcceptanceTargets"]
        self.assertEqual(targets["governedSourceRecords"], 500)
        self.assertGreaterEqual(targets["evidenceBackedRelationshipsMinimum"], 1000)
        self.assertGreaterEqual(targets["generatedConfigurationsMinimum"], 500)
        self.assertGreaterEqual(targets["opportunityCandidatesMinimum"], 200)
        self.assertEqual(targets["relationshipProvenanceCoverage"], 1.0)
        self.assertEqual(targets["publicClaimPolicyCompliance"], 1.0)


if __name__ == "__main__":
    unittest.main()
