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
| **Person** | A human being in the KitchenOS domain. Owns stable, global facts about themselves: age group, health profile, dietary restrictions, and goals. A Person exists independently of any Household. The same Person can be a member of multiple Households. Person is a domain concept — not an auth concept, not an AI concept. |
| **HouseholdMembership** | The explicit relationship between a Person and a Household. Owns context-specific properties: role, permissions, joined date, status, and optional display nickname. A single Person can have multiple HouseholdMemberships. Membership is a first-class domain concept, not a join table. |
| **PersonProfile** | The stable, explicitly-stated facts about a Person: age group, dietary restrictions, allergies, nutrition goals, and health context. These are business facts — not AI-learned beliefs. Never conflated with the Household Intelligence Model. |
| **Pantry** | The current known food inventory of a Household. Always a projection of pantry domain events. |
| **PantryItem** | A single food item in the Pantry with quantity, unit, and optional expiry. |
| **ShoppingList** | An ordered collection of items the Household intends to purchase. |
| **ShoppingItem** | A single item on a ShoppingList. Has a status: pending, purchased, or removed. |
| **Recipe** | A set of ingredients and instructions for preparing a meal. May be system-provided or expert-provided. |
| **WeeklyMealPlan** | The household's committed meal strategy for a week. Contains a collection of MealPlans, one per meal slot. Accepted in a single user action ("Accept Week"). No pantry change on acceptance — only MealSessions produce pantry events. The weekly plan is a living document: it adapts as pantry, leftovers, and schedules change. |
| **MealRecommendation** | An ephemeral AI output: a suggested meal with predicted participants, portions, and confidence score. Creates no commitment. No pantry change. Discarded if rejected or ignored. The Planning Layer. |
| **MealPlan** | A committed intention: a single meal the household plans to cook. Always belongs to a WeeklyMealPlan or created standalone. Contains confirmed participants and planned portions. Creates no pantry change — that only happens when a MealSession completes. The Intention Layer. |
| **MealSession** | Reality: a cooking and eating event that actually happened. Owned by confirmed participants and actual portions. The only object that produces pantry deduction events. The Execution Layer. |
| **Household Schedule Model** | An AI intelligence model (not a domain concept) representing the household's learned weekly routine: who eats on which nights, typical takeout nights, when guests visit, kids' activities, etc. Feeds the recommendation engine when generating weekly plans. Lives in the Intelligence Layer, not the Domain Model. |
| **Budget** | A spending target for grocery and food purchases. Tracked per period (weekly or monthly). |
| **Household Decision Engine** | The AI coordination layer that turns household context into safe, trusted food decisions. Never acts autonomously. Always produces recommendations for user approval. |
| **Allergy Guard** | The deterministic safety check that runs on every recommendation, substitution, and expert suggestion against household safety rules. Never bypassed. |
| **Household Timeline** | The user-facing, human-readable event log of the Household. A read model over the domain event stream. Distinct from the audit log. |
| **Domain Event** | An immutable record of something meaningful that happened in the Household. Written to the `domain_events` table. Never deleted. Every domain event belongs to exactly one Household — `household_id` is required on every event without exception. |
| **Household Context** | An application-layer concept (not a domain concept) representing the active household and member for the current session. Drives routing, permissions, UI state, and notifications. Does not persist when the app is closed. Defined in the Technical Architecture, not here. |
| **Command** | A user or system request to change household state. Commands produce events. The UI shows commands; the ledger records events. |
| **Reversal Event** | A domain event that reverses the effects of a prior event. Does not delete the original event. |
| **Correction Event** | A domain event that records a change in interpretation of a prior event (e.g., consumption re-classified as waste). |
| **Household Safety Rules** | Household-level allergy and dietary rules derived from individual member `dietary_constraints`. Never set independently. |
| **Expert** | A verified nutritionist, dietitian, fitness coach, or wellness practitioner who can access permissioned household data and provide plans. |
| **Provider** | The organisation or individual entity that Expert accounts belong to. May be an independent expert or a clinic, gym, or wellness company. |
| **Expert Plan** | A structured nutrition or fitness plan created by an Expert for a specific Member. Requires user approval before affecting household state. |
| **Expert Recommendation** | A specific suggestion within an Expert Plan (a meal, recipe, substitution, or shopping item). Must pass Allergy Guard and requires user approval. |
| **Consent Grant** | Explicit, scoped, time-bounded permission a Member gives an Expert to access specific household data. |
| **Cook Mode** | A UI capability that facilitates a Meal Session. Guides users step-by-step through a recipe. Cook Mode does not directly update the Pantry — it drives a Meal Session to completion, and the completed Meal Session produces the pantry update events. |
| **MealSession** | A first-class domain aggregate representing a real-world cooking and eating event. Owns participants, portions, leftovers, and the pantry changes that result from confirmed cooking completion. The source of truth for all pantry deductions from food consumption. |
| **ShoppingTrip** | A real-world purchasing event, initiated by a Shopping List and completed by receipt scan or manual confirmation. The source of truth for all pantry additions from purchasing. |
| **Household Activity Lifecycle** | An architectural pattern (not a domain entity) describing the shared lifecycle all household activities follow: Planned → Started → In Progress → Completed → Domain Events produced. Applies to MealSession, ShoppingTrip, PantryCorrection, and WasteEvent. |
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
| **Household** | Household, HouseholdMembership, roles, permissions, shared settings | `household.*` |
| **Person** | Person, PersonProfile, age group, health profile | `person.*` |
| **Profile & Safety** | Dietary restrictions, allergies, goals, household safety rules | `profile.*`, `safety.*` |
| **Receipt** | Receipt scanning, OCR, item extraction, duplicate detection | `receipt.*` |
| **Pantry** | Pantry inventory, quantities, expiry, consumption, waste | `pantry.*` |
| **Shopping** | Shopping lists, items, purchase status | `shopping.*` |
| **Planning & Recipe** | Recipes, WeeklyMealPlans, MealPlans (intentions), MealRecommendations (ephemeral), substitutions | `planning.*` |
| **Cook Mode** | UI session state for step-by-step cooking guidance | `cook.*` |
| **Meal Session** | MealSession aggregate, participants, portions, leftovers, consumption events | `meal.*` |
| **Budget** | Grocery spend tracking, budget periods, reversals | `budget.*` |
| **Expert Marketplace** | Providers, experts, plans, recommendations, consent | `marketplace.*` |
| **Correction & Activity** | Reversal events, undo flows, Household Timeline grouping | `correction.*` |
| **Support** *(future)* | Support tickets, conversations, resolutions, escalations — customer-facing and expert-facing | `support.*` |

