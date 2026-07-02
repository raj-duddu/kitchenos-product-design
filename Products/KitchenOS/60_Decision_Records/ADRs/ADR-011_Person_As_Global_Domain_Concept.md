---
id: ADR-011
title: Person as a Global Domain Concept, Separated from HouseholdMembership and Intelligence Model
type: adr
status: accepted
owner: architecture
depends_on: [ADR-009, ADR-007, ADR-008]
referenced_by: []
tags: [domain-model, person, household-membership, identity, intelligence, ddd, facts-vs-beliefs, platform-architecture]
date: 2026
---

# ADR-011: Person as a Global Domain Concept, Separated from HouseholdMembership and Intelligence Model

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

The previous domain model collapsed three distinct concepts into one `household_members` table:

1. Who a person *is* globally (age, allergies, goals, dietary restrictions)
2. How a person *relates* to a specific household (role, permissions, notifications)
3. What the AI has *learned* about a person (preferences, habits, confidence scores)

This conflation creates several problems:

- A Person's allergy is treated the same as a UI preference, even though one is a safety-critical domain fact and the other is a convenience setting.
- When a person joins a second household, there is no clean model for their global profile — do we duplicate rows? Do allergies apply per-household?
- The Household Intelligence Model has nowhere clean to live — it ends up mixed into member profile data, making facts and beliefs indistinguishable.
- Queries that need "what are this person's constraints?" must join through household context, even though constraints are person-global.
- The platform cannot be extended beyond KitchenOS because the Person concept is inseparable from the Household concept.

The root cause: we treated `household_members` as both a person record and a relationship record, and then also allowed it to mix in AI-learned beliefs.

---

## Decision

**We will introduce `Person` as a first-class domain aggregate, separate from `HouseholdMembership` and entirely separate from the Household Intelligence Model.**

The four-layer model:

```text
Layer 1 — Auth         identities         email, auth provider (auth schema)
Layer 2 — Person       persons            stable domain facts (domain schema)
Layer 3 — Domain       household_memberships, dietary_constraints, user_goals, ...
Layer 4 — Intelligence household_intelligence_model  (intelligence schema)
```

**`Person` owns:**
- `age_group` (adult, teen, child, infant)
- `age_range` (optional, for nutrition estimation only)
- `identity_id` (the single bridge to the auth layer — never read by AI)

**`PersonProfile` (owned by Person via Profile & Safety context) owns:**
- `dietary_constraints` — allergies, intolerances, medical dietary restrictions
- `user_goals` — nutrition and health goals
- `nutrition_preferences` — calorie awareness, protein priority, preferred meal types

**`HouseholdMembership` owns:**
- `person_id` → `persons.id`
- `household_id` → `households.id`
- role, permissions, status, joined_at
- `display_name` (optional, UI-only, never used in AI)
- notification_preferences

**`Household Intelligence Model` owns:**
- Learned cuisine affinity
- Behavioural patterns (shopping frequency, typical cook time, meal acceptance rates)
- Confidence scores
- Nothing from domain or auth layers

---

## The Critical Distinction: Facts vs Beliefs

| Kind | Example | Owned by | Properties |
|---|---|---|---|
| **Domain fact** | Peanut allergy | Person (domain schema) | Explicitly stated, authoritative, never inferred |
| **AI belief** | 92% mushroom rejection | Household Intelligence Model | Learned, probabilistic, can be corrected or replaced |

These must never be conflated. The domain model must never accept AI-inferred data as a fact. The intelligence model must never replace explicit domain facts with learned beliefs.

The test: **does this concept exist if KitchenOS has no AI?** If yes, it belongs in the domain. If only an AI could produce it, it belongs in the intelligence layer.

---

## Reasons

**A Person's constraints are global, not household-specific.**
Raj's peanut allergy applies at home, at his parents' house, and anywhere else he eats. Storing it on `household_members` requires duplication per household or complex join logic when he joins a second household. Storing it on `Person` is correct: the person has the allergy, not the membership.

**Identity ≠ Person.**
An Identity is an auth mechanism — a Firebase UID, an email address, a sign-in method. A Person is a human being. The same Person can change their email, switch auth providers, or re-authenticate without changing who they are. Conflating these two means authentication changes affect profile data, which is wrong.

**Person ≠ Intelligence.**
Goals and allergies are stated explicitly by the Person and are authoritative. Cuisine preferences learned from behaviour are probabilistic beliefs. They are different kinds of knowledge. Domain facts are the ground truth. Intelligence beliefs are the AI's working model, which may be wrong and must be correctable. Storing both in the same table makes it impossible to distinguish which one to trust.

