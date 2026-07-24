#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "manifest_spec.json"
OUTPUT_PATH = ROOT / "generated_manifest.json"


def generate(spec: dict) -> dict:
    slots = []
    index = 1
    universities = spec["institution_sets"]["universities"]
    doe_labs = spec["institution_sets"]["doe_labs"]
    federal = spec["institution_sets"]["federal"]
    domains = spec["domain_clusters"]
    outliers = spec["required_outlier_domains"]
    institution_cycle = universities + doe_labs + federal

    for family in spec["record_families"]:
        for local_index in range(1, family["count"] + 1):
            institution = institution_cycle[(index - 1) % len(institution_cycle)]
            domain = domains[(index - 1) % len(domains)]
            if index % 11 == 0:
                domain = outliers[((index // 11) - 1) % len(outliers)]
            role = family["graph_roles"][(local_index - 1) % len(family["graph_roles"])]
            slots.append({
                "slot_id": f"rc500-{index:03d}",
                "record_family": family["id"],
                "institution_target": institution,
                "domain_target": domain,
                "graph_role": role,
                "required_fields": [
                    "source_record_id", "source_class", "title", "body",
                    "canonical_subject_id", "source_reference", "publisher",
                    "retrieved_at", "permitted_use", "claim_status",
                    "review_state", "geography", "evidence_class"
                ],
                "semantic_facets_required": spec["required_semantic_facets"],
                "stress_tests": [
                    "entity_resolution",
                    "semantic_similarity",
                    "functional_compatibility",
                    "cross_institution_matching",
                    "cross_domain_transfer",
                    "opportunity_recipe_eligibility"
                ]
            })
            index += 1

    if len(slots) != spec["target_record_count"]:
        raise ValueError(f"Expected {spec['target_record_count']} slots, generated {len(slots)}")

    family_counts = {}
    institution_counts = {}
    domain_counts = {}
    for slot in slots:
        family_counts[slot["record_family"]] = family_counts.get(slot["record_family"], 0) + 1
        institution_counts[slot["institution_target"]] = institution_counts.get(slot["institution_target"], 0) + 1
        domain_counts[slot["domain_target"]] = domain_counts.get(slot["domain_target"], 0) + 1

    return {
        "manifest_id": spec["manifest_id"],
        "version": spec["version"],
        "record_count": len(slots),
        "slots": slots,
        "coverage": {
            "family_counts": family_counts,
            "institution_counts": institution_counts,
            "domain_counts": domain_counts,
            "distinct_institutions": len(institution_counts),
            "distinct_domains": len(domain_counts)
        },
        "opportunity_recipes": spec["opportunity_recipes"],
        "acceptance_thresholds": spec["acceptance_thresholds"],
        "non_claims": spec["non_claims"]
    }


def main() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    manifest = generate(spec)
    OUTPUT_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "valid": manifest["record_count"] == 500,
        "record_count": manifest["record_count"],
        "distinct_institutions": manifest["coverage"]["distinct_institutions"],
        "distinct_domains": manifest["coverage"]["distinct_domains"]
    }, indent=2))


if __name__ == "__main__":
    main()