---

## Aggregate Roots

An aggregate root is the authoritative object for a cluster of related entities. All state changes within the aggregate go through the root.

### Household
The primary aggregate. Every other aggregate belongs to or references a Household.

**Entities within aggregate:** HouseholdMembership, HouseholdSafetyRules

**Invariants:**
- A Household is auto-created at account confirmation. The user never creates one manually.
- A Person record is created when an Identity is first confirmed. A default HouseholdMembership is created alongside the auto-created Household. There is no state where a confirmed Identity exists without a Person, a Household, and at least one HouseholdMembership.
- A single person living alone is a valid household of one. The model handles it identically to multi-member households.
- If onboarding is abandoned before completion, the household and membership records still exist. The system operates in a low-confidence state until more context is provided.
- A Household must always have at least one HouseholdMembership with `role: admin`.
- HouseholdSafetyRules are always derived from Member `dietary_constraints` — never set directly.
- **Every domain event must carry `household_id`. This is a non-negotiable domain rule. An event without a `household_id` is a bug.**

> **Design note — Household trends toward a Boundary, not a thick Aggregate.**
> If you strip everything to its own aggregate (Pantry, MealPlan, ShoppingTrip, Budget), Household owns almost nothing:
> `id, display_name, timezone, locale, created_at, status`. It acts as a namespace — the shared `household_id` on every event — rather than as a stateful aggregate.
> This is already the correct design. The label "Aggregate Root" is used here for Version 1 clarity.
> In a fully event-sourced system, Household should be modelled as a **Boundary** with its own thin event stream (created, renamed, archived) and all real state owned by the aggregates inside it.
> Formalize this in Version 2 when event-sourcing infrastructure is in place.

