import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("airport_carbon_compile", ROOT / "compile.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class TenRecordAirportCarbonPolicyGateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "records.json").read_text(encoding="utf-8"))

    def test_nine_records_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["records"].pop()
        with self.assertRaisesRegex(ValueError, "Expected exactly 10"):
            MODULE.compile_slice(payload)

    def test_eleven_records_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["records"].append(copy.deepcopy(payload["records"][0]))
        with self.assertRaisesRegex(ValueError, "Expected exactly 10"):
            MODULE.compile_slice(payload)

    def test_duplicate_source_id_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][1]["source_record_id"] = payload["records"][0]["source_record_id"]
        with self.assertRaisesRegex(ValueError, "must be unique"):
            MODULE.compile_slice(payload)

    def test_pending_review_blocks_publication(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][3]["review_state"] = "pending"
        result = MODULE.compile_slice(payload)
        self.assertFalse(result["validation_report"]["valid"])
        self.assertEqual(result["canonical_opportunities"], [])
        self.assertIn("Candidate failed publication policy", result["validation_report"]["errors"])

    def test_restricted_use_blocks_publication(self):
        payload = copy.deepcopy(self.payload)
        payload["records"][3]["permitted_use"] = "restricted"
        result = MODULE.compile_slice(payload)
        self.assertFalse(result["validation_report"]["valid"])
        self.assertEqual(result["canonical_opportunities"], [])
        self.assertIn("Candidate failed publication policy", result["validation_report"]["errors"])


if __name__ == "__main__":
    unittest.main()
