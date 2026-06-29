---
id: DOC-020
title: KitchenOS Domain Model
type: domain-model
status: active
owner: architecture
depends_on: []
referenced_by: [DOC-010, DOC-040, DOC-050, ADR-004]
tags: [domain-model, ddd, bounded-contexts, aggregates, entities, domain-events, ubiquitous-language, event-sourcing, household, pantry, shopping, marketplace]
date: 2026
---

# KitchenOS: Domain Model

> This document is the authoritative source for what KitchenOS knows and how it thinks. It defines the ubiquitous language, bounded contexts, aggregates, data model, and domain events. All engineers, AI agents, and product decisions should use the terms defined here exactly and consistently. Product decisions live in `10_Product_Vision.md`. Technical implementation of these concepts lives in `40_Technical_Architecture.md`.

---

## Ubiquitous Language

These terms have precise meanings within KitchenOS. Use them exactly as defined. Do not substitute synonyms.

| Term | Definition |
|---|---|
| **Household** | The primary unit of KitchenOS. One or more people sharing a kitchen, pantry, shopping, and food decisions. All data belongs to a Household. |
| **Member** | A person who belongs to a Household. Has individual allergies, dietary constraints, and goals. |
| **Pantry** | The current known food inventory of a Household. Always a projection of pantry domain events. |
| **PantryItem** | A single food item in the Pantry with quantity, unit, and optional expiry. |
| **ShoppingList** | An ordered collection of items the Household intends to purchase. |
| **ShoppingItem** | A single item on a ShoppingList. Has a status: pending, purchased, or removed. |
| **Recipe** | A set of ingredients and instructions for preparing a meal. May be system-provided or expert-provided. |
| **MealPlan** | A structured set of meals assigned to days and meal types for a Household for a period. |
| **Budget** | A spending target for grocery and food purchases. Tracked per period (weekly or monthly). |
| **Household Decision Engine** | The AI coordination layer that turns household context into safe, trusted food decisions. Never acts autonomously. Always produces recommendations for user approval. |
| **Allergy Guard** | The deterministic safety check that runs on every recommendation, substitution, and expert suggestion against household safety rules. Never bypassed. |
| **Household Timeline** | The user-facing, human-readable event log of the Household. A read model over the domain event stream. Distinct from the audit log. |
| **Domain Event** | An immutable record of something meaningful that happened in the Household. Written to the `domain_events` table. Never deleted. |
| **Command** | A user or system request to change household state. Commands produce events. The UI shows commands; the ledger records events. |
| **Reversal Event** | A domain event that reverses the effects of a prior event. Does not delete the original event. |
| **Correction Event** | A domain event that records a change in interpretation of a prior event (e.g., consumption re-classified as waste). |
| **Household Safety Rules** | Household-level allergy and dietary rules derived from individual member `dietary_constraints`. Never set independently. |
| **Expert** | A verified nutritionist, dietitian, fitness coach, or wellness practitioner who can access permissioned household data and provide plans. |
| **Provider** | The organisation or individual entity that Expert accounts belong to. May be an independent expert or a clinic, gym, or wellness company. |
| **Expert Plan** | A structured nutrition or fitness plan created by an Expert for a specific Member. Requires user approval before affecting household state. |
| **Expert Recommendation** | A specific suggestion within an Expert Plan (a meal, recipe, substitution, or shopping item). Must pass Allergy Guard and requires user approval. |
| **Consent Grant** | Explicit, scoped, time-bounded permission a Member gives an Expert to access specific household data. |
| **Cook Mode** | The active cooking session feature. Guides users step-by-step through a recipe and deducts ingredients from the Pantry on completion. |
| **Receipt OCR Pipeline** | The async process: Cloud Vision API scan → item extraction → pantry update → domain event → budget update. |
| **Sync Engine** | The mobile component managing the SQLite pending event queue, conflict resolution on reconnect, and online/offline transitions. |
| **Staleness Indicator** | A visible UI signal that data may be outdated. Required whenever cached or offline data is shown. |
| **Learning Impact** | A field on domain events indicating whether the event should influence future AI recommendations. Some corrections explicitly carry `no_learning_impact`. |
| **Aggregate Root** | A DDD aggregate root: the single entry point for all state changes within an aggregate. Only the aggregate root can emit domain events for its aggregate. |

