#!/usr/bin/env python3
"""Enumerate supported combinations, build variants, markets and venture designs."""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("airport_carbon_compile", ROOT / "compile.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def analyze() -> dict:
    payload = json.loads((ROOT / "records.json").read_text(encoding="utf-8"))
    compiled = MODULE.compile_slice(payload)

    tech_ip_items = [
        "tech-modular-organic-carbon-conversion",
        "tech-distributed-carbon-mrv",
        "patent-modular-organic-conversion",
    ]
    possible_tech_ip = [
        list(combo)
        for size in range(1, len(tech_ip_items) + 1)
        for combo in itertools.combinations(tech_ip_items, size)
    ]
    supported_tech_ip = []
    for combo in possible_tech_ip:
        selected = set(combo)
        if "tech-modular-organic-carbon-conversion" not in selected:
            continue
        if (
            "patent-modular-organic-conversion" in selected
            and "tech-modular-organic-carbon-conversion" not in selected
        ):
            continue
        supported_tech_ip.append(combo)

    build_variants = []
    for include_mrv, include_validation, include_implementation, include_funding in itertools.product(
        [False, True], repeat=4
    ):
        ingredients = [
            "tech-modular-organic-carbon-conversion",
            "patent-modular-organic-conversion",
        ]
        if include_mrv:
            ingredients.append("tech-distributed-carbon-mrv")
        if include_validation:
            ingredients.append("cap-campus-organic-materials-validation")
        if include_implementation:
            ingredients.append("cap-airport-waste-implementation")
        if include_funding:
            ingredients.append("program-climate-demonstration-pilot")

        if not include_mrv:
            tier = "waste_reduction_only"
            carbon_claim_eligible = False
        elif not include_implementation:
            tier = "research_validation"
            carbon_claim_eligible = False
        else:
            tier = "deployable_carbon_system"
            carbon_claim_eligible = True

        build_variants.append(
            {
                "id": f"variant-{len(build_variants)+1:02d}",
                "tier": tier,
                "ingredients": ingredients,
                "carbon_claim_eligible": carbon_claim_eligible,
                "funding_ready": include_funding,
            }
        )

    venture_designs = [
        {
            "id": "venture-01-equipment-license",
            "design": "Equipment licensing and integration company",
            "customer": "Airport waste operator or airport facilities contractor",
            "revenue_model": "Technology license, equipment sale and integration fee",
            "why": "The conversion technology and patent can be commercialized without requiring ownership of the waste stream.",
            "required_variant_tier": "waste_reduction_only",
        },
        {
            "id": "venture-02-managed-service",
            "design": "Managed airport food-waste processing service",
            "customer": "Airport operator, concession manager or waste-services buyer",
            "revenue_model": "Recurring service fee plus avoided-hauling value share",
            "why": "The implementation capability supports recurring collection, operation and reporting.",
            "required_variant_tier": "deployable_carbon_system",
        },
        {
            "id": "venture-03-carbon-data-saas",
            "design": "Carbon MRV and chain-of-custody software",
            "customer": "Airport sustainability office, waste operator or carbon project developer",
            "revenue_model": "Subscription, sensor deployment and verification-data fees",
            "why": "The MRV technology is independently useful wherever auditable waste and carbon reporting is required.",
            "required_variant_tier": "research_validation",
        },
        {
            "id": "venture-04-project-developer",
            "design": "Airport carbon project development company",
            "customer": "Airport operator and carbon-credit or insetting buyer",
            "revenue_model": "Development fee, carbon-value share and long-term operating contract",
            "why": "The full conversion-plus-MRV configuration can organize a project around verified carbon outcomes.",
            "required_variant_tier": "deployable_carbon_system",
        },
        {
            "id": "venture-05-campus-testbed",
            "design": "Campus-airport validation studio",
            "customer": "University, airport innovation program and technology owner",
            "revenue_model": "Sponsored opportunity development, validation contracts and pilot administration",
            "why": "The campus capability can validate feedstock, operating conditions and output stability before deployment.",
            "required_variant_tier": "research_validation",
        },
        {
            "id": "venture-06-procurement-platform",
            "design": "Airport circular-carbon procurement platform",
            "customer": "Airport operator, concession network and implementation partners",
            "revenue_model": "Procurement fee, marketplace fee and program-management contract",
            "why": "The graph connects demand, technology, implementation, funding and methodology into a repeatable buying workflow.",
            "required_variant_tier": "deployable_carbon_system",
        },
    ]

    target_market_entities = [
        {
            "entity_type": "Airport operator",
            "value": "Lower hauling cost, higher diversion and auditable sustainability outcomes",
        },
        {
            "entity_type": "Concession operator or manager",
            "value": "Simpler source separation, waste reporting and compliance support",
        },
        {
            "entity_type": "Airport waste-services contractor",
            "value": "New processing service and differentiated operating contract",
        },
        {
            "entity_type": "Carbon project developer or buyer",
            "value": "Measured feedstock, custody and durable-output evidence",
        },
        {
            "entity_type": "University or campus laboratory",
            "value": "Paid validation, applied research and deployment pathway",
        },
        {
            "entity_type": "Technology owner or licensor",
            "value": "Airport pilot, license pathway and operating evidence",
        },
        {
            "entity_type": "Climate demonstration funder",
            "value": "A bounded, instrumented real-world pilot with measurable milestones",
        },
    ]

    relationship_counts = Counter(rel["type"] for rel in compiled["relationships"])
    assertion_counts = Counter(rel["assertion_type"] for rel in compiled["relationships"])
    average_confidence = round(
        sum(rel["confidence"] for rel in compiled["relationships"])
        / len(compiled["relationships"]),
        3,
    )

    return {
        "slice_id": compiled["slice_id"],
        "validation": compiled["validation_report"],
        "candidate_score": compiled["opportunity_candidates"][0]["score"],
        "graph_summary": {
            "entity_count": len(compiled["canonical_entities"]),
            "relationship_count": len(compiled["relationships"]),
            "relationship_types": dict(sorted(relationship_counts.items())),
            "assertion_counts": dict(sorted(assertion_counts.items())),
            "average_relationship_confidence": average_confidence,
        },
        "combination_summary": {
            "raw_nonempty_tech_ip_combinations": len(possible_tech_ip),
            "supported_tech_ip_combinations": len(supported_tech_ip),
            "supported_tech_ip": supported_tech_ip,
            "build_variants": len(build_variants),
            "build_variant_tiers": dict(Counter(v["tier"] for v in build_variants)),
            "carbon_claim_eligible_variants": sum(v["carbon_claim_eligible"] for v in build_variants),
            "funding_ready_variants": sum(v["funding_ready"] for v in build_variants),
        },
        "build_variants": build_variants,
        "venture_designs": venture_designs,
        "target_market_entities": target_market_entities,
        "limitations": [
            "All records are synthetic architecture-validation records.",
            "Only two technologies and one patent are present, so combination counts are intentionally bounded.",
            "No named airport, corporate, university, patent owner or buyer is verified by this fixture.",
            "Commercial viability, carbon eligibility and patent freedom-to-operate require external evidence and review.",
        ],
    }


def main() -> None:
    result = analyze()
    output_dir = ROOT / "compiled"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "airport-carbon-10.analysis.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
