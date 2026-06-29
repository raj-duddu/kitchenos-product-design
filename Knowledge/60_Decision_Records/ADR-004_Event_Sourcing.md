---
id: ADR-004
title: Domain-Driven Event Sourcing
type: adr
status: accepted
owner: architecture
depends_on: [ADR-003]
referenced_by: [ADR-005]
tags: [event-sourcing, ddd, domain-events, household-timeline, corrections, immutability]
date: 2026
---

# ADR-004: Domain-Driven Event Sourcing

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS makes decisions on behalf of households — what to cook, what to buy, what has changed in the pantry, what was corrected. These decisions must be:

- **Explainable**: the user can see why something happened.
- **Reversible**: any automated action can be undone without data loss.
- **Traceable**: AI learning and recommendations reference the history of real household actions.
- **Auditable**: corrections and undo operations have a clear paper trail.

A traditional CRUD model (update and delete rows in place) cannot satisfy these requirements. Deleting a receipt and reversing its pantry effects requires knowing what the receipt contained, what the pantry looked like before, and what other events were caused by the import. That information is lost in a delete-based model.

---

## Decision

KitchenOS uses **domain-driven event sourcing** from day one. All meaningful household actions are recorded as immutable domain events in an append-only `domain_events` table in PostgreSQL. No domain event is ever deleted or mutated. Corrections are additional events, not mutations of prior events.

---

## Reasons

**Reversibility without data loss.**
Every automated action (receipt import, pantry deduction, shopping list generation, AI recommendation) writes a domain event. Undoing an action writes a correction or reversal event. The original event remains in the log. The user sees the full history, and the system can reconstruct any prior state.

**Household Timeline is only possible with event sourcing.**
The Household Timeline is a first-class product surface — the user-facing event log that tracks what was bought, cooked, consumed, corrected, recommended, accepted, or rejected. It cannot be built from a mutable CRUD model because updates and deletes destroy the history needed to populate it.

**AI learning requires sequential household history.**
The Household Decision Engine reads the household's event history to build context for recommendations. It needs to know not just what the pantry currently contains, but what was cooked last week, what was rejected last month, and what corrections were made. A CRUD model cannot provide this sequential history.

**Trust and explainability.**
Users must trust AI recommendations. That trust requires being able to see why a recommendation was made (what context the AI used) and being able to undo any action the system took. Event sourcing is the technical foundation that makes explainability and reversibility possible.

**Safety-critical correction flows.**
If an allergy rule is violated and a recommendation reaches a user, the system must be able to trace exactly which event caused it, what state the system was in, and what correction was applied. This is not possible without an immutable event log.

---

## What Event Sourcing Means in Practice

- Commands are issued to the system (e.g., `ImportReceipt`, `CookMeal`, `RemoveFromPantry`).
- Each command, if valid, produces one or more domain events written to `domain_events`.
- Domain events are the source of truth. Primary tables (pantry, shopping list, budget) are derived from events.
- Materialised views provide efficient read access to current household state without replaying the full event log on every request.
- The Household Timeline read model is a filtered, human-readable projection of domain events.
- No domain event is ever updated or deleted. Reversals are new events.

---

## What Event Sourcing Does NOT Mean in MVP-0

- **No full event replay infrastructure.** MVP-0 does not need the ability to rebuild all state from events from scratch. The primary tables are still maintained alongside events.
- **No distributed event bus.** Kafka, RabbitMQ, or similar are not required. Events are written to PostgreSQL and processed synchronously in MVP-0.
- **No complex projections.** Materialised views and simple read models are sufficient. CQRS is not required in its full form.

The pragmatic rule: store domain events from day one. Keep the read models simple. Add complexity only when the scale and team justify it.

---

## Alternatives Considered

**Traditional CRUD:**
Simpler to implement initially. Rejected because it makes the Household Timeline impossible to build correctly, makes correction and reversal flows complex and error-prone, and destroys the history needed for AI learning. The entire product philosophy depends on actions being explainable and reversible — CRUD cannot support this.

**Full event replay (pure event sourcing):**
No primary tables at all — all state is derived by replaying the event log. Architecturally pure but operationally expensive for MVP-0. Rejected because a small team cannot manage the operational complexity of full event replay during early product development. The hybrid approach (domain events + primary tables + materialised views) achieves the same product outcomes with lower complexity.

---

## Consequences

- All engineers must understand the domain event model before writing any feature that modifies household state.
- Every feature that creates, updates, or deletes household data must write a domain event. A feature that mutates a row without writing an event is a bug.
- Integration tests must verify the event chain, not just the API response. See ADR-003 and Engineering Handbook.
- The `domain_events` table generates high insert volume. Connection pooling must be configured from day one.
- AI learning signals must be derived only from confirmed backend events, never from unsynced local SQLite events.

---

## Related

- ADR-003: PostgreSQL (event store implementation)
- ADR-005: Modular Monolith (service structure around domain boundaries)
- Main doc, Section 32: Domain-Driven Event Architecture (source of truth for event schema, boundaries, and read models)
- Main doc, Section 42.5: Engineering Quality (event-driven integration testing pattern)
- Main doc, Section 37.8: Offline AI Context Constraint (why backend events, not local events, drive AI)
