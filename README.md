# Airport Opportunity Compiler

Reference implementation for compiling a synthetic airport image into a machine-readable, interactive opportunity environment.

## Fastest way to run

### GitHub Codespaces

1. Open this repository on GitHub.
2. Select **Code → Codespaces → Create codespace on main**.
3. The compiler runs automatically.
4. Port `8000` is forwarded automatically and the browser preview opens.

The preview path is:

```text
/frontend/
```

No local cloning, Python installation, or Terminal authentication is required.

### GitHub Pages

The repository includes an automatic Pages deployment workflow. After Pages is enabled with **GitHub Actions** as its source, each push to `main` recompiles and redeploys the site.

Repository setting:

```text
Settings → Pages → Build and deployment → Source: GitHub Actions
```

The root URL redirects to the interactive frontend.

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
.devcontainer/   One-click Codespaces environment
.github/         GitHub Pages deployment workflow
compiler/        Python compilation engine
schemas/         Machine-readable contracts
environments/    Airport manifests and spatial maps
ontology/        Canonical airport object definitions
frontend/        Interactive hotspot demonstrator
data/            Demonstration marketplace records
docs/            Architecture and governance
examples/        Compiled outputs
assets/          Synthetic environment imagery
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
http://localhost:8000/
```

## Airport image

The frontend expects the reference image at:

```text
assets/airport-reference.png
```

When that file is present, the photorealistic airport renders beneath the normalized semantic hotspot overlay. The frontend displays a clear missing-image message until the asset is committed.

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