---

## Bounded Contexts

KitchenOS is organised into the following bounded contexts. Each context owns its domain events and data. No context mutates another context's primary tables directly — it emits events or calls domain services.

| Bounded Context | Owns | Events belong to |
|---|---|---|
| **Household** | Household, Member, roles, permissions, shared settings | `household.*` |
| **Profile & Safety** | Allergies, dietary constraints, goals, household safety rules | `profile.*`, `safety.*` |
| **Receipt** | Receipt scanning, OCR, item extraction, duplicate detection | `receipt.*` |
| **Pantry** | Pantry inventory, quantities, expiry, consumption, waste | `pantry.*` |
| **Shopping** | Shopping lists, items, purchase status | `shopping.*` |
| **Planning & Recipe** | Meal plans, recipes, recommendations, substitutions | `planning.*` |
| **Cook Mode** | Cooking sessions, step tracking, pantry deduction | `cook.*` |
| **Budget** | Grocery spend tracking, budget periods, reversals | `budget.*` |
| **Expert Marketplace** | Providers, experts, plans, recommendations, consent | `marketplace.*` |
| **Correction & Activity** | Reversal events, undo flows, Household Timeline grouping | `correction.*` |

---

## Aggregate Roots

An aggregate root is the authoritative object for a cluster of related entities. All state changes within the aggregate go through the root.

### Household
The primary aggregate. Every other aggregate belongs to or references a Household.

**Entities within aggregate:** Member, HouseholdSafetyRules

**Invariants:**
- A Household must have at least one Member.
- HouseholdSafetyRules are always derived from Member `dietary_constraints` — never set directly.
- All domain events carry `household_id`.

### Pantry
The current food inventory of a Household.

**Entities within aggregate:** PantryItem

**Invariants:**
- PantryItem quantity is never negative.
- Quantity changes always produce a domain event — no silent mutations.
- Deletions are modelled as `PantryItemThrownAway` or `PantryItemExpired` events, not hard deletes.

### ShoppingList
An active or completed shopping list for a Household.

**Entities within aggregate:** ShoppingItem

**Invariants:**
- Items removed by user produce `ShoppingItemRemoved` (reversible). Hard deletes are not permitted.
- A ShoppingList may be AI-generated, user-created, or expert-suggested.

### MealPlan
A structured plan of meals for a Household over a period.

**Entities within aggregate:** MealPlanItem

**Invariants:**
- All recipes in a MealPlan must pass Allergy Guard before being shown to the user.
- Expert-suggested meal plans require explicit user approval before entering the MealPlan.

### Budget
Grocery spend tracking for a Household over a period.

**Invariants:**
- Budget spend is recorded by events from the Receipt context, not set directly.
- Reversals (e.g., duplicate receipt) produce `BudgetSpendReversed` events.

### Provider *(Expert Marketplace context)*
An organisation or individual that Expert accounts belong to.

**Entities within aggregate:** ProviderMember, ExpertProfile, ServiceOffering

**Invariants:**
- An ExpertProfile must belong to a Provider.
- An Expert can only access household data covered by an active ConsentGrant.

### ExpertPlan *(Expert Marketplace context)*
A structured plan created by an Expert for a Member.

**Entities within aggregate:** ExpertRecommendation

**Invariants:**
- Every ExpertRecommendation must pass Allergy Guard before the user sees it.
- No ExpertRecommendation may change household state without `user_approval_status: approved`.

---

## Data Model

Tables are organised by bounded context. The `domain_events` table is cross-cutting.

### Cross-Cutting: Events