**The MealSession needs a clean participant model.**
A MealSession's `participants` list references `person_id`. The Recommendation Engine loads each participant's `PersonProfile` to compute combined constraints. This only works cleanly if PersonProfile is keyed on `person_id` and global — not scoped to a particular household membership.

**This is the right foundation for the Amanaska platform.**
The Identity → Person → Relationship → Domain → Intelligence layering is not KitchenOS-specific. It applies to HealthOS, FinanceOS, LearningOS, and every future Amanaska product. KitchenOS is where we establish this pattern. Getting it right now means future products inherit a clean foundation rather than a KitchenOS-specific entanglement.

---

## What Changed

| Previous model | New model |
|---|---|
| `household_members.member_type` | `persons.age_group` |
| `household_members.age_group` | `persons.age_range` |
| `household_members.identity_id` | `persons.identity_id` |
| `dietary_constraints.member_id` | `dietary_constraints.person_id` |
| `user_goals.member_id` | `user_goals.person_id` |
| `nutrition_preferences.member_id` | `nutrition_preferences.person_id` |
| `meal_session_participants.member_id` | `meal_session_participants.person_id` |
| `consent_grants.member_id` | `consent_grants.person_id` |
| `expert_plans.member_id` | `expert_plans.person_id` |
| `client_provider_relationships.member_id` | `client_provider_relationships.person_id` |

---

## Alternatives Considered

### Option A: Keep household_members, add a separate persons table as a view

Introduce `persons` as a view over `household_members` with deduplication. Profile data stays on `household_members`.

Rejected because:
- Allergies and goals are still physically scoped to a membership row. Multi-household persons require duplication.
- The view approach hides the problem rather than solving it.
- Future products cannot reuse the Person concept if it is a view over a kitchen-specific table.

### Option B: Separate table but same schema as household_memberships

Introduce `persons` as a proper table but keep it in the same PostgreSQL schema as `household_memberships` and intelligence data.

Partially accepted: the schema separation between auth and domain is the hard requirement. Separating persons from intelligence within the domain schema by application-level convention is acceptable for MVP-0. Physical schema separation between domain and intelligence is required by MVP-1.

### Option C: Keep the three concepts merged, handle multi-household via duplication

Copy profile data to each membership when a person joins a second household. Keep memberships as the source of truth.

Rejected because:
- Allergy updates must be applied to every membership row — a correctness and safety hazard.
- Cannot distinguish global facts from household-specific context.
- Does not scale to the platform architecture.

---

## Consequences

### Positive

- Person's constraints are single-source-of-truth across all households they belong to.
- MealSession participant model is clean: `person_id` → load PersonProfile → compute constraints.
- Domain facts and AI beliefs are physically separated — no ambiguity about which to trust.
- Platform-ready: the Identity → Person → Relationship → Domain pattern applies to all future Amanaska products.
- Allergy Guard always reads the same PersonProfile regardless of which household context the session is in.

### Negative

- More tables than the previous model. Engineers must understand the four-layer separation.
- Login resolution is slightly more complex: `identity_id` → `person_id` → `household_memberships`. Acceptable — this happens once per session.

### Risks

- **Boundary drift:** Developer adds a learned preference directly to `persons`. Mitigation: code review policy; PersonProfile only accepts explicit user input, never AI output.
- **Multi-household edge cases in MealSession:** A guest who is not a member of the hosting household needs a `person_id`. Mitigation: a Person can be created and added as a `guest` HouseholdMembership for the duration of their visit.

---

## Engineering Rules

1. `persons` owns only stable, globally-true facts about a human being. No learned preferences, no AI-generated data.
2. `dietary_constraints`, `user_goals`, and `nutrition_preferences` are keyed on `person_id` — never on `household_membership_id`.
3. The recommendation engine receives `person_id` and `household_id`. It loads PersonProfile from the domain schema. It loads learned preferences from the intelligence schema. These are kept separate in memory and in persistence.
4. The `identity_id` field on `persons` is never read by the intelligence layer, the recommendation engine, or any data pipeline.
5. A Person's allergies from one household automatically apply when that person participates in a MealSession in any other household.

---

## Related

- ADR-009: Privacy-by-Design — Identity Isolation and Data Minimisation
- ADR-007: Household Intelligence Model as a Separate Architectural Layer
- ADR-008: Collective Intelligence Model with Explicit Opt-In
- `Knowledge/20_Domain_Model.md`: Person aggregate, four-layer connection diagram
- `Knowledge/40_Technical_Architecture.md`, Section 23: Four-Layer Model
- `Knowledge/10_Product_Vision.md`, Sections 8.11 and 9A: Four Layers and Amanaska Platform Architecture
