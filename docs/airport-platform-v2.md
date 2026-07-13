# Airport Opportunity Platform v2

## Purpose

Turn a synthetic airport image into a governed, executable commercialization environment rather than a static annotated picture.

## System boundary

```text
Airport Specification
  -> Airport Compiler
  -> Compiled Environment Package
  -> Spatial Viewer
  -> Opportunity Query Engine
  -> Evidence-Governed Marketplace
  -> Opportunity Workspace
```

## Permanent separations

1. **Canonical Object** describes what exists.
2. **Canonical Type** formally specifies the object.
3. **Airport Entity** instantiates the type for a real or synthetic airport.
4. **Visual Representation** depicts one or more entities.
5. **Spatial Annotation** maps image coordinates to entities.
6. **Opportunity Query** defines retrieval and ranking behavior.
7. **Marketplace Result** is a governed record returned by a query.
8. **Workspace** stores user intent, selections, comparisons, and opportunity development activity.

## Compiled environment package

Every compiled airport must produce:

- environment metadata;
- image and rendition metadata;
- stable object identities;
- normalized hotspot geometry;
- object hierarchy;
- permitted relationships;
- opportunity-family mappings;
- query profiles;
- role and objective ranking inputs;
- recursive expansion rules;
- UI presentation metadata;
- validation report;
- compiler version and provenance.

## Viewer contract

The viewer must provide:

- responsive image canvas;
- pan and zoom;
- point, polygon, and region hotspots;
- keyboard-accessible selection;
- hover labels;
- selected-object drawer;
- relationship display;
- generated marketplace rails;
- mobile-compatible interaction;
- stable deep links to selected entities;
- no ownership of canonical object definitions or marketplace records.

## Evidence governance

Every production marketplace result must include:

- source identity;
- source URL or internal source reference;
- retrieved date;
- claim type;
- claim status;
- evidence status;
- permitted-use status;
- entity identity;
- confidence;
- freshness;
- contradictions or unresolved conflicts;
- human review state where required.

Synthetic demonstrations must remain visibly labeled and may never be presented as verified opportunities.

## Recursive exploration

The viewer may navigate:

```text
Airport
  -> System
  -> Subsystem
  -> Component
  -> Capability
  -> Opportunity Family
  -> Technology / IP / Research / Pilot / Funding
```

Each transition must preserve the selected object identity, user role, objective, and originating deployment context.

## Reference implementation status

Airport Viewer v2 establishes the interaction shell: pan, zoom, point hotspots, object drawer, relationships, and marketplace rails. It does not yet constitute the complete canonical airport library or a production evidence index.

## Next governed build sequence

1. Complete canonical airport object discovery and definitions.
2. Define relationship vocabulary and validation constraints.
3. Replace reference geometry with reviewed image-specific annotations.
4. Add production-resolution WebP/AVIF renditions.
5. Introduce claim and evidence schemas.
6. Connect real marketplace indexes.
7. Add role-aware and objective-aware ranking.
8. Add recursive subsystem scenes.
9. Add opportunity workspace persistence.
10. Validate a second airport without changing canonical definitions or viewer code.
