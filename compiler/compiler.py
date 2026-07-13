from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_marketplace_rows(obj: dict[str, Any], profile: dict[str, Any]) -> list[dict[str, Any]]:
    base_terms = list(dict.fromkeys([
        obj["label"],
        *obj.get("opportunityFamilies", []),
        *profile.get("include", []),
    ]))
    row_defs = [
        ("Technologies and IP", ["technology", "patent", "complementaryTechnology"]),
        ("Researchers and Labs", ["researcher", "laboratory"]),
        ("Pilots and Deployment Partners", ["pilotSite", "corporateSolution", "procurementPathway"]),
        ("Funding and Open Challenges", ["fundingProgram", "openChallenge", "investor"]),
        ("Standards, Data, and Research", ["standard", "dataset", "publication"]),
    ]
    return [
        {
            "label": label,
            "entityTypes": entity_types,
            "query": {
                "must": base_terms,
                "mustNot": profile.get("exclude", []),
                "objectId": obj["id"],
                "limit": 100,
            },
        }
        for label, entity_types in row_defs
    ]


def compile_environment(
    manifest_path: Path,
    profiles_path: Path,
    catalog_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    profiles = load_json(profiles_path)
    catalog = load_json(catalog_path)

    compiled_objects: list[dict[str, Any]] = []
    for obj in manifest["objects"]:
        profile = profiles.get(obj["queryProfile"], {"include": [], "exclude": []})
        matches = [
            record
            for record in catalog
            if obj["id"] in record.get("objectIds", [])
            or set(obj.get("opportunityFamilies", []))
            & set(record.get("opportunityFamilies", []))
        ]
        compiled_objects.append(
            {
                **obj,
                "marketplaceRows": build_marketplace_rows(obj, profile),
                "demoResults": matches[:100],
            }
        )

    compiled = {
        "compiler": {"name": "Airport Opportunity Compiler", "version": "1.0.0"},
        "environment": {key: value for key, value in manifest.items() if key != "objects"},
        "objects": compiled_objects,
        "stats": {
            "objects": len(compiled_objects),
            "relationships": sum(len(obj.get("relationships", [])) for obj in compiled_objects),
            "opportunityFamilies": len(
                {family for obj in compiled_objects for family in obj.get("opportunityFamilies", [])}
            ),
            "catalogItems": len(catalog),
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(compiled, indent=2), encoding="utf-8")
    return compiled


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile an airport opportunity environment.")
    parser.add_argument("--manifest", default="environments/airports/reference-airport.json")
    parser.add_argument("--profiles", default="data/query-profiles.json")
    parser.add_argument("--catalog", default="data/sample-catalog.json")
    parser.add_argument("--out", default="examples/airport.compiled.json")
    args = parser.parse_args()

    compiled = compile_environment(
        Path(args.manifest),
        Path(args.profiles),
        Path(args.catalog),
        Path(args.out),
    )
    print(json.dumps(compiled["stats"], indent=2))


if __name__ == "__main__":
    main()
