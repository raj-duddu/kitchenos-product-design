---
id: ADR-009
title: Privacy-by-Design — Identity Isolation and Data Minimisation
type: adr
status: accepted
owner: architecture
depends_on: [ADR-003, ADR-004, ADR-007, ADR-008]
referenced_by: []
tags: [privacy, identity, data-minimisation, security, gdpr, member-model, identity-isolation, pii]
date: 2026
---

# ADR-009: Privacy-by-Design — Identity Isolation and Data Minimisation

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS stores sensitive household data: allergies, dietary restrictions, health goals, nutrition preferences, height, weight, and medical conditions. It also needs to identify users for authentication, account recovery, and multi-device sync.

The naive approach — a `users` table with name, email, and all profile data — is common and simple, but it creates a single point of failure where a data breach exposes both identity (who the person is) and intelligence (what the system knows about them). It also tends to accumulate fields over time without a clear principle governing what should or should not be stored.

There are two compounding problems specific to KitchenOS:

1. **The Collective Intelligence pipeline** extracts anonymised observations from household data. If identity fields (email, name) exist in the same schema as intelligence fields (allergies, goals, preferences), the anonymisation pipeline must actively strip them — and one mistake exposes PII in the collective store.

2. **Indirect identifiers**: even without a name, combinations of data (age, location, household size, specific dietary restrictions) can re-identify individuals. Minimising what is stored reduces re-identification risk.

The question is: what is the right architectural boundary between identity and intelligence, and what data should the system collect at all?

---

## Decision

**We will apply privacy-by-design through two mechanisms: identity isolation and data minimisation.**

**Identity isolation:** The `identities` table (authentication layer — email, auth provider) and the `household_members` table (intelligence layer — member role, age group, goals, allergies) are physically separated into different PostgreSQL schemas. The join between them via `identity_id` must never be traversed by the intelligence layer, the Household Intelligence Model, the Recommendation Engine, or the Collective Intelligence pipeline.

**Data minimisation:** Every field in the data model must answer: what recommendation, safety check, or household decision does this enable? If there is no clear answer, the field is not stored. Age ranges are stored instead of exact ages. Display names are optional and UI-only. Height and weight are stored only when an active nutrition goal requires them, scoped to that member.

---

## The Three-Layer Model

```text
Identity Service (separate schema)
  identities
    id              uuid
    email           string    ← the only PII in the system
    auth_provider   string    google | apple | email
    created_at      timestamptz

        ↓  identity_id (the only bridge — never crossed by AI)

Household Service (intelligence schema)
  household_members
    id              uuid      ← member_id; used throughout intelligence layer
    household_id    uuid
    identity_id     uuid      ← foreign key up to identities; never read by AI
    member_type     string    adult | child | teen
    age_group       string    25-34 | 35-44 | child | etc.
    display_name    string, nullable  ← UI only; never used in recommendations

        ↓

Intelligence Layer (same intelligence schema)
  dietary_constraints, user_goals, nutrition_preferences
    all keyed on member_id only
    no email, no name, no identity_id
```

---

## Reasons

**A breach of the intelligence schema must not expose identity.**
If an attacker accesses the intelligence schema — allergies, goals, preferences, learned behaviours — they must not be able to identify who those records belong to. Physical schema separation enforces this at the infrastructure level, not just by application convention.

**The Collective Intelligence pipeline must be safe by construction.**
The anonymisation pipeline reads from the intelligence schema to extract observations. If email or name exists in the same schema, every pipeline run is a potential exposure. Separating the schemas makes the pipeline safe by construction — there is nothing identifying to accidentally include.

**Removing names does not remove privacy obligations; minimising data reduces them.**
Privacy regulations (GDPR, CCPA) treat indirect identifiers as personal data when they can re-identify individuals in combination. Collecting less data — age range instead of exact age, no name, no address — reduces the total re-identification surface. This is a genuine privacy improvement, not just a compliance posture.

**Exact age is not required.** The nutrition estimation and meal sizing functions require knowing whether a member is an adult, teen, or child — and optionally a broad age range for calorie targets. An exact birth date adds no product value and adds legal and security obligations.

**Names are not required for recommendations.** The Recommendation Engine, Allergy Guard, Household Intelligence Model, and Collective Intelligence pipeline all operate on `member_id`. None of them require or use a person's name. Display names exist purely for household UI convenience and are stored as optional, nullable fields that are never passed to AI or data pipelines.

**This aligns with "Trust is earned through transparency."**
Users who understand that KitchenOS does not store their name internally — and can verify what it does store through the transparency screen — have a stronger trust foundation than users who must take data practices on faith.