```text
domain_events
  event_id          uuid, primary key
  event_type        string             e.g. "ItemConsumed"
  domain            string             e.g. "pantry"
  household_id      uuid, indexed
  actor_type        string             "user" | "system" | "ai" | "expert"
  actor_id          uuid
  source_type       string             "cook_mode" | "receipt_scan" | "manual" | ...
  entity_type       string             e.g. "pantry_item"
  entity_id         uuid
  occurred_at       timestamptz
  payload           jsonb
  correlation_id    uuid               groups events from one user action
  causation_id      uuid               which event caused this event
  reversal_of       uuid, nullable     links reversal/correction to original event
  learning_impact   string             "learning" | "no_learning" | "waste_signal" | ...
  privacy_level     string             "household" | "member_only" | "expert_scoped"
```

### Household Context

```text
households
  id                uuid
  name              string

users
  id                uuid
  name              string
  email             string

household_members
  id                uuid
  household_id      uuid → households.id
  user_id           uuid → users.id
  role              string    "admin" | "member"
  included_in_meal_planning   boolean
  allergy_visibility          string  "household" | "private"
  goal_visibility             string  "household" | "private"
```

### Profile & Safety Context

```text
dietary_constraints
  id                    uuid
  user_id               uuid → users.id
  type                  string    "allergy" | "intolerance" | "preference" | "medical"
  ingredient_or_category  string
  severity              string    "critical" | "moderate" | "mild"
  enforcement_level     string    "block" | "warn" | "flag"
  notes                 string, nullable

household_safety_rules
  id                    uuid
  household_id          uuid → households.id
  rule_type             string    "block" | "warn"
  ingredient_or_category  string
  enforcement_level     string
  derived_from_user_id  uuid → users.id

user_goals
  id                uuid
  user_id           uuid → users.id
  goal_type         string    "muscle_gain" | "weight_reduction" | "maintenance" | "healthier_eating" | "medical_nutrition"
  target_direction  string    "increase" | "decrease" | "maintain"
  intensity         string    "aggressive" | "moderate" | "conservative"
  status            string    "active" | "paused" | "completed"
  start_date        date
  review_cadence    string    "weekly" | "monthly"

nutrition_preferences
  id                        uuid
  user_id                   uuid → users.id
  protein_priority          string
  calorie_awareness_level   string
  preferred_meal_types      string[]
  avoided_foods             string[]

meal_audience_goals
  id                uuid
  meal_plan_id      uuid → meal_plans.id
  user_id           uuid → users.id
  goal_id           uuid → user_goals.id
  portion_strategy  string
  add_on_strategy   string
  exclusion_strategy  string
```

### Pantry Context

```text
pantry_items
  id            uuid
  household_id  uuid → households.id
  name          string
  category      string
  quantity      numeric
  unit          string
  expiry_date   date, nullable
  added_at      timestamptz
  source        string    "receipt_scan" | "manual" | "expert_plan"
```

### Shopping Context

```text
shopping_lists
  id            uuid
  household_id  uuid → households.id
  created_at    timestamptz
  status        string    "active" | "completed" | "archived"
  source        string    "ai_generated" | "user_created" | "expert_suggested"

shopping_items
  id                uuid
  shopping_list_id  uuid → shopping_lists.id
  name              string
  quantity          numeric, nullable
  unit              string, nullable
  status            string    "pending" | "purchased" | "removed"
  added_by          string    "user" | "ai" | "expert"
```

### Planning & Recipe Context

```text
recipes
  id            uuid
  name          string
  source        string    "system" | "expert" | "user"
  ingredients   jsonb
  instructions  jsonb
  cook_time_minutes  integer
  servings      integer

meal_plans
  id            uuid
  household_id  uuid → households.id
  week_start    date
  status        string    "draft" | "active" | "completed"

meal_plan_items
  id            uuid
  meal_plan_id  uuid → meal_plans.id
  recipe_id     uuid → recipes.id
  day           string
  meal_type     string    "breakfast" | "lunch" | "dinner" | "snack"
```

### Budget Context

