# Airport Opportunity Compiler

Reference implementation for compiling a synthetic airport image into a machine-readable, interactive opportunity environment.

## Core contract

```text
Synthetic Image
+ Canonical Airport Specification
+ Spatial Object Manifest
+ Relationship Graph
+ Opportunity Families
+ Query Profiles
+ Marketplace Catalog
= Executable Airport Opportunity Environment
```

## Repository structure

```text
compiler/       Python compilation engine
schemas/        Machine-readable contracts
environments/   Airport manifests and spatial maps
ontology/       Canonical airport object definitions
frontend/       Interactive hotspot demonstrator
data/           Demonstration marketplace records
docs/           Architecture and governance
examples/       Compiled outputs
```

## Run locally

```bash
git clone https://github.com/Bman2017/airport-opportunity-compiler.git
cd airport-opportunity-compiler
python3 compiler/compiler.py
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000/frontend/
```

## Current status

Version 1 establishes the compiler contract and a first airport reference manifest. Demonstration marketplace records are synthetic and must be replaced by evidence-governed records before production use.

## Governing separation

The system keeps these concepts distinct:

1. Canonical Airport Object — what exists.
2. Canonical Type — the formal specification.
3. Airport Entity — an instance of that type.
4. Visual Representation — an image depicting the entity.
5. Spatial Annotation — geometry connecting image regions to entities.
6. Opportunity Query — executable retrieval logic.
7. Marketplace Result — evidence-governed records returned by the query.
