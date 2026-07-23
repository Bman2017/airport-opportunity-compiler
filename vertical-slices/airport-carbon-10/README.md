# Ten-Record Airport Carbon Vertical Slice

## Purpose

Prove the complete SpinOut U loop with exactly ten heterogeneous source records before scaling corpus ingestion.

```text
10 source records
  -> immutable evidence records
  -> normalized records
  -> canonical entities
  -> governed relationships
  -> semantic intersection
  -> scored opportunity candidate
  -> policy-approved canonical opportunity
  -> marketplace projection
  -> opportunity experience projection
  -> build seed
```

This fixture is deliberately small, deterministic, and visibly synthetic. It validates architecture and contracts; it does not represent an airport partnership or a verified commercial opportunity.

## Fixed demonstration context

- Deployment environment: `env-airport-alpha`
- Domain: airport food waste and carbon accounting
- Source-record limit: exactly 10
- Expected publishable opportunities: exactly 1
- Expected marketplace cards: exactly 1
- Expected build seeds: exactly 1

## Ten records

1. Airport operating environment
2. Airport organic-waste problem
3. Organic-waste conversion technology
4. Carbon-measurement technology
5. Patent evidence for the conversion technology
6. Campus validation capability
7. Corporate demand signal
8. Deployment funding program
9. Implementation company capability
10. Carbon-methodology constraint

## Canonical objects created

The ten records may support more than ten objects because source evidence and canonical identity are separate. The compiled graph includes:

- Environment
- OperationalSystem
- Problem
- Requirement
- DesiredOutcome
- Technology
- Patent
- Organization
- Capability
- DemandSignal
- Program
- Constraint
- Evidence
- OpportunityCandidate
- Opportunity
- Build

## Governing rules

A candidate may be published only when:

- all ten source records are preserved with provenance;
- the problem has at least one evidence record;
- at least two requirements exist;
- at least two technologies satisfy different requirements;
- every inferred relationship carries evidence and confidence;
- the candidate score is at least 0.75;
- permitted-use status is public or internal-demo;
- contradictions are empty;
- review state is `approved_for_demo`.

## Run

From the repository root:

```bash
python3 vertical-slices/airport-carbon-10/compile.py
python3 -m unittest vertical-slices/airport-carbon-10/test_compile.py
```

Generated output is written to:

```text
vertical-slices/airport-carbon-10/compiled/airport-carbon-10.compiled.json
```

## Acceptance test

The slice is complete when the compiler deterministically produces:

- 10 preserved source records;
- canonical entities with stable IDs;
- evidence-backed typed relationships;
- one scored candidate;
- one policy-approved canonical opportunity;
- one `MarketplaceOpportunityCardView`;
- one `OpportunityExperienceView`;
- one inherited `BuildSeedView`;
- a validation report with no errors.
