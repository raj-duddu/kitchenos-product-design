---
id: ADR-013
title: Knowledge and Implementation Live in Separate Repositories
type: adr
status: proposed
owner: architecture
depends_on: [GOV-003, DOC-000]
referenced_by: []
operating_principles: ["1. Transform Complexity into Clarity", "9. Simplicity Is a Feature"]
tags: [repositories, knowledge-system, monorepo, bridge-contract, drift, agentic-development, company-wide]
date: 2026
---

# ADR-013: Knowledge and Implementation Live in Separate Repositories

**Status:** Proposed
**Date:** 2026-07-04
**Deciders:** Founders (proposed via Architect role)
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Operating Principles:** 1 (Transform Complexity into Clarity), 9 (Simplicity Is a Feature). No conflicts identified.

---

## Context

This repository was founded on an explicit premise: it models the company and its products — vision, governance, domain models, architecture, decision records — and deliberately contains no application code, because as code and tests accumulate, company- and product-level artifacts become hard to track. With PRD-001 approaching Stage 6, the first implementation repository is about to exist, and the informal premise must become a recorded standard before code is written anywhere.

Three structural facts drive the decision:

- **Scope mismatch.** This repository is company-scoped: `Company/` governs KitchenOS, HealthOS, FinanceOS, and every future product. An implementation repository is product-scoped. A monorepo would embed the company constitution inside one product's codebase — untenable the day a second product exists.
- **Different review regimes and audiences.** Knowledge changes run through founder-gated CODEOWNERS and docs-quality CI at a deliberate cadence; code needs build/test CI, faster merges, and eventually contributors who may commit code but must not touch GDRs. Separate repositories make that a permission boundary, not a path rule.
- **The history is a product.** This repository's git log is the company's decision archaeology. Interleaving it with dependency bumps and test fixes destroys its readability — the original founding concern, still correct.

The two-class knowledge model (Documentation Philosophy rule 7) extends naturally: records and living documents live here; implementation is a third artifact class — a projection of the knowledge here into running code — with its own evolution rules and its own home.

---

## Decision

**Knowledge and implementation live in separate repositories. This repository is the knowledge repository: company constitution, governance, product knowledge through Stage 5, all decision records, and the enforcement tooling. Each product gets its own implementation repository (first: the KitchenOS repository, created when PRD-001 reaches Stage 6), containing code, tests, and Stage 6+ artifacts only.**

The boundary and the bridge are part of the decision:

- **Artifact boundary:** everything through Stage 5 lives in the knowledge repository — PRDs, Solution Designs (`45_Solution_Designs/`), all GDR/ADR/PDR/UXDR records, wireframes. Stage 6+ artifacts live in the implementation repository — code, executable `.feature` files implementing PRD scenarios, migrations, runbooks-as-code.
- **Bridge contract:** every implementation repository carries a thin entry document (`CLAUDE.md` / `CONTRIBUTING.md` in the future implementation repository, not this one) that is pure pointer, zero copied policy: the Domain Model owns the ubiquitous language and event catalogue; GOV-003 owns when an ADR is required — architecture decisions are proposed in the knowledge repository, never made in code; the Engineering Handbook owns how code ships. Context is allowed, authority is not (Documentation Philosophy rule 7, applied across repositories).
- **Decision flow is one-directional:** decisions are made and recorded here, implemented there. A change born in code that alters architecture or domain semantics must come back here as a proposed record before merging there.
- **Drift gate (build when there is code to check):** the implementation repository's CI fetches this repository and mechanically verifies cheap invariants — event names in code exist in the Domain Model catalogue, module names match bounded contexts. The Engineering Manager role's drift duty, made machine-detected.
- The pattern is company-wide: future products (HealthOS, FinanceOS, LearningOS) each get an implementation repository under the same contract, all governed by this one knowledge repository.

---

## Reasons

- Preserves the founding property: knowledge history stays readable, reviewable, and constitutionally gated as code velocity grows (Principle 1 — each audience sees a clear view of its own concern).
- One knowledge repository governing N product repositories is the only topology that scales to the multi-product vision without duplicating governance.
- Permission boundaries by repository are simpler and safer than path-based rules inside one repository (Principle 9 — least machinery).
- Agent workflows favour it: a coding agent needs a thin pointer contract and targeted reads of governing documents, not four thousand lines of vision in its working tree; a knowledge agent needs no node_modules.

---

## Alternatives Considered

### Option A: Monorepo — code joins this repository
One clone, atomic cross-cutting changes, one CI. Rejected: buries the constitution inside a product, destroys history readability (the founding concern), forces path-based permissions, and turns docs-quality and build CI into one entangled pipeline. The atomicity benefit is small because the lifecycle already sequences docs-first.

### Option B: Docs live in the code repository (`/docs` folder)
The industry default. Rejected for the same scope mismatch — it is Option A with the hierarchy inverted, and it makes company-wide governance a subfolder of KitchenOS.

### Option C: Knowledge split per product (each code repository carries its product's docs; a small company repository holds the constitution)
Superficially cleaner ownership. Rejected: fragments the knowledge graph — `knowledge_index` and `governance_check` lose the single tree they validate; cross-product impact analysis (`--impact GDR-002`) becomes multi-repository archaeology; the Platform extraction path (Canonical Data Model) has no home.

### Option D: Do nothing (decide when the code repository is created)
Rejected: the code repository is weeks away at most, and an unrecorded topology decision would be relitigated by every future engineer ("why isn't this a monorepo?"). This record exists precisely to answer that question once.

### Option E (chosen): Separate repositories with a defined bridge contract

---

## Consequences

### Positive
- Knowledge history remains the company's readable decision archaeology; constitutional review gates stay clean.
- Repository-level access control: contractors and future engineers get code access without constitution write access.
- The topology scales to N products with one governing knowledge repository.

### Negative
- Cross-repository references escape `knowledge_index --check` — links from code to knowledge (and back) are not machine-validated until the drift gate exists.
- One feature can require two PRs (living-document update here, implementation there). Accepted: the docs-first lifecycle already sequences this.
- The bridge contract is a new artifact to keep honest — it must remain pointer-only, and reviewing that is a human duty until tooling covers it.

### Risks
- **Bridge rot:** the implementation repository's entry contract quietly accumulates copied policy that then drifts. Mitigation: the contract is reviewed against "context allowed, authority not" in code-repository PRs touching it; the drift gate later checks the mechanical invariants.
- **Two-repository friction tempts consolidation:** under deadline pressure, someone proposes "just put the docs in the code repo." This record is the standing answer; superseding it requires a new ADR, not a habit.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-04 | Proposed | Claude (Architect role), sponsored by @raj-duddu | PR # (add on merge) |

---

## Related

- `00_Knowledge_Map.md` — Documentation Philosophy rule 7 (two classes of artifact; implementation is a projection with its own home)
- `Company/Governance/Architecture_Governance.md` — ADR triggers ("a decision that was previously informal becomes a standard"); decision flow the bridge contract enforces
- `Process/Quality_Gates.md` — the knowledge repository's enforcement; the implementation repository gets its own gates plus the drift gate
- `Products/KitchenOS/50_Engineering_Handbook.md` — owns how code ships in the implementation repository
- PRD-001 — the feature whose Stage 6 creates the first implementation repository
- `Knowledge/Canonical_Data_Model.md` — the future `Platform/` extraction assumes one knowledge repository across products