---

## What Is and Is Not Stored

| Data | Decision | Reason |
|---|---|---|
| Email | Stored in Identity Service only | Required for auth, account recovery, multi-device sync |
| Name | Not stored internally | Recommendations do not require it; optional `display_name` for UI |
| Exact age / birth date | Not stored | Age range is sufficient for nutrition estimation |
| Age group / range | Stored on `member_id` | Required for calorie targets and recipe sizing |
| Allergies | Stored on `member_id` | Safety-critical; must be asked, never inferred |
| Height / weight | Stored on `member_id`, only when goal active | Required for body-composition nutrition goals only |
| Medical conditions | Stored on `member_id`, only when goal active | Scoped to member; not visible to other members by default |
| Location | Metro region only (Collective Intelligence) | Never exact address |
| Shopping history | Stored as household-level receipts | No name attached; `household_id` only |

---

## Alternatives Considered

### Option A: Single `users` table with all profile data

One table containing email, name, age, allergies, goals, preferences. Standard approach.

Rejected because:
- A single breach exposes both identity and sensitive health/dietary data.
- The Collective Intelligence anonymisation pipeline must actively strip identity fields — one omission exposes PII in the collective store.
- Accumulates fields without a principle governing what should be stored.
- Harder to reason about privacy obligations when data is commingled.

### Option B: Separate tables in the same schema, by convention

Keep `identities` and `household_members` as separate tables but in the same PostgreSQL schema, relying on application-level access controls.

Partially accepted for MVP-0 (schema separation is complex to set up immediately), but the principle must be established now. Application-level access controls are enforced from day one. Physical schema separation is a hard requirement by MVP-1 before any sensitive health or nutrition data is collected.

### Option C: Store everything, anonymise on export only

Collect full user data including names, ages, and preferences; anonymise only when contributing to the Collective Intelligence Model.

Rejected because:
- Does not reduce re-identification risk in the primary database.
- Anonymisation on export is more error-prone than not collecting the data in the first place.
- Contradicts data minimisation as an engineering principle.
- If the primary database is breached, full identity + intelligence exposure occurs regardless of export anonymisation.

---

## Consequences

### Positive

- A breach of the intelligence schema cannot expose user identities.
- Collective Intelligence pipeline is safe by construction — no identity in the intelligence schema.
- Reduced re-identification risk through data minimisation.
- Defensible under GDPR, CCPA, and anticipated future privacy regulations.
- Aligns with product principle "Trust is earned through transparency."
- Account recovery and multi-device sync work correctly via the `identity_id` bridge.

### Negative

- Slightly more complex data model than a single `users` table.
- Engineers must understand the boundary and enforce it. Adding an identity field to the intelligence schema is a security violation, not just a design smell.
- Physical schema separation adds operational complexity in MVP-1 onwards.

### Risks

- **Boundary drift:** A developer adds `user_email` to a query for logging or debugging. Mitigation: code review policy, database-level access controls on the intelligence schema, explicit rule in engineering handbook.
- **MVP-0 pragmatism:** Physical schema separation may not be implemented immediately. The application-level rule (never pass `identity_id` or email to AI or data pipelines) must be enforced from day one, even before physical separation is complete.

---

## Engineering Rules (Non-Negotiable)

1. The `identities` table is only read by the auth layer (login, account recovery, invite flow).
2. The `identity_id` field on `household_members` is never included in any query that feeds the Recommendation Engine, Household Intelligence Model, or Collective Intelligence pipeline.
3. The `display_name` field on `household_members` is never included in AI prompts, domain event payloads, or data pipeline outputs.
4. Any PR that adds an identity field (email, name, phone, address, exact age) to the intelligence schema must be rejected in code review.
5. Height, weight, and medical conditions are only stored when an active goal of the relevant type exists for that member. They are deleted when the goal is removed.

---

## Related

- ADR-003: PostgreSQL (schema strategy for separation)
- ADR-004: Domain-Driven Event Sourcing (domain events carry `member_id`, not `user_id` or name)
- ADR-007: Household Intelligence Model Separation (intelligence model operates on member_id)
- ADR-008: Collective Intelligence Model (anonymisation pipeline reads intelligence schema only)
- `Knowledge/10_Product_Vision.md`, Sections 8.10 and 8.11: Data Minimisation and Identity Isolation principles
- `Knowledge/20_Domain_Model.md`: Privacy-by-Design note and refactored data model
- `Knowledge/40_Technical_Architecture.md`, Section 23: Identity Service and Data Minimisation Architecture
