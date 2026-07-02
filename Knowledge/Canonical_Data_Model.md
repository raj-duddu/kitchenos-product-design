---
id: KNOW-002
title: Canonical Data Model
type: knowledge
status: active
owner: founders
scope: company-wide
date: 2026
---

# Canonical Data Model

> Shared domain concepts that exist across all Amanaska products. When a new product is built, it inherits these concepts rather than reinventing them.
> Product-specific extensions live in each product's Domain Model.

---

## Core Entities

### Identity
The authentication mechanism. The only entity that contains PII (email).

```text
identities
├── id (uuid)                ← identity_id throughout the system
├── email                    ← THE ONLY PII IN THE SYSTEM
├── auth_provider            google | apple | email
└── created_at
```

Owned by: Auth layer (separate schema).
**Never read by the domain layer or intelligence layer.**

---

### Person
A human being in the Amanaska platform. Global — the same `person_id` is used across KitchenOS, HealthOS, FinanceOS, and any future product.

```text
persons
├── id (uuid)                ← person_id used everywhere
├── identity_id              ← FK to identities; never used in AI or analytics
├── age_group                adult | teen | child | infant
└── age_range                25-34 | 35-44 | etc. (optional)
```

Owned by: Domain layer.
**person_id is the universal cross-product identifier. identity_id is the auth bridge and must never leak into product logic.**

---

### Relationship
How a Person relates to a product's primary context (household, account, organisation). The concrete entity is product-specific, but the pattern is canonical.

In KitchenOS: `HouseholdMembership` (person_id + household_id + role)
In HealthOS (future): `HealthAccountMembership` (person_id + account_id + role)
In FinanceOS (future): `FinancialHouseholdMembership` (person_id + household_id + role)

The pattern: a Person may belong to multiple contexts. The relationship entity carries role, permissions, and context-specific display preferences.

---

### ConsentGrant
A scoped, time-bounded, revocable permission granted by a user for a specific data use.

```text
consent_grants
├── id (uuid)
├── grantor_person_id        ← who granted it
├── grantee_id               ← who received it (expert, organisation, service)
├── scope                    ← specific data types granted
├── granted_at
├── expires_at               ← null if open-ended
└── revoked_at               ← null if active
```

Owned by: Domain layer.
**Scope cannot be broadened after grant creation. New scope requires a new grant.**

---

## The Platform Stack

The full Amanaska platform stack, from identity to experience. Every product is built on this foundation:

```text
Identity         ← who you are (Auth layer)
     │
     ▼
Person           ← the business entity (Domain layer)
     │
     ▼
Relationship     ← how you relate to a context (household, account, org)
     │
     ▼
Domain           ← what you do in that context (pantry, meals, finances, learning)
     │
     ▼
Events           ← what happened (append-only, immutable)
     │
     ▼
Intelligence     ← what the AI has learned about you (beliefs, confidence, patterns)
     │
     ▼
Decision         ← what the AI recommends (decision support, not autonomous action)
     │
     ▼
Experience       ← what you see and do
```

This stack applies to every product Amanaska builds. KitchenOS is the first full implementation. HealthOS, FinanceOS, and LearningOS will build on the same Identity and Person foundation.

---

## What Shared Platform Will Own

When a second product is built, the following will be extracted from KitchenOS into a shared `Platform/` layer:

| Service | Description |
|---|---|
| Identity Service | Auth, session management, token issuance |
| Person Service | `persons` table, global person_id registry |
| Consent Service | `consent_grants` management across all products |
| Notification Service | FCM, email, push delivery |
| AI Platform | Shared model hosting, prompt versioning, evaluation infrastructure |
| Observability | Logging, tracing, alerting — product-agnostic |
| Billing | Payment processing, subscription management |

Until a second product exists, these live in KitchenOS. This document records the extraction candidates so that when the time comes, the boundaries are already designed.

---

## Related

- `Company/Governance/GDRs/GDR-002_Privacy_By_Design.md` — privacy principles that govern all shared data
- ADR-009 — Identity isolation
- ADR-011 — Person as a global domain concept
- `Knowledge/Patterns/Privacy_By_Design.md` — four-layer isolation pattern
- `Products/KitchenOS/20_Domain_Model.md` — KitchenOS-specific extension of this canonical model