### Pantry
The current food inventory of a Household.

**Entities within aggregate:** PantryItem

**Invariants:**
- PantryItem quantity is never negative.
- Quantity changes always produce a domain event — no silent mutations.
- Deletions are modelled as `PantryItemThrownAway` or `PantryItemExpired` events, not hard deletes.
- **Pantry state is derived exclusively from confirmed household activities.** The pantry is never updated by a recommendation, a recipe, or a prediction. Only completed ShoppingTrips, completed MealSessions, confirmed WasteEvents, and confirmed PantryCorrections may produce pantry update events. This is a non-negotiable invariant.

### Person
A human being in the KitchenOS domain. Global and portable across households.

**Entities within aggregate:** PersonProfile

**Invariants:**
- A Person is created when an Identity is first confirmed. It always exists independently of any Household.
- `PersonProfile` owns all stable facts about a Person: age group, dietary restrictions, allergies, goals, and any health measurements required by an active goal (e.g. height, weight). There is no separate `HealthProfile` — a profile-inside-a-profile adds indirection without adding clarity. All stable Person facts live flat on `PersonProfile`.
- Learned preferences (cuisine affinity, shopping habits, meal acceptance rates) are NOT part of Person. They belong to the Household Intelligence Model.
- A Person's allergies and goals travel with them to every Household they join. HouseholdMembership does not override PersonProfile facts.

### WeeklyMealPlan
The household's committed meal strategy for a week. Contains a set of MealPlans.

**Entities within aggregate:** MealPlan (one per meal slot)

**Invariants:**
- A WeeklyMealPlan is accepted in a single user action. All constituent MealPlans are created atomically.
- Accepting a WeeklyMealPlan does NOT update pantry, shopping list, or budget. Acceptance is commitment to intention, not execution.
- A WeeklyMealPlan is a living document. Individual MealPlans within it may be swapped, cancelled, or replaced as the week unfolds — without invalidating the whole plan.
- The AI may proactively suggest swaps mid-week based on pantry changes, expiry risk, schedule signals, or leftover availability. These are suggestions — the user confirms each swap.
- One WeeklyMealPlan per household per week. A household may have at most one active WeeklyMealPlan.

> **Design note — WeeklyMealPlan trends toward a Planning Horizon, not a thick Aggregate.**
> The week is a container for MealPlans, not an aggregate with its own business rules.
> In a future version consider modelling it as a `planning_horizon` (week_start + household_id) with MealPlans referencing it by FK — rather than a parent aggregate that owns child aggregates.
> The distinction: a Planning Horizon has no invariants of its own. It is simply a time-scoped grouping.
> Leave as an Aggregate Root in Version 1 for clarity. Revisit when the planning engine matures.

### MealRecommendation
An ephemeral AI output. The Planning Layer.

**Invariants:**
- A MealRecommendation commits nothing. It carries no household state.
- It holds predicted participants and a confidence score — these are AI beliefs, not confirmed facts.
- A MealRecommendation is accepted (→ creates a MealPlan), rejected (→ discarded), or expires (→ discarded). No other outcomes.
- Accepting a MealRecommendation does NOT update the pantry, shopping list, or budget.

### MealPlan
A committed intention for a single meal. The Intention Layer.

**Invariants:**
- A MealPlan belongs to a WeeklyMealPlan or is created standalone.
- It holds confirmed participants and planned portions — these are domain facts, not AI beliefs.
- A MealPlan does NOT update the pantry. Intention ≠ execution.
- A MealPlan transitions to a MealSession when the user starts cooking. If cooking never happens, the MealPlan expires without affecting any state.
- One MealPlan produces at most one MealSession.
- A MealPlan within a WeeklyMealPlan can be swapped or cancelled independently without affecting other MealPlans in the week.

### MealSession
Reality: a cooking and eating event that actually happened. The Execution Layer.

**Entities within aggregate:** MealSessionParticipant, MealSessionLeftover

