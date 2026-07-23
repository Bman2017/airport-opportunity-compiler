#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "real_records.json"
OUTPUT = ROOT / "compiled" / "airport-carbon-10.real.compiled.json"


def rel(i: str, source: str, kind: str, target: str, evidence: list[str], confidence: float, assertion: str = "inferred") -> dict[str, Any]:
    return {"id": i, "type": kind, "source_entity_id": source, "target_entity_id": target, "evidence_ids": evidence, "confidence": confidence, "assertion_type": assertion, "review_state": "approved_for_demo", "visibility": "public-evidence-demo"}


def compile_real(payload: dict[str, Any]) -> dict[str, Any]:
    records = payload["records"]
    if len(records) != 10:
        raise ValueError("Real slice requires exactly 10 records")
    if len({r["source_record_id"] for r in records}) != 10:
        raise ValueError("Real slice record IDs must be unique")
    evidence = [{
        "id": f"evidence-{r['source_record_id']}", "type": "Evidence", "source_record_id": r["source_record_id"],
        "source_reference": r["source_reference"], "publisher": r["publisher"], "retrieved_at": r["retrieved_at"],
        "claim_status": r["claim_status"], "permitted_use": r["permitted_use"], "review_state": r["review_state"]
    } for r in records]
    e = {x["source_record_id"]: x["id"] for x in evidence}

    entities = [
        {"id":"env-msp-airport","type":"Environment","name":"Minneapolis–Saint Paul International Airport"},
        {"id":"org-metropolitan-airports-commission","type":"Organization","name":"Metropolitan Airports Commission"},
        {"id":"system-msp-concession-organics","type":"OperationalSystem","name":"MSP concession organics and composting system"},
        {"id":"problem-msp-organics-value-gap","type":"Problem","name":"Organics are diverted, but higher-value conversion and auditable outcome pathways remain unproven"},
        {"id":"req-preserve-prevention-donation","type":"Requirement","name":"Preserve prevention and edible-food donation priority"},
        {"id":"req-improve-sorting-measurement","type":"Requirement","name":"Improve source sorting and measurement"},
        {"id":"req-validate-wet-feedstock-conversion","type":"Requirement","name":"Validate conversion on actual airport organic feedstock"},
        {"id":"req-quantify-avoided-methane","type":"Requirement","name":"Quantify avoided landfill methane without overstating carbon removal"},
        {"id":"outcome-msp-circular-organics-platform","type":"DesiredOutcome","name":"A measured, hierarchy-aligned circular organics platform for MSP"},
        {"id":"tech-oscar-ai-waste-sorting","type":"Technology","name":"Oscar AI waste sorting assistant"},
        {"id":"tech-umn-hydrothermal-carbonization","type":"Technology","name":"University of Minnesota hydrothermal carbonization process"},
        {"id":"patent-us9475698b2","type":"Patent","name":"US9475698B2 Hydrothermal carbonization of sewage wastes"},
        {"id":"cap-umn-hydrothermal-carbonization","type":"Capability","name":"UMN wet-organic-feedstock hydrothermal carbonization research capability"},
        {"id":"program-faa-airport-waste-planning","type":"Program","name":"FAA airport recycling and waste-reduction planning pathway"},
        {"id":"method-epa-food-waste-methane","type":"Methodology","name":"EPA avoided-landfilled-food-waste methane methodology"},
        {"id":"market-msp-concession-ecosystem","type":"MarketEntitySet","name":"MSP concession and food-service operator ecosystem"},
        {"id":"constraint-food-waste-pathway-integrity","type":"Constraint","name":"Food-waste pathway and carbon-claim integrity"}
    ]

    relationships = [
        rel("real-rel-001","org-metropolitan-airports-commission","operates","env-msp-airport",[e["real-001-msp-environment"]],1.0,"asserted"),
        rel("real-rel-002","env-msp-airport","contains","system-msp-concession-organics",[e["real-002-msp-compost-system"]],1.0,"asserted"),
        rel("real-rel-003","system-msp-concession-organics","has_performance_signal","demand-msp-organics-performance",[e["real-003-msp-performance-demand"]],1.0,"asserted"),
        rel("real-rel-004","tech-oscar-ai-waste-sorting","deployed_in","env-msp-airport",[e["real-003-msp-performance-demand"],e["real-004-oscar-sort-technology"]],0.98,"asserted"),
        rel("real-rel-005","tech-oscar-ai-waste-sorting","may_satisfy","req-improve-sorting-measurement",[e["real-004-oscar-sort-technology"]],0.94),
        rel("real-rel-006","patent-us9475698b2","evidences","tech-umn-hydrothermal-carbonization",[e["real-005-umn-htc-patent"]],0.97,"asserted"),
        rel("real-rel-007","cap-umn-hydrothermal-carbonization","supports","tech-umn-hydrothermal-carbonization",[e["real-006-umn-htc-research"]],0.95,"asserted"),
        rel("real-rel-008","tech-umn-hydrothermal-carbonization","may_satisfy","req-validate-wet-feedstock-conversion",[e["real-005-umn-htc-patent"],e["real-006-umn-htc-research"]],0.68),
        rel("real-rel-009","method-epa-food-waste-methane","may_satisfy","req-quantify-avoided-methane",[e["real-008-epa-methane-methodology"]],0.96,"asserted"),
        rel("real-rel-010","program-faa-airport-waste-planning","may_support","outcome-msp-circular-organics-platform",[e["real-007-faa-airport-waste-guidance"]],0.76),
        rel("real-rel-011","market-msp-concession-ecosystem","participates_in","system-msp-concession-organics",[e["real-002-msp-compost-system"],e["real-009-msp-concession-ecosystem"]],0.95,"asserted"),
        rel("real-rel-012","constraint-food-waste-pathway-integrity","constrains","outcome-msp-circular-organics-platform",[e["real-008-epa-methane-methodology"],e["real-010-epa-pathway-constraint"]],1.0,"asserted"),
        rel("real-rel-013","problem-msp-organics-value-gap","creates_requirement","req-preserve-prevention-donation",[e["real-009-msp-concession-ecosystem"],e["real-010-epa-pathway-constraint"]],0.91),
        rel("real-rel-014","problem-msp-organics-value-gap","creates_requirement","req-improve-sorting-measurement",[e["real-003-msp-performance-demand"],e["real-004-oscar-sort-technology"]],0.93),
        rel("real-rel-015","problem-msp-organics-value-gap","creates_requirement","req-validate-wet-feedstock-conversion",[e["real-002-msp-compost-system"],e["real-005-umn-htc-patent"]],0.65),
        rel("real-rel-016","problem-msp-organics-value-gap","creates_requirement","req-quantify-avoided-methane",[e["real-003-msp-performance-demand"],e["real-008-epa-methane-methodology"]],0.90)
    ]

    score_components = {"problem_evidence":0.92,"environment_specificity":0.96,"sorting_technology_fit":0.94,"conversion_technology_fit":0.68,"methodology_fit":0.96,"market_entity_access":0.78,"policy_pathway":0.76,"rights_and_site_readiness":0.42}
    score = round(sum(score_components.values())/len(score_components),3)
    candidate = {
        "id":"candidate-msp-circular-organics-platform","type":"OpportunityCandidate","title":"Build a measured circular organics platform at MSP",
        "environment_id":"env-msp-airport","problem_ids":["problem-msp-organics-value-gap"],
        "requirement_ids":["req-preserve-prevention-donation","req-improve-sorting-measurement","req-validate-wet-feedstock-conversion","req-quantify-avoided-methane"],
        "technology_ids":["tech-oscar-ai-waste-sorting","tech-umn-hydrothermal-carbonization"],
        "patent_ids":["patent-us9475698b2"],"supporting_ids":["cap-umn-hydrothermal-carbonization","program-faa-airport-waste-planning","method-epa-food-waste-methane","market-msp-concession-ecosystem"],
        "constraint_ids":["constraint-food-waste-pathway-integrity"],"score":score,"score_components":score_components,
        "evidence_ids":[x["id"] for x in evidence],"review_state":"approved_for_demo",
        "contradictions":[],"non_claims":["No MSP partnership is claimed","No UMN license availability is claimed","No carbon credit eligibility is claimed","No FAA funding award is claimed"]
    }
    publishable = score >= 0.75 and all(r["review_state"] == "approved_for_demo" and r["permitted_use"] == "public" for r in records)
    opportunity = {
        "id":"opp-msp-circular-organics-platform","type":"Opportunity","canonical_status":"published_evidence_demo" if publishable else "held",
        "title":candidate["title"],"summary":"Connect MSP's existing organics program and Oscar AI sorting with UMN wet-feedstock conversion research and EPA measurement methods to design a governed validation pathway.",
        "derived_from_candidate_id":candidate["id"],"technology_ids":candidate["technology_ids"],"patent_ids":candidate["patent_ids"],"evidence_ids":candidate["evidence_ids"],
        "missing_ingredients":["MSP sponsor and data access","actual feedstock characterization","technology licensing and freedom-to-operate review","bench and pilot conversion validation","site and utility requirements","techno-economic analysis","approved environmental and carbon claims"],
        "score":score,"visibility":"public-evidence-demo"
    }
    variants = [
        {"id":"variant-1","name":"Sorting and measurement optimization","ingredients":["tech-oscar-ai-waste-sorting","method-epa-food-waste-methane"],"readiness":"highest","market_entities":["Metropolitan Airports Commission","MSP concession operators"]},
        {"id":"variant-2","name":"Campus feedstock validation program","ingredients":["cap-umn-hydrothermal-carbonization","system-msp-concession-organics"],"readiness":"research-ready after permissions","market_entities":["University of Minnesota","Metropolitan Airports Commission"]},
        {"id":"variant-3","name":"Hydrothermal conversion pilot","ingredients":["tech-umn-hydrothermal-carbonization","patent-us9475698b2","cap-umn-hydrothermal-carbonization"],"readiness":"conditional","market_entities":["University of Minnesota technology owner","airport waste operator","engineering integrator"]},
        {"id":"variant-4","name":"Measured diversion and avoided-methane service","ingredients":["tech-oscar-ai-waste-sorting","method-epa-food-waste-methane","market-msp-concession-ecosystem"],"readiness":"high after data access","market_entities":["Metropolitan Airports Commission","concession operators","waste service contractor"]},
        {"id":"variant-5","name":"Integrated circular organics operating system","ingredients":["tech-oscar-ai-waste-sorting","tech-umn-hydrothermal-carbonization","patent-us9475698b2","method-epa-food-waste-methane","cap-umn-hydrothermal-carbonization"],"readiness":"longer-term validation","market_entities":["Metropolitan Airports Commission","University of Minnesota","concession operators","waste and engineering partners"]}
    ]
    return {"slice_id":payload["slice_id"],"fixture_label":payload["label"],"source_records":records,"evidence":evidence,"canonical_entities":entities,"relationships":relationships,"opportunity_candidates":[candidate],"canonical_opportunities":[opportunity] if publishable else [],"build_variants":variants,"validation_report":{"valid":publishable and all(r["evidence_ids"] for r in relationships),"counts":{"source_records":10,"evidence":10,"canonical_entities":len(entities),"relationships":len(relationships),"opportunities":1 if publishable else 0,"build_variants":len(variants)},"score":score}}


def main() -> None:
    compiled = compile_real(json.loads(INPUT.read_text()))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(compiled, indent=2)+"\n")
    print(json.dumps(compiled["validation_report"], indent=2))

if __name__ == "__main__":
    main()
