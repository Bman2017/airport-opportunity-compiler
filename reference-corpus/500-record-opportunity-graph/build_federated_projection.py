#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "source_registry.json"
POLICY = ROOT / "selection_policy.json"
OUTPUT = ROOT / "compiled" / "federated-500-acquisition-plan.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_projection(registry: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    channels = registry["source_channels"]
    quota_total = sum(channel["reference_quota"] for channel in channels)
    expected = policy["source_universe"]["reference_projection_size"]
    if quota_total != expected:
        raise ValueError(f"Source quotas total {quota_total}, expected {expected}")

    role_targets = policy["required_record_roles"]
    if sum(role_targets.values()) != expected:
        raise ValueError("Required record-role quotas must total 500")

    slots: list[dict[str, Any]] = []
    sequence = 1
    for channel in channels:
        roles = channel["graph_roles"]
        for channel_index in range(1, channel["reference_quota"] + 1):
            role = roles[(channel_index - 1) % len(roles)]
            slots.append({
                "slot_id": f"rc500-{sequence:03d}",
                "source_channel_id": channel["id"],
                "source_channel_name": channel["name"],
                "adapter_type": channel["adapter_type"],
                "priority": channel["priority"],
                "provisional_graph_role": role,
                "selection_status": "unfilled",
                "source_record_id": None,
                "canonical_subject_id": None,
                "institution": None,
                "domains": [],
                "stress_tests": [],
                "evidence_state": "not_acquired",
                "required_gates": policy["selection_gates"],
            })
            sequence += 1

    if len(slots) != 500:
        raise ValueError(f"Generated {len(slots)} slots, expected 500")
    if len({slot['slot_id'] for slot in slots}) != 500:
        raise ValueError("Slot IDs are not unique")

    channel_counts = Counter(slot["source_channel_id"] for slot in slots)
    provisional_role_counts = Counter(slot["provisional_graph_role"] for slot in slots)

    return {
        "projection_id": "federated-reference-500-v1",
        "source_universe": policy["source_universe"],
        "selection_objective": policy["selection_objective"],
        "governance": registry["governance"],
        "institution_requirements": policy["institution_requirements"],
        "domain_requirements": policy["domain_requirements"],
        "stress_test_quotas": policy["stress_test_quotas"],
        "target_role_quotas": role_targets,
        "summary": {
            "slot_count": len(slots),
            "source_channel_count": len(channels),
            "source_channel_quotas": dict(sorted(channel_counts.items())),
            "provisional_role_distribution": dict(sorted(provisional_role_counts.items())),
            "existing_corpus_share": channel_counts["existing-technology-corpus"] / len(slots),
            "external_public_source_share": 1 - channel_counts["existing-technology-corpus"] / len(slots),
        },
        "slots": slots,
        "next_stage": {
            "name": "source acquisition and candidate assignment",
            "required_outputs": [
                "candidate records drawn from the existing 52000-record corpus",
                "authoritative public source records from registered adapters",
                "deduplication candidate groups",
                "canonical subject candidates",
                "structured semantic enrichment",
                "evidence and permitted-use state",
                "stress-test assignments",
            ],
        },
    }


def main() -> None:
    projection = build_projection(load(REGISTRY), load(POLICY))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(projection, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(projection["summary"], indent=2))


if __name__ == "__main__":
    main()