**Invariants:**
- A MealSession is created when the user commits to cooking — tapping "Start Cooking" or equivalent.
- Confirmed participants are pre-filled from the MealPlan (or household defaults at high confidence). The user confirms or adjusts before cooking starts.
- Participants are identified by `person_id` — the Recommendation Engine loads each participant's PersonProfile to compute combined constraints.
- Pantry deductions are produced only when a MealSession reaches `status: completed` and the user confirms. Never on recommendation, plan creation, or cooking start.
- Leftovers are first-class: prepared portions minus consumed portions equals leftovers, which are recorded and optionally returned to the pantry as a new PantryItem.
- A MealSession can exist without a prior MealPlan (manual logging) and without Cook Mode (logged after the fact).
- Cook Mode is one UI path into a MealSession. It does not own pantry state.

### ShoppingList
An active or completed shopping list for a Household.

**Entities within aggregate:** ShoppingItem

**Invariants:**
- Items removed by user produce `ShoppingItemRemoved` (reversible). Hard deletes are not permitted.
- A ShoppingList may be AI-generated, user-created, or expert-suggested.

### ShoppingTrip
A real-world purchasing event. The Execution Layer for shopping — the exact parallel of `MealSession` for cooking.

**Entities within aggregate:** ShoppingTripItem, Receipt

**Invariants:**
- A ShoppingTrip is initiated from a ShoppingList (or manually). It does not create a ShoppingList retroactively.
- A ShoppingTrip is completed by receipt scan or manual confirmation. Both paths produce the same `PantryItemsAddedFromReceipt` events.
- **Receipt is evidence, not the reality.** The ShoppingTrip is the real-world event. The Receipt is how KitchenOS learns what was purchased. A ShoppingTrip can be completed without a receipt (manual confirmation).
- Pantry additions are produced only when a ShoppingTrip is `status: confirmed`. Never on ShoppingList creation or receipt scan alone.
- Duplicate receipt detection runs before confirmation. A duplicate receipt produces `ReceiptMarkedDuplicate` and blocks pantry additions.

> The shopping lifecycle mirrors cooking:
> ```
> ShoppingList (intention)  ←→  MealPlan (intention)
>         ↓                              ↓
> ShoppingTrip (reality)    ←→  MealSession (reality)
>         ↓                              ↓
> Pantry ADDED              ←→  Pantry DEDUCTED
> ```

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

> **Design note — Expert Marketplace will likely split into multiple aggregates.**
> As this context grows, `Provider`, `Expert`, `ConsentGrant`, `ExpertPlan`, and `ClientProviderRelationship` will each acquire enough invariants and event streams to justify being independent aggregate roots.
> For Version 1, grouping under Provider and ExpertPlan is sufficient.
> Before building this context, revisit whether these are truly one aggregate or five.

---

## Actor Model

KitchenOS interacts with multiple distinct actor types. Each actor has its own interface, permissions, and relationship to household data.

### Version 1 Actors

| Actor | Interface | Relationship to household |
|---|---|---|
| **Customer** | KitchenOS mobile app | Member of one or more households; all data scoped to their household |
| **Expert** | Expert Portal *(future)* | Accesses household data only within an active, scoped `ConsentGrant` |
| **AI** | Internal APIs | No direct interface; acts on behalf of household via recommendations |

### Future Actors (post-MVP)

| Actor | Interface | Role |
|---|---|---|
| **Support Agent** | Support Console | Assists customers and experts; reads limited, scoped data for issue resolution |
| **Expert Operations** | Internal Admin Portal | Verifies expert credentials, manages onboarding, audits consent, monitors marketplace quality |
| **Operations Engineer** | Platform Operations Dashboard | Keeps the platform running; no access to household data |
| **Product Administrator** | Internal Admin Portal | Manages system-level configuration, feature flags, platform settings |
| **AI Agent** | Internal APIs | Autonomous agents acting on household data; always within user-granted boundaries |

