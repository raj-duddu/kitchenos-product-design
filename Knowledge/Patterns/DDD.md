---
id: KNOW-PAT-001
title: Domain-Driven Design
type: knowledge-pattern
status: active
owner: founders
scope: company-wide
related: [KNOW-PAT-002, KNOW-PAT-003]
date: 2026
---

# Domain-Driven Design (DDD)

> This document captures the DDD concepts used across all Amanaska products. It is a reference, not a tutorial. For product-specific application of these concepts, see each product's Domain Model.

---

## Why We Use DDD

Complex business domains — food decisions, health management, financial planning, learning — cannot be modelled accurately with simple CRUD data models. DDD gives us:

- A shared language between product and engineering that eliminates translation errors.
- A domain model that reflects real business concepts, not database tables.
- Clear boundaries between different parts of the system (bounded contexts) that allow independent evolution.
- A natural fit for event sourcing — every state change is a domain event with business meaning.

---

## Core Concepts We Apply

### Ubiquitous Language
The vocabulary used by product, engineering, QA, and support within a bounded context. Every product's Domain Model defines its ubiquitous language. Code, tickets, tests, and conversations use the same terms. No synonyms.

### Bounded Context
A well-defined boundary within which the domain model is internally consistent. Different contexts may use the same word differently (e.g., "recommendation" in KitchenOS means a meal suggestion; in a future learning product it would mean a course). The boundary makes each meaning explicit.

In Amanaska products, bounded contexts are:
- Identified in the Domain Model
- Mapped to database schemas or service boundaries
- Named explicitly in domain events (`meal.*`, `pantry.*`, `shopping.*`)

### Aggregate and Aggregate Root
An aggregate is a cluster of domain objects treated as a unit for data changes. The aggregate root is the only entry point — external code never holds references to internal aggregate members directly.

Example: `Household` is an aggregate root. `HouseholdMembership` is an entity within it. To add a member, you call `Household.addMember()` — you never write directly to `household_memberships`.

### Domain Events
Something that happened in the domain, named in past tense, immutable, append-only. The foundation of our event sourcing architecture.

- `MealRecommendationAccepted` — not `UpdateMealStatus`
- `ReceiptScanned` — not `InsertReceipt`
- `PantryItemConsumed` — not `DecrementQuantity`

### Repository Pattern
A collection-like interface over the persistence layer for aggregates. Domain logic never touches the database directly. The repository translates between domain objects and the persistence layer.

### Domain Service
Logic that doesn't naturally belong on an entity or value object. The `AllergyCuard`, the `HouseholdDecisionEngine`, and the `ConfidenceScorer` are domain services — they operate on multiple aggregates and express business logic that can't live on a single entity.

---

## What We Don't Use

- **Anemic Domain Model** — entities with no behaviour, only getters/setters. All business logic lives in the domain, not in services that manipulate dumb objects.
- **God aggregates** — one aggregate that owns everything. Each aggregate has a clear, narrow responsibility.
- **Shared databases between contexts** — each bounded context owns its tables. Cross-context access goes through events or APIs, not direct SQL joins.

---

## How This Applies to KitchenOS

See `Products/KitchenOS/20_Domain_Model.md` for the full KitchenOS application of these concepts, including:
- Bounded contexts table
- Aggregate roots and entities
- Domain events catalogue
- Ubiquitous language glossary
- Business invariants