```text
budgets
  id            uuid
  household_id  uuid → households.id
  period_type   string    "weekly" | "monthly"
  period_start  date
  amount        numeric
  currency      string

budget_entries
  id            uuid
  budget_id     uuid → budgets.id
  amount        numeric
  category      string
  recorded_at   timestamptz
  source_event  uuid → domain_events.event_id
```

### Expert Marketplace Context

```text
providers
  id                  uuid
  provider_type       string    "individual" | "organization"
  name                string
  legal_entity_type   string
  verification_status string    "pending" | "verified" | "suspended"

provider_members
  id            uuid
  provider_id   uuid → providers.id
  user_id       uuid → users.id
  role          string    "owner" | "expert" | "admin"
  status        string    "active" | "inactive"

expert_profiles
  id                    uuid
  provider_member_id    uuid → provider_members.id
  expert_type           string    "nutritionist" | "dietitian" | "personal_trainer" | "yoga_instructor" | "wellness_coach"
  specialties           string[]
  credentials           string
  bio                   string
  verification_status   string

service_offerings
  id                    uuid
  expert_profile_id     uuid → expert_profiles.id
  title                 string
  category              string
  duration              string
  price                 numeric
  includes_chat         boolean
  includes_video        boolean
  includes_plan_review  boolean

client_provider_relationships
  id                    uuid
  household_id          uuid → households.id
  user_id               uuid → users.id
  expert_profile_id     uuid → expert_profiles.id
  service_offering_id   uuid → service_offerings.id
  status                string    "active" | "paused" | "ended"

consent_grants
  id                uuid
  user_id           uuid → users.id
  household_id      uuid → households.id
  expert_profile_id uuid → expert_profiles.id
  data_scope        string[]    e.g. ["pantry", "goals", "timeline"]
  expires_at        timestamptz

expert_plans
  id                uuid
  expert_profile_id uuid → expert_profiles.id
  user_id           uuid → users.id
  household_id      uuid → households.id
  plan_type         string    "nutrition" | "fitness" | "combined"
  status            string    "draft" | "active" | "completed"

expert_recommendations
  id                    uuid
  expert_plan_id        uuid → expert_plans.id
  recommendation_type   string    "meal" | "recipe" | "shopping_item" | "substitution"
  payload               jsonb
  safety_status         string    "pending_check" | "passed" | "blocked"
  user_approval_status  string    "pending" | "approved" | "rejected"

chat_threads
  id                uuid
  relationship_id   uuid → client_provider_relationships.id
  thread_type       string    "general" | "plan_review" | "check_in"
```

---

## Domain Events

Events are organised by bounded context. All events share the standard envelope defined in the next section.

### Household
- `HouseholdCreated`
- `MemberAdded`
- `MemberRoleChanged`
- `MemberRemovedFromHousehold`

### Profile & Safety
- `AllergyAdded`
- `AllergyUpdated`
- `AllergyRemoved`
- `GoalSet`
- `GoalUpdated`
- `GoalDeactivated`
- `HouseholdSafetyRulesDerived`

### Receipt
- `ReceiptScanned`
- `ReceiptOcrCompleted`
- `ReceiptItemsConfirmed`
- `PantryItemsAddedFromReceipt`
- `BudgetSpendRecorded`
- `ShoppingItemsMatched`
- `ReceiptMarkedDuplicate`
- `PantryReceiptAdditionsReversed`
- `BudgetSpendReversed`
- `ShoppingMatchesUnlinked`

### Pantry
- `ItemAddedToPantry`
- `ItemConsumed`
- `PantryItemThrownAway`
- `PantryItemExpired`
- `PantryItemQuantityCorrected`
- `PantryItemConsumptionCorrected`

### Shopping
- `ShoppingListCreated`
- `ShoppingItemAdded`
- `ShoppingItemRemoved`
- `ShoppingItemPurchased`
- `ShoppingItemRestoredAfterUndo`

### Planning & Recipe
- `MealPlanned`
- `RecipeRecommended`
- `RecipeAccepted`
- `RecipeRejected`
- `MealPlanCreated`
- `MealPlanUpdated`