> **Design note — Support as a future bounded context.**
> Customer Support is a **business capability**, not a platform capability. It owns domain objects with their own lifecycle:
> `SupportTicket`, `Conversation`, `SupportAgent`, `Escalation`, `Resolution`.
>
> Domain events it will produce:
> `SupportTicketCreated`, `SupportAgentAssigned`, `CustomerResponded`, `SupportAgentResponded`, `IssueResolved`, `IssueClosed`
>
> This is not part of Technical Architecture (auth/authz), nor Engineering Handbook (on-call/runbooks).
> It is a product context that will grow in importance as the marketplace matures — particularly Expert Operations:
> verifying credentials, handling disputes, auditing consent compliance, and monitoring marketplace quality.
>
> Model it as a bounded context in Version 2. Reserve `support.*` event namespace now.
> See `Knowledge/95_Customer_Expert_Operations/` for the operational workflows that sit above this domain context.

---

## Privacy-by-Design Principle

> **Collect only the information required to improve the user's experience.**

This principle governs every field in this data model. Before adding a column, the team must answer: what recommendation, safety check, or household decision does this field enable? If there is no clear answer, the field does not belong here.

Key decisions reflected in the data model:

- **Identity is isolated from intelligence.** The `identities` table (auth layer) is physically separate from the `household_members` table (intelligence layer). The recommendation engine operates on `member_id` — never on names or emails.
- **Names are not stored internally.** A `display_name` field is optional and exists only for UI presentation. It is never used in recommendations, safety checks, or AI reasoning.
- **Age range, not exact age.** The system stores `age_group` (Adult, Child, Teen) and an optional `age_range` (e.g. 25–35) where needed for nutrition estimation. Exact birth dates are not required.
- **Sensitive data is scoped.** Height, weight, and medical conditions are stored only on the member who provides them, only when an active goal requires them, and are never visible to other household members by default.

See `Knowledge/10_Product_Vision.md`, Sections 8.10 and 8.11. See `ADR-009` for the full architectural decision.

---

## Data Model

Tables are organised by bounded context. The `domain_events` table is cross-cutting.

### Cross-Cutting: Events

```text
domain_events
  event_id          uuid, primary key
  event_type        string             e.g. "ItemConsumed"
  event_version     integer            starts at 1; increment on schema change to payload
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

### Person and Household Context

```text
identities                         ← auth layer only; no domain or intelligence data lives here
  id                uuid
  email             string         the only PII stored; required for login and account recovery
  auth_provider     string         "google" | "apple" | "email"
  created_at        timestamptz

persons                            ← domain layer: stable facts about a human being
  id                uuid           person_id — used throughout profile, safety, meal session
  identity_id       uuid → identities.id   the only bridge to auth layer; never read by AI
  age_group         string         "adult" | "teen" | "child" | "infant"
  age_range         string, nullable   "18-24" | "25-34" | "35-44" | "45-54" | "55+"
  created_at        timestamptz

households
  id                uuid
  display_name      string, nullable   optional household name for UI only
  created_at        timestamptz

household_memberships              ← context layer: relationship between a Person and a Household
  id                uuid
  person_id         uuid → persons.id
  household_id      uuid → households.id
  role              string         "admin" | "member" | "caregiver" | "guest"
  status            string         "active" | "invited" | "suspended"
  joined_at         timestamptz
  display_name      string, nullable   optional nickname for UI display only; never used in AI
  included_in_meal_planning   boolean
  allergy_visibility          string  "household" | "private"
  goal_visibility             string  "household" | "private"
  notification_preferences    jsonb, nullable
```

**How the four layers connect:**

```text
identities
  id ──────────────────────────────────┐
  email                                │ identity_id (auth bridge — crossed once at login only)
  auth_provider                        │
                                       ↓
                                    persons
                                      id (person_id) ←── used by profile, safety, meal session, AI
                                      identity_id ──────── points back to identities; never read by AI
                                      age_group
                                      age_range
                                          │
                              ┌───────────┴────────────┐
                              │ person_id               │ person_id
                              ↓                         ↓
                  household_memberships          dietary_constraints
                    person_id                    user_goals
                    household_id ──┐             nutrition_preferences
                    role           │
                    status         ↓
                               households
                                 id
                                 display_name
