#!/usr/bin/env python3
"""Compile the ten-record airport carbon fixture into governed projections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "records.json"
OUTPUT_DIR = ROOT / "compiled"
OUTPUT = OUTPUT_DIR / "airport-carbon-10.compiled.json"


def evidence(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"evidence-{record['source_record_id']}",
        "type": "Evidence",
        "source_record_id": record["source_record_id"],
        "source_class": record["source_class"],
        "source_reference": record["source_reference"],
        "retrieved_at": record["retrieved_at"],
        "permitted_use": record["permitted_use"],
        "claim_status": record["claim_status"],
        "review_state": record["review_state"],
        "content_hash_basis": f"{record['title']}|{record['body']}",
    }


def relationship(
    rel_id: str,
    source: str,
    rel_type: str,
    target: str,
    evidence_ids: list[str],
    confidence: float,
    assertion_type: str = "inferred",
) -> dict[str, Any]:
    return {
        "id": rel_id,
        "type": rel_type,
        "source_entity_id": source,
        "target_entity_id": target,
        "assertion_type": assertion_type,
        "confidence": confidence,
        "evidence_ids": evidence_ids,
        "review_state": "approved_for_demo",
        "visibility": "internal-demo",
    }


def compile_slice(payload: dict[str, Any]) -> dict[str, Any]:
    records = payload["records"]
    if len(records) != 10:
        raise ValueError(f"Expected exactly 10 source records, found {len(records)}")

    ids = [r["source_record_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Source record IDs must be unique")

    ev = [evidence(r) for r in records]
    ev_by_source = {e["source_record_id"]: e["id"] for e in ev}

    entities = [
        {"id": "env-airport-alpha", "type": "Environment", "name": "Airport Alpha", "status": "synthetic"},
        {"id": "system-airport-concessions", "type": "OperationalSystem", "name": "Airport concession and organic-waste system"},
        {"id": "problem-airport-organic-waste", "type": "Problem", "name": "Unmeasured mixed concession food waste"},
        {"id": "req-reduce-hauling", "type": "Requirement", "name": "Reduce waste hauling and disposal"},
        {"id": "req-auditable-carbon", "type": "Requirement", "name": "Produce auditable carbon outcomes"},
        {"id": "outcome-airport-carbon-value", "type": "DesiredOutcome", "name": "Convert airport food waste into measurable carbon value"},
        {"id": "tech-modular-organic-carbon-conversion", "type": "Technology", "name": "Modular organic-waste carbon conversion system"},
        {"id": "tech-distributed-carbon-mrv", "type": "Technology", "name": "Distributed carbon measurement and chain-of-custody system"},
        {"id": "patent-modular-organic-conversion", "type": "Patent", "name": "Modular organic conversion patent evidence"},
        {"id": "org-campus-alpha", "type": "Organization", "name": "Campus Alpha", "status": "synthetic"},
        {"id": "cap-campus-organic-materials-validation", "type": "Capability", "name": "Organic-materials validation"},
        {"id": "demand-measurable-airport-waste-carbon", "type": "DemandSignal", "name": "Demand for measurable airport waste and carbon outcomes"},
        {"id": "program-climate-demonstration-pilot", "type": "Program", "name": "Climate demonstration pilot program"},
        {"id": "org-implementation-alpha", "type": "Organization", "name": "Implementation Company Alpha", "status": "synthetic"},
        {"id": "cap-airport-waste-implementation", "type": "Capability", "name": "Airport waste operations implementation"},
        {"id": "constraint-carbon-claim-integrity", "type": "Constraint", "name": "Carbon claim integrity requirements"},
    ]

    relationships = [
        relationship("rel-001", "env-airport-alpha", "contains", "system-airport-concessions", [ev_by_source["src-001-airport-environment"]], 1.0, "asserted"),
        relationship("rel-002", "system-airport-concessions", "experiences", "problem-airport-organic-waste", [ev_by_source["src-002-organic-waste-problem"]], 0.98, "asserted"),
        relationship("rel-003", "problem-airport-organic-waste", "creates_requirement", "req-reduce-hauling", [ev_by_source["src-002-organic-waste-problem"]], 0.92),
        relationship("rel-004", "problem-airport-organic-waste", "creates_requirement", "req-auditable-carbon", [ev_by_source["src-002-organic-waste-problem"], ev_by_source["src-010-methodology-constraint"]], 0.95),
        relationship("rel-005", "tech-modular-organic-carbon-conversion", "may_satisfy", "req-reduce-hauling", [ev_by_source["src-003-conversion-technology"], ev_by_source["src-005-patent-evidence"]], 0.88),
        relationship("rel-006", "tech-distributed-carbon-mrv", "may_satisfy", "req-auditable-carbon", [ev_by_source["src-004-mrv-technology"], ev_by_source["src-010-methodology-constraint"]], 0.91),
        relationship("rel-007", "patent-modular-organic-conversion", "evidences", "tech-modular-organic-carbon-conversion", [ev_by_source["src-005-patent-evidence"]], 1.0, "asserted"),
        relationship("rel-008", "org-campus-alpha", "possesses", "cap-campus-organic-materials-validation", [ev_by_source["src-006-campus-capability"]], 1.0, "asserted"),
        relationship("rel-009", "cap-campus-organic-materials-validation", "can_validate", "tech-modular-organic-carbon-conversion", [ev_by_source["src-006-campus-capability"], ev_by_source["src-003-conversion-technology"]], 0.82),
        relationship("rel-010", "demand-measurable-airport-waste-carbon", "validates", "outcome-airport-carbon-value", [ev_by_source["src-007-demand-signal"]], 0.89),
        relationship("rel-011", "program-climate-demonstration-pilot", "may_support", "outcome-airport-carbon-value", [ev_by_source["src-008-funding-program"]], 0.80),
        relationship("rel-012", "org-implementation-alpha", "possesses", "cap-airport-waste-implementation", [ev_by_source["src-009-implementation-capability"]], 1.0, "asserted"),
        relationship("rel-013", "cap-airport-waste-implementation", "can_deploy_in", "env-airport-alpha", [ev_by_source["src-009-implementation-capability"], ev_by_source["src-001-airport-environment"]], 0.84),
        relationship("rel-014", "constraint-carbon-claim-integrity", "constrains", "outcome-airport-carbon-value", [ev_by_source["src-010-methodology-constraint"]], 1.0, "asserted"),
    ]

    score_components = {
        "problem_evidence": 0.95,
        "airport_specificity": 0.90,
        "technology_fit": 0.89,
        "carbon_integrity": 0.91,
        "pilotability": 0.84,
        "market_pull": 0.89,
        "campus_adjacency": 0.82,
        "pathway_completeness": 0.83,
    }
    candidate_score = round(sum(score_components.values()) / len(score_components), 3)

    candidate = {
        "id": "candidate-airport-food-waste-carbon-value",
        "type": "OpportunityCandidate",
        "title": "Turn airport food waste into a verifiable carbon asset",
        "environment_id": "env-airport-alpha",
        "problem_ids": ["problem-airport-organic-waste"],
        "requirement_ids": ["req-reduce-hauling", "req-auditable-carbon"],
        "technology_ids": ["tech-modular-organic-carbon-conversion", "tech-distributed-carbon-mrv"],
        "supporting_ids": ["cap-campus-organic-materials-validation", "demand-measurable-airport-waste-carbon", "program-climate-demonstration-pilot", "cap-airport-waste-implementation"],
        "constraint_ids": ["constraint-carbon-claim-integrity"],
        "score": candidate_score,
        "score_components": score_components,
        "evidence_ids": [e["id"] for e in ev],
        "review_state": "approved_for_demo",
        "contradictions": [],
    }

    publishable = (
        candidate_score >= 0.75
        and len(candidate["requirement_ids"]) >= 2
        and len(candidate["technology_ids"]) >= 2
        and not candidate["contradictions"]
        and all(r["review_state"] == "approved_for_demo" for r in records)
        and all(r["permitted_use"] in {"public", "internal-demo"} for r in records)
    )

    opportunity = {
        "id": "opp-airport-food-waste-carbon-value",
        "type": "Opportunity",
        "canonical_status": "published_demo" if publishable else "held",
        "title": candidate["title"],
        "summary": "Combine modular organic-waste conversion, carbon MRV, campus validation and airport operations into a pilotable carbon-value system.",
        "derived_from_candidate_id": candidate["id"],
        "environment_ids": [candidate["environment_id"]],
        "problem_ids": candidate["problem_ids"],
        "requirement_ids": candidate["requirement_ids"],
        "technology_ids": candidate["technology_ids"],
        "evidence_ids": candidate["evidence_ids"],
        "missing_ingredients": ["verified daily waste volume", "site footprint", "airport operating sponsor", "accepted carbon methodology"],
        "score": candidate_score,
        "visibility": "internal-demo",
    }

    marketplace_view = {
        "view_type": "MarketplaceOpportunityCardView",
        "id": opportunity["id"],
        "eyebrow": "Airport Carbon",
        "title": opportunity["title"],
        "summary": opportunity["summary"],
        "location_label": "Airport Alpha",
        "technology_count": len(opportunity["technology_ids"]),
        "evidence_count": len(opportunity["evidence_ids"]),
        "buildability_score": round(candidate_score * 100),
        "primary_action": "Explore the opportunity",
        "demo_label": "Synthetic architecture-validation fixture",
    }

    experience_view = {
        "view_type": "OpportunityExperienceView",
        "opportunity_id": opportunity["id"],
        "sections": {
            "what_could_be_built": ["distributed airport food-waste carbon pilot", "carbon-accounted waste service", "campus-airport validation program"],
            "why_this_environment": ["concentrated food-service operations", "repeatable collection points", "controlled pilot geography"],
            "matched_ingredients": candidate["technology_ids"] + candidate["supporting_ids"],
            "requirements": candidate["requirement_ids"],
            "evidence": candidate["evidence_ids"],
            "missing_ingredients": opportunity["missing_ingredients"],
        },
        "next_action": "Obtain verified daily food-waste volume, composition, hauling cost and operating constraints.",
    }

    build_seed = {
        "view_type": "BuildSeedView",
        "id": "build-airport-food-waste-carbon-pilot",
        "title": "Airport Food Waste Carbon Pilot",
        "source_opportunity_id": opportunity["id"],
        "inherited_entity_ids": [candidate["environment_id"]] + candidate["problem_ids"] + candidate["requirement_ids"] + candidate["technology_ids"] + candidate["supporting_ids"] + candidate["constraint_ids"],
        "inherited_evidence_ids": candidate["evidence_ids"],
        "first_consequential_action": experience_view["next_action"],
        "status": "draft",
    }

    validation_errors: list[str] = []
    if not publishable:
        validation_errors.append("Candidate failed publication policy")
    if len(ev) != 10:
        validation_errors.append("Evidence count is not 10")
    if any(not rel["evidence_ids"] for rel in relationships):
        validation_errors.append("A relationship is missing evidence")
    if any(not 0 <= rel["confidence"] <= 1 for rel in relationships):
        validation_errors.append("Relationship confidence outside 0..1")

    return {
        "slice_id": payload["slice_id"],
        "fixture_label": payload["label"],
        "source_records": records,
        "evidence": ev,
        "canonical_entities": entities,
        "relationships": relationships,
        "opportunity_candidates": [candidate],
        "canonical_opportunities": [opportunity] if publishable else [],
        "projections": {
            "marketplace_cards": [marketplace_view] if publishable else [],
            "opportunity_experiences": [experience_view] if publishable else [],
            "build_seeds": [build_seed] if publishable else [],
        },
        "validation_report": {
            "valid": not validation_errors,
            "errors": validation_errors,
            "counts": {
                "source_records": len(records),
                "evidence": len(ev),
                "canonical_entities": len(entities),
                "relationships": len(relationships),
                "opportunity_candidates": 1,
                "canonical_opportunities": 1 if publishable else 0,
                "marketplace_cards": 1 if publishable else 0,
                "opportunity_experiences": 1 if publishable else 0,
                "build_seeds": 1 if publishable else 0,
            },
        },
    }


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    compiled = compile_slice(payload)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(compiled, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(compiled["validation_report"], indent=2))


if __name__ == "__main__":
    main()