### Cook Mode
- `CookingSessionStarted`
- `CookingStepCompleted`
- `MealCooked`
- `PantryDeductedFromCooking`
- `CookingDeductionReversed`

### Budget
- `BudgetPeriodCreated`
- `BudgetSpendRecorded` *(also emitted from Receipt context)*
- `BudgetSpendReversed`
- `BudgetAmountUpdated`

### Expert Marketplace
- `ExpertRelationshipCreated`
- `ExpertRelationshipEnded`
- `ConsentGranted`
- `ConsentRevoked`
- `ExpertPlanCreated`
- `ExpertRecommendationCreated`
- `ExpertRecommendationSafetyChecked`
- `ExpertRecommendationApproved`
- `ExpertRecommendationRejected`

### Correction & Activity
- `CorrectionEventCreated`
- `ReversalCompleted`
- `HouseholdTimelineGroupCreated`

---

## Standard Event Envelope

Every domain event shares this envelope. The `payload` field carries event-specific data.

```text
event_id            uuid            globally unique
event_type          string          PascalCase, e.g. "ItemConsumed"
domain              string          bounded context name, e.g. "pantry"
household_id        uuid            always present
actor_type          string          "user" | "system" | "ai" | "expert"
actor_id            uuid            user_id, system process id, or expert_profile_id
source_type         string          "cook_mode" | "receipt_scan" | "manual" | "ai_recommendation" | "expert_plan"
entity_type         string          the aggregate type affected, e.g. "pantry_item"
entity_id           uuid            the affected entity
occurred_at         timestamptz     when the event happened (not when it was stored)
payload             jsonb           event-specific data
correlation_id      uuid            groups all events from one user action
causation_id        uuid            the event_id that caused this event (nullable)
reversal_of         uuid            the event_id being reversed or corrected (nullable)
learning_impact     string          "learning" | "no_learning" | "waste_signal" | "correction_signal"
privacy_level       string          "household" | "member_only" | "expert_scoped"
```

**Key envelope fields:**

- `correlation_id` — one receipt scan produces multiple events (`ReceiptScanned`, `PantryItemsAdded`, `BudgetSpendRecorded`). All share the same `correlation_id`.
- `causation_id` — shows which event caused another. `PantryItemsAddedFromReceipt` is caused by `ReceiptItemsConfirmed`.
- `reversal_of` — links a reversal or correction event to the event it reverses. Never overwrite the original.
- `learning_impact` — tells the AI whether this event should influence future recommendations. Waste and corrections carry different signals than consumption.
- `privacy_level` — controls visibility: member-only constraints are not visible to other household members unless the member sets `allergy_visibility: household`.

---

## Business Invariants

These rules must hold at all times. They are not implementation details — they are domain facts. Violations require an ADR or an explicit exception record.

1. **Every meaningful household action produces a domain event.** No silent state changes. No soft deletes on domain data.

2. **Allergy Guard runs before any recommendation or expert suggestion reaches the user.** The check is deterministic and cannot be bypassed by AI output or expert instructions.

3. **Corrections and reversals are additional events, never mutations.** The original event is preserved permanently.

4. **Commands express user intent. Events express system fact.** The UI presents commands ("Remove item"). The ledger records events (`ShoppingItemRemoved`).

5. **`household_safety_rules` are derived from `dietary_constraints`, never set independently.** The derivation runs whenever a member's constraints change.

6. **User goals apply after safety constraints.** Safety always wins. A goal cannot override an allergy block.

7. **Expert recommendations require user approval before any household state change.** An `ExpertRecommendationApproved` event must exist before the recommendation affects pantry, shopping, or meal plan state.

8. **An Expert can only access data covered by an active, unexpired `ConsentGrant`.** Consent is scoped (e.g., pantry only) and time-bounded.

9. **The Household Timeline is a read model, not a primary table.** It is always reconstructable from the `domain_events` table.

10. **Staleness must always be visible.** Cached, offline, or stale data must carry a visible indicator. Implicit staleness is a trust failure.