```

Key points:

- `identities` → `persons`: crossed once at login to resolve `person_id`. Never crossed again by AI or intelligence layer.
- `persons` → `household_memberships`: one Person can have multiple memberships (one per household).
- `persons` → profile tables: dietary restrictions, goals, and preferences are owned by the Person, not the membership. They are global and travel with the person to every household.
- `household_memberships` → `households`: context only — role, permissions, notification prefs. No profile data.
- When a user logs in: `identity_id` → `person_id` → memberships resolved → Household Context assembled. After that, only `person_id` and `household_id` travel through the system.

> `identities` and `persons` must live in separate schemas. The `identity_id` bridge on `persons` must never be read by the intelligence layer, the Household Intelligence Model, or the Collective Intelligence pipeline. The recommendation engine receives only `person_id` and `household_id`.

### Profile & Safety Context

```text
dietary_constraints
  id                    uuid
  person_id             uuid → persons.id
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
  derived_from_person_id  uuid → persons.id

user_goals
  id                uuid
  person_id         uuid → persons.id
  goal_type         string    "muscle_gain" | "weight_reduction" | "maintenance" | "healthier_eating" | "medical_nutrition"
  target_direction  string    "increase" | "decrease" | "maintain"
  intensity         string    "aggressive" | "moderate" | "conservative"
  status            string    "active" | "paused" | "completed"
  start_date        date
  review_cadence    string    "weekly" | "monthly"

nutrition_preferences
  id                        uuid
  person_id                 uuid → persons.id
  protein_priority          string
  calorie_awareness_level   string
  preferred_meal_types      string[]
  avoided_foods             string[]

meal_audience_goals
  id                uuid
  meal_plan_id      uuid → meal_plans.id
  person_id         uuid → persons.id
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
  source        string    "receipt_scan" | "manual" | "expert_plan" | "meal_session_leftover"
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

shopping_trips                     ← real-world purchasing event; parallel to meal_sessions
  id                uuid
  household_id      uuid → households.id
  shopping_list_id  uuid → shopping_lists.id, nullable
  status            string    "in_progress" | "confirmed" | "cancelled"
  started_at        timestamptz
  confirmed_at      timestamptz, nullable
  store_name        string, nullable

receipts                           ← evidence of a shopping trip; not the trip itself
  id                uuid
  household_id      uuid → households.id
  shopping_trip_id  uuid → shopping_trips.id, nullable
  scanned_at        timestamptz
  raw_text          text, nullable
  total_amount      numeric, nullable
  currency          string, nullable
  status            string    "processing" | "confirmed" | "duplicate" | "rejected"

> Receipt is how KitchenOS learns what was purchased.
> ShoppingTrip is what actually happened.
> Pantry additions are produced by a confirmed ShoppingTrip — not by the receipt scan itself.
```

### Meal Session Context

```text
meal_sessions
  id                    uuid
  household_id          uuid → households.id
  recipe_id             uuid → recipes.id, nullable
  initiated_by          uuid → household_members.id
  status                string    "planned" | "started" | "in_progress" | "completed" | "abandoned"
  planned_portions      integer
  actual_portions       integer, nullable
  leftovers_portions    integer, nullable    default 0
  started_at            timestamptz, nullable
  completed_at          timestamptz, nullable
  cook_mode_used        boolean              was Cook Mode UI used?
  notes                 string, nullable

meal_session_participants
  id                    uuid
  meal_session_id       uuid → meal_sessions.id
  person_id             uuid → persons.id     PersonProfile loaded at recommendation time
  portions_consumed     numeric              actual portions this person ate

meal_session_leftovers
  id                    uuid
  meal_session_id       uuid → meal_sessions.id
  description           string               e.g. "Chicken pasta"
  quantity              numeric
  unit                  string
  stored_as_pantry_item boolean             did leftovers go back into pantry?
  pantry_item_id        uuid → pantry_items.id, nullable
```

> Pantry deduction events (`PantryItemConsumed`) are emitted by the MealSession aggregate on completion — never by the recipe, recommendation engine, or Cook Mode UI directly.

### Planning & Recipe Context

```text
recipes
  id                 uuid
  name               string
  source             string    "system" | "expert" | "user"
  ingredients        jsonb
  instructions       jsonb
  cook_time_minutes  integer
  servings           integer   default serving size for reference only

