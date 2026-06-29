---
id: ADR-005
title: Modular Monolith for Backend Architecture
type: adr
status: accepted
owner: architecture
depends_on: [ADR-004, ADR-006]
referenced_by: [ADR-006]
tags: [architecture, nestjs, modular-monolith, ddd, bounded-contexts, microservices]
date: 2026
---

# ADR-005: Modular Monolith for Backend Architecture

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS requires a backend that coordinates multiple functional domains: authentication, pantry management, shopping, cooking, receipts, AI recommendations, household timeline, goals, allergy safety, notifications, and (post-MVP) the expert marketplace.

Two primary structural approaches were considered:

- **Microservices**: independent deployable services per domain, communicating over network
- **Modular monolith**: a single deployable service with clearly bounded internal modules, no inter-service network calls

---

## Decision

KitchenOS uses a **modular monolith** for the MVP-0 backend. All domain modules live in a single NestJS application deployed as a single Cloud Run service. Module boundaries are enforced at the code level, not the network level.

---

## Reasons

**Team size does not justify microservices.**
Microservices require independent deployment pipelines, inter-service networking, distributed tracing, service discovery, and the operational overhead of managing multiple running services. A small founding team cannot manage this complexity while simultaneously building core product features. The productivity cost of microservices before reaching significant scale is well-documented.

**Transactional integrity across domains.**
KitchenOS frequently needs atomic operations across multiple domains. Scanning a receipt must update the pantry, write to the event log, update the budget, and trigger a recommendation — all in one transaction. In a microservices architecture, this requires distributed transactions or saga patterns, which are complex and failure-prone. In a modular monolith, these are standard database transactions.

**Module boundaries enforce DDD without network overhead.**
NestJS modules provide clear boundaries between domain contexts (PantryModule, ShoppingModule, RecipeModule, HouseholdModule, AIModule). These boundaries enforce the domain-driven design principles without the latency and failure surface of network calls between services.

**Easier to refactor into microservices later.**
A well-structured modular monolith with clean module boundaries is significantly easier to extract into microservices when the team and scale justify it. A monolith with poor boundaries (a "big ball of mud") is not. The discipline required to maintain module boundaries in the monolith is the same discipline required to design good microservice interfaces.

**Single deployment unit for MVP-0.**
One Cloud Run service is deployed. One Docker image is built and pushed. One service is monitored. One set of environment variables is managed. This is operationally simple for a small team.

---

## Module Structure

```text
NestJS Application (single Cloud Run service)
  │
  ├── AuthModule          (Firebase Authentication integration)
  ├── HouseholdModule     (household state, members, profiles)
  ├── PantryModule        (pantry items, quantities, expiry)
  ├── ShoppingModule      (shopping lists, generation, updates)
  ├── RecipeModule        (recipes, cook mode, pantry deduction)
  ├── ReceiptModule       (OCR integration, receipt import, deduplication)
  ├── AIModule            (Household Decision Engine, AI provider abstraction)
  ├── TimelineModule      (Household Timeline read model)
  ├── NotificationModule  (Firebase Cloud Messaging)
  ├── GoalModule          (individual nutrition and fitness goals)
  ├── SafetyModule        (allergy rules, household-level safety aggregation)
  └── EventModule         (domain_events table, event dispatch)
```

**Module boundary rules:**
- Modules communicate through defined interfaces, not direct imports of internal classes.
- No circular dependencies between modules.
- The EventModule is a shared infrastructure module. All other modules depend on it to write events; it depends on no domain module.
- The SafetyModule is called by AIModule before any recommendation leaves the system. It is never bypassed.

---

## Alternatives Considered

**Microservices from day one:**
Independent deployable services per domain. Rejected for MVP-0 because the operational overhead (service mesh, distributed tracing, inter-service auth, independent deployment pipelines) is too high for a founding team. The transactional integrity requirements across domains also make microservices significantly more complex to implement correctly.

**Single monolith without module boundaries:**
The simplest possible backend — all code in one place with no internal structure. Rejected because it accumulates technical debt rapidly and makes domain boundaries impossible to enforce or later extract. The modular monolith provides the same deployment simplicity with enforced structure.

---

## Migration Path to Microservices

When a specific module consistently bottlenecks performance, has an independent team working on it, or requires independent scaling, it can be extracted as a separate service:

```text
Phase 1 (MVP-0 → MVP-1): Full modular monolith
Phase 2 (Post-MVP, team growth): Extract AIModule as dedicated AI service (first candidate)
Phase 3 (Scale): Extract MarketplaceModule if expert marketplace grows to significant volume
```

The AIModule is the most likely first extraction candidate because AI inference is compute-intensive, has different scaling requirements from the core API, and would benefit from independent deployment and scaling.

---

## Consequences

- All engineers work in a single NestJS repository. No cross-service coordination required for MVP-0 feature development.
- Module boundaries must be actively maintained. A feature that imports a class directly from another module's internals is a boundary violation and must be rejected in code review.
- The EventModule must be treated as infrastructure, not a domain module. All domains emit events through it; it emits events through no domain module.
- The SafetyModule must be invoked by AIModule on every recommendation path. Tests must verify this (see Engineering Quality, safety-critical path coverage requirement).

---

## Related

- ADR-004: Event Sourcing (the EventModule implements the domain event model)
- ADR-006: Cloud Run (the modular monolith deploys as a single Cloud Run service)
- Main doc, Section 37.2: Backend Architecture
- Main doc, Section 34: Service Layer Architecture
