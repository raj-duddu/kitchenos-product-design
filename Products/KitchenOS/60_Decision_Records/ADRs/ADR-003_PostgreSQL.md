---
id: ADR-003
title: PostgreSQL as Primary Database
type: adr
status: accepted
owner: architecture
depends_on: [ADR-002]
referenced_by: [ADR-004]
tags: [database, postgresql, event-sourcing, cloud-sql, acid, materialised-views]
date: 2026
---

# ADR-003: PostgreSQL as Primary Database

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS requires a primary database for household data (users, pantry, shopping lists, recipes, budgets), an event store for the append-only `domain_events` table, and materialised views for the Household Timeline read model and household state.

The data model is relational: households have members, members have profiles and goals, pantry items belong to households, domain events reference aggregates by ID. Transactional integrity across multiple tables is required, particularly for event sourcing (a command must write to both the primary table and the `domain_events` table atomically).

The main candidates were:

- **PostgreSQL**
- **MySQL / MariaDB**
- **MongoDB**

---

## Decision

**PostgreSQL** was chosen as the primary and event store database for KitchenOS.

---

## Reasons

**Relational model fits the domain.**
The KitchenOS domain is inherently relational. Household → Members → Profiles → Goals → Events is a clear relational hierarchy. A document database would introduce denormalisation complexity without benefit.

**ACID transactions for event sourcing correctness.**
The event sourcing model requires that a command writes to both the primary table and the `domain_events` table atomically. PostgreSQL ACID transactions guarantee this. A failure midway leaves no partial state. This is not a nice-to-have — it is a correctness requirement for the append-only event log.

**Native support for append-only patterns.**
The `domain_events` table is insert-only, never updated or deleted. PostgreSQL handles high-insert-rate workloads well with proper indexing. The `SERIAL` or `UUID` primary key pattern for events is standard Postgres.

**Materialised views for read models.**
PostgreSQL materialised views are used for the household state read model and Household Timeline read model. These allow efficient reads of derived state without recomputing from the full event log on every request. This is a critical performance decision for the Home screen.

**Managed via Cloud SQL.**
Cloud SQL (PostgreSQL) on GCP provides automated backups, point-in-time recovery, read replicas (for Phase 2+ scaling), and no server management. It integrates directly with Cloud Run via Cloud SQL Proxy.

**Event sourcing on PostgreSQL is well-understood.**
Kafka, EventStoreDB, and distributed event buses are not required for MVP-0. PostgreSQL as both primary store and event store is a proven pattern for products at KitchenOS's scale. The complexity of a distributed event bus is not justified until the product has validated its core loop with tens of thousands of households.

---

## Alternatives Considered

**MySQL / MariaDB:**
Comparable relational capabilities. Rejected because PostgreSQL has stronger support for JSON columns (useful for the event envelope payload), more powerful materialised view support, and better GCP Cloud SQL feature parity for advanced Postgres-specific features.

**MongoDB:**
Document model, flexible schema, good for rapid prototyping. Rejected because ACID transaction support across multiple collections in MongoDB (multi-document transactions) adds complexity and is less mature than PostgreSQL's native transaction model. The relational nature of the KitchenOS domain makes a document model a poor fit.

**EventStoreDB:**
Purpose-built for event sourcing. Rejected for MVP-0 because it requires self-hosting or a separate managed service, adds operational complexity, and the `domain_events` table in PostgreSQL is sufficient for thousands of households. EventStoreDB is a valid future option if the event volume outgrows PostgreSQL.

---

## Consequences

- The `domain_events` table is append-only from day one. No row is ever updated or deleted. Corrections are additional events, not mutations.
- Connection pooling via Cloud SQL Proxy or PgBouncer must be configured from day one, not at scale. The append-only event table creates high insert volume.
- Materialised views must be refreshed on a schedule or triggered after significant events. Stale read models are acceptable within defined freshness windows.
- Integration tests must use real PostgreSQL (via Testcontainers), not mocks. Mock databases will not catch constraint violations or materialised view behaviour.

---

## Related

- ADR-004: Event Sourcing (the event store lives in PostgreSQL)
- ADR-002: GCP (Cloud SQL is the managed PostgreSQL service)
- Main doc, Section 37.3: Database Strategy
- Main doc, Section 32: Domain-Driven Event Architecture
- Main doc, Section 42.5: Engineering Quality (Testcontainers requirement)