meal_recommendations               ← ephemeral AI output; no household state committed
  id                    uuid
  household_id          uuid → households.id
  recipe_id             uuid → recipes.id, nullable
  predicted_persons     uuid[]    person_ids predicted to participate
  predicted_portions    integer
  confidence_score      numeric   0.0 – 1.0
  meal_type             string    "breakfast" | "lunch" | "dinner" | "snack"
  recommended_for_date  date
  status                string    "pending" | "accepted" | "rejected" | "expired"
  generated_at          timestamptz
  expires_at            timestamptz

weekly_meal_plans                  ← the household's committed weekly strategy; no pantry change
  id                uuid
  household_id      uuid → households.id
  week_start        date             Monday of the planned week
  status            string           "draft" | "accepted" | "in_progress" | "completed" | "abandoned"
  generated_by      string           "ai" | "user"
  accepted_at       timestamptz, nullable
  notes             string, nullable

meal_plans                         ← single meal intention; no pantry change
  id                uuid
  household_id      uuid → households.id
  weekly_meal_plan_id  uuid → weekly_meal_plans.id, nullable   null if standalone
  recipe_id         uuid → recipes.id, nullable
  recommendation_id uuid → meal_recommendations.id, nullable   origin if AI-suggested
  planned_for_date  date
  meal_type         string    "breakfast" | "lunch" | "dinner" | "snack"
  planned_persons   uuid[]    confirmed person_ids
  planned_portions  integer
  status            string    "planned" | "in_progress" | "completed" | "cancelled" | "swapped"

> A WeeklyMealPlan is accepted in one tap. Each MealPlan within it can be swapped individually.
> A MealPlan transitions to a MealSession on "Start Cooking".
> Neither a WeeklyMealPlan nor a MealPlan updates the pantry — only a completed MealSession does.
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
  person_id             uuid → persons.id
  expert_profile_id     uuid → expert_profiles.id
  service_offering_id   uuid → service_offerings.id
  status                string    "active" | "paused" | "ended"

consent_grants
  id                uuid
  person_id         uuid → persons.id
  household_id      uuid → households.id
  expert_profile_id uuid → expert_profiles.id
  data_scope        string[]    e.g. ["pantry", "goals", "timeline"]
  expires_at        timestamptz

expert_plans
  id                uuid
  expert_profile_id uuid → expert_profiles.id
  person_id         uuid → persons.id
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

### Person
- `PersonCreated`
- `PersonAgeGroupUpdated`

### Household
- `HouseholdCreated`
- `PersonJoinedHousehold`
- `HouseholdMembershipRoleChanged`
- `PersonRemovedFromHousehold`

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
- `ShoppingTripStarted`
- `ShoppingTripConfirmed`            ← pantry additions triggered here
- `ShoppingTripCancelled`

### Planning & Recipe
- `WeeklyMealPlanGenerated`       ← AI proposes a full week; no commitment
- `WeeklyMealPlanAccepted`        ← household accepts the week in one action
- `WeeklyMealPlanAbandoned`
- `MealSwappedWithinWeek`         ← AI suggests or user swaps one meal in week
- `MealRecommended`              ← individual AI meal output; no commitment
- `MealRecommendationAccepted`   ← user accepts; creates MealPlan
- `MealRecommendationRejected`   ← user rejects; discarded
- `MealPlanned`                  ← MealPlan created (from recommendation or within weekly plan)
- `MealPlanParticipantsConfirmed`
- `MealPlanCancelled`
- `MealPlanSwapped`              ← one MealPlan replaced by another within a WeeklyMealPlan

### Cook Mode
- `CookModeSessionStarted`
- `CookModeStepCompleted`
- `CookModeSessionAbandoned`

> Cook Mode events are UI state only. They do not update the pantry. Pantry updates are produced by MealSession events.

### Meal Session
- `MealSessionPlanned`
- `MealSessionStarted`
- `MealSessionParticipantsConfirmed`
- `MealSessionCompleted`
- `MealSessionAbandoned`
- `LeftoversCreated`
- `LeftoversStoredToPantry`
- `PantryItemConsumed` *(emitted by MealSession on completion — the authoritative pantry deduction event)*
- `MealSessionPortionsCorrected`

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
event_version       integer         starts at 1; increment on breaking payload schema change
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

11. **`event_version` must be incremented on any breaking change to an event's payload schema.** Consumers must handle multiple versions. Old versions must not be silently ignored.

---

## Intelligence Layer

> **This section describes the Intelligence Layer. It is not part of the Domain Model. It lives in a separate schema. It is included here so engineers and product designers understand what KitchenOS learns, where it learns it from, and how it stays separate from domain facts.**

The Intelligence Layer is KitchenOS's moat. Not the pantry. Not the recipes. Not the meal plans. The value is in what the system has learned about a household over time — and how it applies that learning to reduce effort while maintaining trust.

### What It Is Not

- It is not a domain aggregate. It owns no domain events.
- It does not write to any domain table. It only reads from the domain event stream.
- It does not override domain facts. A learned preference never replaces an explicit allergy or goal.
- It is replaceable. If the AI model changes, the intelligence layer is rebuilt from the event stream. The domain is unaffected.

### Sub-Models

```text
Household Intelligence Model
│
├── Preference Model
│   ├── Cuisine affinity (learned from MealSession completions and rejections)
│   ├── Ingredient preferences (liked / disliked / avoided)
│   ├── Cooking complexity preference (quick weeknight vs elaborate weekend)
│   └── Confidence scores per preference, evidence count, last-reinforced date
│
├── Consumption Model
│   ├── Pantry depletion rates per item category
│   ├── Typical portion sizes per person per meal type
│   ├── Leftover behaviour (how often leftovers are eaten vs wasted)
│   └── Waste patterns per category (what expires unused)
│
├── Shopping Model
│   ├── Store preferences and frequency
│   ├── Typical basket composition per store
│   ├── Price sensitivity per category
│   └── Buy-in-bulk vs buy-fresh preference per item
│
├── Schedule Model  (Household Schedule Model)
│   ├── Typical participants per meal slot per day of week
│   ├── Absence and travel patterns per person
│   ├── Takeout nights (frequency and day)
│   ├── Guest meal frequency
│   └── Confidence scores per slot; decays without reinforcement
│
├── Cooking Confidence Model
│   ├── Skill level inference (from Cook Mode abandonment and recipe complexity accepted)
│   ├── Preferred cook time range per meal type
│   └── Equipment signals (if smart appliances integrated)
│
└── Expert Interaction Model
    ├── Expert plan acceptance and rejection rates
    ├── Which recommendations were acted on vs ignored
    └── Goal progress signals (derived from MealSession nutrition data)
```

### Learning Sources

| Sub-Model | Primary event sources |
|---|---|
| Preference Model | `MealSessionCompleted`, `MealRecommendationRejected`, `MealPlanSwapped` |
| Consumption Model | `PantryItemConsumed`, `PantryItemThrownAway`, `PantryItemExpired`, `MealSessionLeftoverRecorded` |
| Shopping Model | `ShoppingTripConfirmed`, `ReceiptItemsConfirmed`, `ShoppingItemRemoved` |
| Schedule Model | `MealSessionCompleted` (who participated), `MealPlanCancelled`, `WeeklyMealPlanAccepted` |
| Cooking Confidence | `CookModeSessionAbandoned`, `MealSessionCompleted` (recipe complexity) |
| Expert Interaction | `ExpertRecommendationApproved`, `ExpertRecommendationRejected` |

### Relationship to Domain Model

```text
Domain Events (immutable, append-only)
        │
        │  Learning Engine reads asynchronously
        ▼
Household Intelligence Model  (intelligence schema, separate)
        │
        │  Recommendation Engine reads synchronously at request time
        ▼
Recommendation output  →  user sees it  →  accepts or rejects  →  new domain event  →  loop
```

The Learning Engine never writes to domain tables. The Recommendation Engine never writes to domain tables. Domain facts are produced only by user-confirmed actions.

### Transparency and Control

Every sub-model must support:
- **Explainability**: the user can see what KitchenOS has learned about their household.
- **Correction**: the user can mark any inference as wrong.
- **Reset**: the user can erase any sub-model entirely.

This is a product requirement, not just a privacy posture. The household must always be in control of what the AI knows about them. See `ADR-009` and `10_Product_Vision.md`, Section 8.11.
