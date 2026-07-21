---
id: DOC-040
title: KitchenOS Technical Architecture
type: architecture
status: active
owner: architecture
depends_on: [DOC-020, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-012]
referenced_by: [DOC-050]
tags: [architecture, backend, ai, event-sourcing, offline, technology-stack, ddd, household-decision-engine, building-blocks]
date: 2026
---

# KitchenOS: Technical Architecture

> This document is the authoritative source for how KitchenOS is built: the AI architecture, backend design, event sourcing model, offline strategy, technology stack, architecture principles, and building blocks. Product decisions live in `10_Product_Vision.md`. Domain entity definitions live in `20_Domain_Model.md`. Specific technology choices are recorded in `60_Decision_Records/ADRs/`.

---

## 23. Identity Service and Data Minimisation Architecture

Full product-level rationale: `Products/KitchenOS/10_Product_Vision.md`, Sections 8.10 and 8.11. Architectural decision: `ADR-009`.

### Governing Principle

> **Collect only the information required to improve the user's experience.**

Every field in every table must have a clear answer to: what recommendation, safety check, or household decision does this enable? If there is no clear answer, the field does not belong.

### Four-Layer Model

```text
Layer 1 — Auth (separate schema)
  identities
  ├── id (uuid)
  ├── email              ← the only PII in the system
  ├── auth_provider      google | apple | email
  └── created_at

        ↓  identity_id bridge — crossed once at login, never again

Layer 2 — Person (domain schema)
  persons
  ├── id  (person_id)    ← used throughout domain, profile, meal session, and AI
  ├── identity_id        ← points up to identities; never read by AI or intelligence layer
  ├── age_group          adult | teen | child | infant
  └── age_range          25-34 | 35-44 | etc. (optional, for nutrition estimation)

        ↓  person_id

Layer 3 — Domain (domain schema)
  dietary_constraints, user_goals, nutrition_preferences  ← keyed on person_id
  household_memberships  ← person_id + household_id + role + permissions
  households, pantry_items, shopping_lists, meal_sessions, receipts, budgets

        ↓  person_id + household_id (only these travel to AI)

Layer 4 — Intelligence (separate schema)
  household_intelligence_model  ← learned beliefs, keyed on person_id + household_id
  ├── confidence-scored preferences
  ├── behavioural patterns
  └── never contains email, name, identity_id, or domain facts
```

### The Critical Distinction: Facts vs Beliefs

| Layer | Examples | Owned by |
|---|---|---|
| Auth | Email, auth token | Identity Service (auth schema) |
| Person / Domain | Allergies, goals, age group, dietary restrictions | Domain Model (domain schema) |
| Intelligence | Cuisine affinity, shopping habits, meal acceptance rate, confidence scores | Household Intelligence Model (intelligence schema) |

Person is a **domain concept**, not an AI concept. A Person with a peanut allergy has that allergy whether or not KitchenOS has AI. The allergy is a business fact owned by the domain. Cuisine preferences learned from behaviour are AI beliefs owned by the Intelligence Model. These must never be conflated.

### Why Physical Separation Matters

- `identities` and `persons` in separate schemas: breach of domain schema exposes no email or auth data.
- `persons` and `household_intelligence_model` in separate schemas: breach of intelligence schema exposes no identity or domain facts.
- The Collective Intelligence anonymisation pipeline reads only from the intelligence schema — it cannot accidentally include email, name, or allergies.
- The recommendation engine receives only `person_id` and `household_id`. It never touches `identities`.

### What KitchenOS Does and Does Not Store

| Data | Stored | Layer | Notes |
|---|---|---|---|
| Email | Yes | Auth | Identity Service only. |
| Name | No (display only) | — | `display_name` optional, UI-only, never in AI. |
| Exact age / birth date | No | — | `age_group` sufficient for nutrition estimation. |
| Allergies | Yes | Domain | Safety-critical. Keyed on `person_id`. |
| Height / weight | Only when goal requires | Domain | Scoped to person. Deleted when goal removed. |
| Medical conditions | Only when goal requires | Domain | Same scoping. |
| Shopping history | Yes | Domain | Household-level receipts. No name attached. |
| Cuisine preferences | Learned | Intelligence | Never stored as domain facts. |
| Location | Metro region only | Intelligence | For Collective observations. Never exact address. |

### Account Recovery and Multi-Device Sync

A user logging in on a new device authenticates via the Identity Service. `identity_id` resolves to `person_id`. Memberships are loaded. Household Context is assembled. From that point only `person_id` and `household_id` travel through the system — no identity data reaches the domain or intelligence layers.

### Nicknames

`display_name` is optional on `household_memberships` — for UI convenience only. Never used in AI prompts, domain event payloads, or data pipeline outputs. Internally all persons are referenced by `person_id`.

---

## 23A. Household Context (Application Layer)

> **Household Context is not a domain concept. It is an application-layer concept.**

It exists only while a user has an active session. It does not persist when the app is closed. It is not stored in the domain model or written to `domain_events`.

Full domain model definitions: `Products/KitchenOS/20_Domain_Model.md`, Ubiquitous Language.

---

### What Household Context Contains

```text
Household Context (session-scoped)
  identity_id          resolved at login from Identity Service
  active_household_id  which household all actions are directed to
  active_member_id     the member_id for this identity in this household
  role                 from HouseholdMembership — drives permissions
  locale               language and regional settings
  units                metric | imperial
  currency             for budget and price display
  current_session      device, timestamp, auth token reference
```

None of these fields belong in the domain model. They are application routing and presentation concerns.

---

### Architectural Layers (TOGAF separation)

| Layer | Concept | Examples |
|---|---|---|
| **Business / Domain** | What exists regardless of the application | Identity, Household, HouseholdMembership, Pantry, Receipt |
| **Application** | What exists during a session | Household Context, active_household_id, navigation state |
| **Technology** | How session state is implemented | JWT, Redis session cache, Flutter secure storage |

---

### Session Resolution at Login

```text
User authenticates (Firebase Auth)
        │
        ▼
Identity Service resolves identity_id
        │
        ▼
Look up HouseholdMembership(s) for identity_id
        │
        ├── one membership found  → set as active_household_id automatically
        │
        └── multiple memberships → prompt household switcher, user selects active household
                │
                ▼
        Household Context assembled
          active_household_id
          active_member_id
          role, locale, units, currency
                │
                ▼
        All subsequent requests carry household_id + member_id
        identity_id is not passed further
```

---

### Household Switcher (Application Layer, not Domain Layer)

The household switcher is a UI/application concern. It changes `active_household_id` in the session — it does not modify any domain entity.

**Rules:**
- If the user has **one household**: no switcher is shown. The app simply feels like "my kitchen."
- If the user has **two or more households**: a lightweight switcher appears in the header.
- Switching household changes all subsequent actions to route to the new `active_household_id`.
- Switching does not require re-authentication.

**Notifications** must be scoped to the source household when the user manages multiple:

> ~~"Your spinach expires tomorrow."~~
> **"Home: Your spinach expires tomorrow."**
> **"Parents: Milk is running low."**

---

### What Never Changes with Multi-Household

- Domain events always carry exactly one `household_id` — this rule does not change.
- The intelligence layer (Household Intelligence Model) is scoped per `household_id` — separate intelligence per household.
- The Collective Intelligence pipeline reads `household_id` from observations — multi-household users contribute observations independently per household.

---

## 23B. Identity & Access Management

> **Authentication and Authorization are platform capabilities, not business capabilities. They belong here, not in the Domain Model.**

The Domain Model defines *what exists* (Person, HouseholdMembership, role, permissions). This section defines *how those domain concepts are enforced at the platform level*.

---

### Authentication — Who Are You?

Answers the question: *Is this person who they claim to be?*

Implemented via Firebase Authentication. Supported sign-in methods:

| Method | Status |
|---|---|
| Google Sign-In | MVP-0 |
| Apple Sign-In | MVP-0 |
| Email + Password | MVP-0 |
| Passkeys | Post-MVP |
| MFA | Post-MVP |

Authentication is pure infrastructure. It knows nothing about households, pantry, or meal plans. It produces one output: a verified `identity_id`.

From that point on, `identity_id` is crossed to `person_id` once (at session resolution — see Section 23A) and does not travel further through the system.

---

### Authorization — What Can You Do?

Answers the question: *Is this person allowed to perform this action in this household?*

Authorization is derived entirely from the domain model:

```text
identity_id
    ↓  resolved once at login
person_id
    ↓  joined to
HouseholdMembership
    ↓  carries
role          "admin" | "member" | "caregiver" | "guest"
permissions   scoped capabilities (invite, delete, view_budget, etc.)
    ↓  evaluated by
Authorization Layer (API middleware)
    ↓
Request allowed or denied
```

**Example:**

```text
Raj
  Admin of Household A  → can invite members, delete pantry items, view budgets
  Member of Household B → cannot invite, cannot view other members' private goals

In Household A:
  ✓ Invite members
  ✓ Delete pantry items
  ✓ View household budget
  ✗ View another member's private nutrition goals (allergy_visibility: private)

In Household B:
  ✗ Invite members
  ✗ Delete pantry items
  ✗ Perform admin actions
```

Authorization is evaluated at the API layer on every request. It is never evaluated in the mobile client — the client shows or hides UI elements for UX convenience only, not security.

---

### Permission Scoping Rules

| Resource | Rule |
|---|---|
| Household data (pantry, shopping, timeline) | Any active member of the household |
| Admin actions (invite, remove member, archive household) | `role: admin` only |
| Another member's private goals | Only if that member sets `goal_visibility: household` |
| Another member's private allergies | Only if that member sets `allergy_visibility: household` |
| Expert data access | Only within an active, unexpired `ConsentGrant` scoped to named data types |
| Support Agent data access | Scoped, read-only, time-bounded — defined in `Products/KitchenOS/95_Customer_Expert_Operations/` |

---

### Session Security

- All API requests require a valid Firebase JWT.
- JWTs are short-lived (1 hour). Refresh tokens are rotated on use.
- `household_id` and `person_id` in request context are resolved server-side from the JWT — never trusted from client payload.
- Cross-household access attempts (a person attempting to read another household they are not a member of) are rejected at the authorization layer before any query executes.

---

### Actor Authorization Summary

| Actor | Auth Method | Authorization Scope |
|---|---|---|
| Customer | Firebase Auth (Google, Apple, Email) | Their households only, via HouseholdMembership |
| Expert | Firebase Auth + Expert Portal | Household data within active ConsentGrant only |
| Support Agent *(future)* | Internal SSO | Read-only, scoped to ticket context, time-bounded |
| Operations Engineer *(future)* | Internal SSO + MFA | Platform infrastructure only; no household data |
| AI (system) | Service account | Read domain events + intelligence; write via domain service only |

---

## 24. AI Architecture: Household Decision Engine

KitchenOS intelligence is not a chatbot bolted onto screens.

Core principle:

> Intelligence is the coordination layer that turns household context into safe, trusted food decisions.

### 24.1 Household Decision Engine

```text
AI Orchestrator
  |
  +-- Pantry AI
  +-- Shopping AI
  +-- Meal AI
  +-- Budget AI
  +-- Receipt AI
  +-- Consumption AI
  |
Household Knowledge Graph
  |
  +-- Receipts
  +-- Consumption
  +-- Budget
```

The Household Decision Engine does not merely answer questions. It maintains a living model of the household so KitchenOS can recommend, explain, and adapt decisions over time.

### 24.2 Household Knowledge Graph

Entities:

- Food items.
- Meals.
- Receipts.
- Stores.
- Budget categories.
- Recipes.
- Household members.

Relationships:

```text
Milk -> bought_at -> Costco
Milk -> used_in -> Pancakes
Milk -> expires_in -> 2 days
Milk -> price_history -> $3.99 average
Milk -> consumption_rate -> 8-day cycle
```

This allows KitchenOS to support decisions without asking the user repeatedly:

- What should I buy?
- What can I cook?
- Am I overspending?
- What will expire?
- What do I usually forget?

---

## 24A. Household Intelligence Model

> The Household Intelligence Model is the AI's continuously evolving understanding of a household. It combines explicit profile information, observed behaviours, learned preferences, contextual signals, and confidence scores to produce personalised guidance.

This is a first-class architectural artifact — distinct from the Domain Model, distinct from the User Profile, and distinct from the Recommendation Engine. It is the reasoning substrate of the Household Decision Engine.

Full product-level explanation: `Products/KitchenOS/10_Product_Vision.md`, Section 50A.

### Why a Separate Layer

The Domain Model stores **facts**.

```text
Milk — Quantity: 2 litres — Expires: June 10
```

The Household Intelligence Model stores **beliefs**.

```text
Milk consumption cycle — Estimate: 8 days — Confidence: 91%
Evidence: 14 purchase events, 6 cook completions using milk
```

One is a recorded event. One is a derived inference. They must never be mixed into the same data model. If the intelligence model is replaced — different AI provider, new recommendation model, reinforcement learning — nothing in the Domain Model changes.

### Structure

Full sub-model specification: `Products/KitchenOS/20_Domain_Model.md`, Intelligence Layer section.

```text
Household Intelligence Model
│
├── Preference Model
│   ├── Cuisine affinity
│   ├── Ingredient preferences
│   ├── Cooking complexity preference
│   └── Confidence scores + evidence count + last-reinforced date
│
├── Consumption Model
│   ├── Pantry depletion rates per category
│   ├── Typical portion sizes per person per meal type
│   ├── Leftover behaviour
│   └── Waste patterns per category
│
├── Shopping Model
│   ├── Store preferences and frequency
│   ├── Typical basket composition
│   ├── Price sensitivity per category
│   └── Buy-in-bulk vs buy-fresh preference
│
├── Schedule Model  (see Household Schedule Model section above)
│   ├── Participants per meal slot per day of week
│   ├── Absence and travel patterns
│   ├── Takeout nights
│   └── Guest frequency
│
├── Cooking Confidence Model
│   ├── Skill level inference
│   ├── Preferred cook time range per meal type
│   └── Equipment signals (if smart appliances integrated)
│
├── Expert Interaction Model
│   ├── Expert plan acceptance / rejection rates
│   ├── Which recommendations were acted on vs ignored
│   └── Goal progress signals
│
└── Current Context  (live, refreshed per recommendation request — not persisted)
    ├── Pantry state snapshot
    ├── Budget status and spend pace
    ├── Active season / weather signal (optional)
    └── Calendar signal (optional, explicit opt-in)
```

### Storage Considerations

| Component | Storage | Notes |
|---|---|---|
| Static Facts | PostgreSQL (user_goals, dietary_constraints tables) | Written once at onboarding, editable |
| Learned Preferences | PostgreSQL or dedicated ML feature store | Updated asynchronously after events |
| Confidence Scores | Stored alongside learned preferences | Decays over time without reinforcing events |
| Current Context | Redis (materialised household state) | Refreshed on each recommendation request |

### Relationship to Other Components

```text
Domain Events (append-only)
        │
        ▼
Learning Engine  ──────────────────►  Household Intelligence Model
                                              │
                                              ▼
                           Recommendation Engine
                                    │         │
                           Domain Facts    AI Beliefs
                                    │         │
                                    └────┬────┘
                                         ▼
                                   Guidance Output
                                 (explained, safe, ranked)
```

The Learning Engine reads domain events and updates the Household Intelligence Model asynchronously. The Recommendation Engine reads both the Domain Model and the Intelligence Model synchronously at request time.

### Household Schedule Model

A named sub-model within the Household Intelligence Model. Represents the household's **learned weekly routine** — distinct from food preferences and pantry behaviour.

```text
Household Schedule Model
│
├── Typical participants per meal slot
│   ├── Monday Dinner: everyone (confidence 97%)
│   ├── Friday Dinner: takeout (confidence 83%)
│   └── Saturday: extended family likely (confidence 61%)
│
├── Absence patterns
│   ├── Adult 1 travels Tuesdays 3 of 4 weeks
│   └── Child 2 has soccer Wednesday evenings
│
├── Routine exception signals
│   ├── Family calendar integration (optional, explicit opt-in)
│   └── Pattern deviation detection (e.g. less cooking than usual last 3 days)
│
└── Confidence scores per slot
    Decays when patterns change. Resets on explicit user correction.
```

**What it feeds:**
- Weekly meal plan generation (who to plan for each night)
- Per-meal participant pre-filling at "Start Cooking"
- Confidence-based questioning threshold (Principle 8.13)
- Proactive mid-week swap suggestions (expiry risk + schedule mismatch)

**What it is NOT:**
- Not a calendar. It does not own schedule data.
- Not a domain concept. It does not produce domain events.
- Not authoritative. It is a probabilistic model. The user always confirms.

**Storage:** Intelligence schema. Keyed on `household_id`. Never keyed on `identity_id`. Updated asynchronously by the Learning Engine after MealSession completions and plan deviations.

---

### Closed-Loop Weekly Planning Architecture

```text
Sunday evening
      │
      ▼
Household Schedule Model ──────────────────────────────────┐
      +                                                     │
Pantry State (domain events)                         feeds │
      +                                                     │
Household Intelligence Model (food prefs, goals)           │
      │                                                     │
      ▼                                                     ▼
Recommendation Engine ──────────────► WeeklyMealPlan (proposed)
                                              │
                                     User accepts ("Accept Week")
                                              │
                                              ▼
                                     WeeklyMealPlanAccepted event
                                     MealPlans created (one per slot)
                                              │
                              ┌───────────────┤ Week unfolds
                              │               │
                     Pantry changes      Schedule changes
                     Leftovers appear    Calendar signals
                     Expiry risk         Deviations detected
                              │               │
                              └───────────────┤
                                              │
                                     AI suggests mid-week swaps
                                     User confirms each swap
                                              │
                              Each evening: Daily reminder shown
                                              │
                                     User taps "Start Cooking"
                                              │
                                     MealSession created
                                              │
                                     Cooking completes
                                              │
                                     PantryItemConsumed events
                                     Nutrition recorded
                                     Learning Engine updates model
```

The loop closes when MealSession completions feed back into the Household Intelligence Model and Household Schedule Model — making the next week's plan more accurate.

---

### Transparency Requirement

Every learned preference in the Intelligence Model must be:

- **Explainable** — the user can see what KitchenOS has learned.
- **Editable** — the user can correct any inference.
- **Resettable** — the user can erase any learned preference.

This is a product requirement, not just a UX nicety. See `Products/KitchenOS/10_Product_Vision.md`, Section 50A for the UX specification.

### Scope by MVP Phase

| Phase | Intelligence Model Scope |
|---|---|
| MVP-0 | Static Facts only — onboarding data seeds the model; no behavioural learning yet |
| MVP-1 | Basic behavioural signals — meal acceptance/rejection, pantry depletion rates |
| Post-MVP | Full confidence-scored preference model, Learning Engine, transparency screen |

---

## 25. AI Orchestrator

The AI Orchestrator is responsible for:

### 25.1 Intent Detection

Example:

```text
User input: What should I cook?
Intent: Meal Recommendation
Context: Pantry + Preferences + Time + Budget
```

### 25.2 Agent Routing

The orchestrator routes work to the right agents.

Example:

- Meal AI generates recipe candidates.
- Pantry AI checks ingredient availability.
- Budget AI filters expensive options.

### 25.3 Aggregation and Explanation

Final output should be concise and grounded.

Example:

> You can cook Palak Dal. You already have 92% of the ingredients. It fits your budget and usually takes 25 minutes.

---

## 26. AI Agents

### 26.1 Pantry AI

Responsible for:

- Inventory tracking.
- Expiration prediction.
- Usage rate estimation.
- Missing item detection.

Example:

> Milk will run out in 2 days based on your usage pattern.

### 26.2 Shopping AI

Responsible for:

- Optimizing shopping lists.
- Store comparison.
- Cost estimation.
- Trip bundling.

Example:

> Buying these items at Costco saves $8.40 compared to Walmart.

### 26.3 Meal AI

Responsible for:

- Recipe generation.
- Pantry-based suggestions.
- Nutrition matching.
- Time-based suggestions.

Example:

> You usually cook light meals on weekdays. Suggesting Veg Stir Fry.

### 26.4 Budget AI

Responsible for:

- Spending tracking.
- Anomaly detection.
- Forecasting.
- Category optimization.

Example:

> Your grocery spend is 12% higher this month due to dairy.

### 26.5 Receipt AI

Responsible for:

- Document extraction via Document Understanding (multimodal LLM — ADR-012).
- Item normalization.
- Price mapping.
- Store detection.

### 26.6 Consumption AI

Responsible for:

- Learning eating habits.
- Predicting depletion.
- Improving future planning.

---

## 27. AI Memory System

AI memory is not chat history. It is structured household memory.

### 27.1 Short-Term Memory

- Current week plan.
- Active shopping list.
- Pending receipts.

### 27.2 Long-Term Memory

- Purchase frequency.
- Food preferences.
- Store preferences.
- Consumption patterns.

Example:

```text
Milk: bought every 8 days
Bananas: bought every 5 days
Costco: preferred for bulk items
```

---

## 28. AI Decision Flow

Every recommendation should follow a consistent pipeline.

```text
User Action or Event
  -> Context Builder
  -> Knowledge Graph Query
  -> Agent Processing
  -> Constraint Filtering
  -> Ranking Engine
  -> Explanation Generator
  -> UI Output
```

Constraint filtering should account for:

- Budget.
- Time.
- Nutrition.
- Pantry availability.
- Expiration urgency.
- User preferences.

---

## 29. Event-Driven Intelligence

AI is triggered by events.

Example events:

- Receipt scanned.
- Item consumed.
- Item expiring.
- Weekly plan needed.
- Budget threshold reached.

Example event chain:

```text
Receipt scanned
  -> Pantry updated
  -> Budget updated
  -> Shopping list updated
  -> Meal plan recalculated
  -> Notification generated
```

---

## 30. Explanation Layer

Every AI output should include:

- Why it was recommended.
- What data was used.

Example:

> We recommended Pasta because you have tomatoes and onions, it takes under 30 minutes, and you usually cook it on Wednesdays.

Without explanation, AI feels random. With explanation, AI feels trustworthy.

---

## 31. AI Cost Control Strategy

KitchenOS should not call LLMs for everything.

| Tier | Method | Example |
|---|---|---|
| Tier 1 | Rules | Expiration alerts, pantry thresholds |
| Tier 2 | ML models | Consumption prediction, demand forecasting |
| Tier 3 | LLM | Meal planning, explanations, conversational AI |

Principle:

> Use the cheapest reliable intelligence for each job.

---

## 32. Backend Architecture

Core backend requirement:

> The system must always know the truth about the household.

KitchenOS should use:

> Event-driven architecture + household state graph.

This section is the source of truth for domain-driven event architecture. Negative flows, corrections, Household Timeline, offline sync, and AI learning should all depend on this model.

### 32.1 Core System Design

```text
User Actions
  -> Domain Commands
  -> Event Generator
  -> Event Stream
  -> Domain Services
  -> Household State View
  -> Household Timeline Read Model
  -> AI Decision Engine
  -> UI Layer
```

### 32.2 Event Sourcing Model

Every meaningful action becomes an immutable event.

Example events:

- `ReceiptScanned`
- `ItemAddedToPantry`
- `ItemConsumed`
- `MealPlanned`
- `MealCooked`
- `ShoppingItemAdded`
- `BudgetUpdated`
- `ReceiptMarkedDuplicate`
- `ReceiptEffectsReversed`
- `PantryItemThrownAway`
- `ShoppingItemRemoved`
- `ExpertRecommendationApproved`

Example payload:

```json
{
  "event_type": "ItemConsumed",
  "domain": "pantry",
  "timestamp": "2026-01-23T18:22:00Z",
  "household_id": "h123",
  "user_id": "u123",
  "item": "Milk",
  "quantity": 1,
  "unit": "liter",
  "source": "cook_mode",
  "learning_impact": "consumption_signal"
}
```

### 32.3 Why Event Sourcing Matters

If the system only stores:

```text
Milk = 2 liters
```

It loses:

- When milk was bought.
- How fast it is consumed.
- Price changes.
- Usage patterns.
- Whether a quantity change was consumption, waste, correction, or reversal.
- Which receipt, user, AI suggestion, expert recommendation, or device caused the change.

With events, the system can reconstruct:

- Consumption rate.
- Expiration prediction.
- Purchase frequency.
- Cost behavior.
- Waste patterns.
- Activity history.
- Correction history.
- AI learning eligibility.

Without events, AI guesses. With events, AI predicts and explains.

### 32.4 Domain Event Boundaries

Events should be organized by product domain, not by database table.

Recommended event domains:

```text
Household
  -> membership, roles, permissions, shared settings

Profile and Safety
  -> allergies, dietary restrictions, goals, medical constraints

Receipt
  -> scanning, document understanding, item extraction, duplicate detection, reversal

Pantry
  -> item creation, quantity changes, expiry, consumption, waste, correction

Shopping
  -> list creation, item addition, removal, purchase, rejection

Planning and Recipe
  -> meal plans, recipe recommendations, substitutions, rejections

Cook Mode
  -> cooking sessions, step completion, pantry deduction, deduction reversal

Budget
  -> grocery spend, category updates, budget reversal

Expert Marketplace
  -> expert relationships, consent, recommendations, approvals

Correction and Activity
  -> undo, reversal, activity timeline grouping, non-learning markers
```

This prevents one module from silently mutating another module's state without a traceable event.

### 32.5 Commands vs Events

Product actions should distinguish commands from events.

Commands are requests:

```text
Scan receipt
Remove shopping item
Mark yogurt as thrown away
Approve expert recommendation
Undo receipt effects
```

Events are facts:

```text
ReceiptScanned
ShoppingItemRemoved
PantryItemThrownAway
ExpertRecommendationApproved
ReceiptEffectsReversed
```

The product should show commands in the UI and preserve events in the system ledger.

### 32.6 Standard Event Envelope

Every domain event should share a common envelope.

Suggested fields:

```text
event_id
event_type
domain
household_id
actor_type
actor_id
source_type
entity_type
entity_id
occurred_at
payload
correlation_id
causation_id
reversal_of_event_id
learning_impact
privacy_level
```

Important fields:

- `correlation_id` groups related events from one action, such as one receipt scan creating pantry, budget, and shopping updates.
- `causation_id` shows which event caused another event.
- `reversal_of_event_id` links undo or correction events back to the original event.
- `learning_impact` tells AI whether the event should affect future recommendations.
- `privacy_level` helps control access for household members, experts, and future organization accounts.

### 32.7 Reversal and Correction Events

KitchenOS should not hard-delete meaningful household events as the default behavior.

Use reversal events:

```text
ReceiptScanned
  -> PantryItemsAddedFromReceipt
  -> BudgetSpendRecorded
  -> ShoppingItemsMatched

ReceiptMarkedDuplicate
  -> PantryReceiptAdditionsReversed
  -> BudgetSpendReversed
  -> ShoppingMatchesUnlinked
```

Use correction events:

```text
PantryItemConsumed
  -> PantryItemConsumptionCorrected
  -> PantryItemMarkedThrownAway
  -> LearningImpactChangedToWasteSignal
```

This allows KitchenOS to preserve history while keeping the current household state accurate.

### 32.8 Household Timeline Read Model

The Household Timeline should be generated from grouped events, not manually maintained as unrelated UI text. The Activity Log is the implementation read model that powers the user-facing Household Timeline.

Technical events:

```text
ReceiptScanned
ReceiptOcrCompleted
ReceiptItemsConfirmed
PantryItemsAdded
BudgetSpendRecorded
ShoppingItemsMatched
```

User-facing Household Timeline entry:

```text
Costco receipt scanned.
8 pantry items added, 3 shopping items completed, $84.31 recorded.
```

Product rule:

> The event ledger is for system truth. The Household Timeline is for user trust.

### 32.9 MVP Event Scope

MVP should use a pragmatic event architecture:

```text
PostgreSQL primary tables
  + append-only domain_events table
  + materialized household state views
  + Household Timeline / Activity Log read model
```

MVP event domains:

- Receipt.
- Pantry.
- Shopping.
- Cook Mode.
- Profile and Safety.
- Correction and Activity.

Post-MVP event domains:

- Expert Marketplace.
- Advanced nutrition goals.
- Fitness context.
- Organization/provider accounts.
- Live sessions.

The final backend rule:

> Store what happened as domain events, compute current household state from those events, and use correction/reversal events instead of silent mutation whenever user trust or AI learning is affected.

---

## 33. Materialized Household State

Events are the source of truth, but the UI needs fast access.

Therefore KitchenOS needs materialized views:

- Current pantry state.
- Current budget state.
- Current meal plan.
- Current shopping list.
- Current consumption trends.
- Current Household Timeline.
- Current correction and reversal status.

Principle:

```text
Events = immutable truth
State = computed fast access
```

---

## 34. Core Services

### 34.1 Pantry Service

Responsibilities:

- Inventory updates.
- Expiry tracking.
- Consumption inference.

### 34.2 Shopping Service

Responsibilities:

- List generation.
- Store optimization.
- Cost estimation.

### 34.3 Recipe Service

Responsibilities:

- Recipe storage.
- Ingredient matching.
- Substitution logic.

### 34.4 Budget Service

Responsibilities:

- Expense tracking.
- Category analysis.
- Forecasting.

### 34.5 Receipt Service

Responsibilities:

- Document Understanding ingestion (ADR-012).
- Item normalization.
- Price mapping.

### 34.6 AI Orchestration Service

Responsibilities:

- Event interpretation.
- Recommendation generation.
- Ranking.
- Explanation building.

### 34.7 Timeline, Activity, and Correction Service

Responsibilities:

- Household Timeline grouping.
- Undo and reversal coordination.
- Correction reason tracking.
- Learning impact updates.
- Audit trail coordination.

---

## 35. Offline Architecture

Offline-first is critical for real kitchen and grocery use.

### 35.1 Local Device Layer

Store locally:

- Pantry snapshot.
- Shopping list.
- Meal plan.
- Cached recipes.
- Pending events.

### 35.2 Sync Layer

```text
Local Events Queue
  -> Sync Engine
  -> Conflict Resolution
  -> Cloud Event Store
```

### 35.3 Offline Behavior

User actions are:

- Stored locally.
- Immediately reflected in UI.
- Queued for sync.

No core action should block because of missing network connectivity.

### 35.4 Conflict Resolution

Use event ordering and timestamps.

Example:

```text
Device A: Milk consumed at 10:00
Device B: Milk added at 10:05
Final state: derived from event sequence
```

---

## 25. Household Activity Lifecycle Pattern

Full product context: `Products/KitchenOS/10_Product_Vision.md`. Governing ADR: `ADR-010`.

> **The pantry is never updated by a recommendation, a recipe, or a prediction. It is only updated by confirmed household activities.**

This is the most important invariant in the KitchenOS backend. It is not a technical preference — it is what makes pantry state trustworthy enough to base AI recommendations on.

---

### What Is the Household Activity Lifecycle?

It is an **architectural pattern**, not a domain entity. Users do not create "activities." They shop, cook, throw food away, and correct their pantry. Each of these is a distinct first-class domain concept. What they share is a reusable lifecycle:

```text
Planned → Started → In Progress → Completed → Domain Events emitted
                                       ↓
                                  Pantry updated
                                  Budget updated
                                  Nutrition updated
                                  Household Timeline updated
```

The pattern applies to every household action that changes pantry state.

---

### The Four Activity Types

| Activity | Domain Aggregate | Pantry Effect |
|---|---|---|
| **Shopping Trip** | ShoppingTrip / Receipt | Adds items to pantry on confirmation |
| **Meal Session** | MealSession | Deducts items from pantry on completion |
| **Waste Event** | WasteEvent (via PantryCorrection) | Removes items from pantry on confirmation |
| **Pantry Correction** | PantryCorrection | Adjusts quantities on confirmation |

Each follows the same lifecycle. Each produces its own domain events. None of them delegate pantry updates to a recipe, a recommendation, or a UI component.

---

### The Symmetry

```text
ACQUIRE FOOD                        USE FOOD
─────────────                       ────────
Shopping Trip                       Meal Session
      ↓                                   ↓
   Receipt                             Recipe (optional)
      ↓                                   ↓
Items Confirmed                     Participants Confirmed
      ↓                                   ↓
Pantry ADDED                        Pantry DEDUCTED
Budget RECORDED                     Nutrition RECORDED
Price History UPDATED               Leftovers CREATED (if any)
```

Both sides follow the same lifecycle. Both require user confirmation before pantry state changes. Neither side allows silent, automatic pantry mutation.

---

### Cook Mode's Role

Cook Mode is a **UI capability**, not a domain aggregate. It facilitates a MealSession by providing step-by-step guidance. It does not own pantry state.

```text
Cook Mode (UI)
      ↓
  facilitates
      ↓
MealSession (domain aggregate)
      ↓
  on completion + user confirmation
      ↓
PantryItemConsumed events emitted
      ↓
Pantry updated
```

This separation means:
- A user can log a meal without using Cook Mode (manual entry).
- A future voice interface or smart oven integration produces the same MealSession — same pantry outcome.
- Cook Mode steps are UI state events (`cook.*`). They do not produce pantry events.

---

### The Confirmation Step

Every activity requires a user confirmation step before pantry state changes. This is intentional.

| Activity | What triggers confirmation |
|---|---|
| Shopping Trip | "Confirm items from this receipt" |
| Meal Session | "Cooking complete — confirm portions and participants" |
| Waste Event | "Confirm you threw this away" |
| Pantry Correction | "Confirm updated quantity" |

The AI can pre-fill suggestions for all of these. The user approves. The domain event is written. The pantry updates. This keeps pantry state accurate, auditable, and trustworthy.

---

### Guests and Unexpected Portions

MealSession handles the "unexpected guests" case cleanly. The default is the household's active participants. Before confirming completion, the user can adjust:

```text
Cooking for:
  ✓ Household (Adult 1, Child 1)
  or Custom: Adults 3, Children 2
```

The adjusted participants and portions are stored on the MealSession. Pantry deduction and nutrition tracking use the confirmed values — not the recipe's default servings.

---

## 36. AI Data Pipeline

AI should not read the UI. It should read system data.

Input sources:

- Event stream.
- Household graph.
- Materialized views.

Pipeline:

```text
Events
  -> Feature Builder
  -> Context Pack
  -> AI Models
  -> Recommendations
  -> UI Output
```

---

## 36A. Collective Intelligence Architecture

Full product-level explanation and consent model: `Products/KitchenOS/10_Product_Vision.md`, Section 54A.

### Purpose

The Collective Intelligence Model learns from anonymised observations contributed by opted-in households. It produces shared intelligence signals that improve recommendations for every household on the platform — including those that have little personal history.

This is architecturally separate from the Household Intelligence Model (Section 24A), which learns only from one household's own events.

### Intelligence Model Relationship

```text
Household A events ──┐
Household B events ──┤
Household C events ──┼──► Anonymisation Pipeline
Household N events ──┘           │
                                 ▼
                     Collective Intelligence Model
                          │
                          │   (regional prices, seasonal trends,
                          │    recipe success, depletion rates,
                          │    waste patterns, recommendation
                          │    acceptance rates)
                          │
                          ▼
                   Recommendation Engine
                          ▲
                          │
               Household Intelligence Model
               (this household's own context)
```

The Recommendation Engine reads both models at request time. Personal context determines relevance. Collective context improves calibration and fills gaps where personal history is thin.

---

### Consent and Privacy Architecture

> **Collective intelligence is built through informed participation, never silent collection.**

| Rule | Detail |
|---|---|
| Default | All household data is private. No contribution without explicit opt-in. |
| Opt-in trigger | Presented after first meaningful household action (e.g. first receipt scanned). Never during onboarding. |
| What is contributed | Anonymised item-level observations stripped of all identifying context. |
| What is never contributed | Household ID, user ID, names, emails, device identifiers, timestamps precise enough to identify a household. |
| Identifiable vs non-identifiable | Item-level observations are permitted. Identifiable observations are not. This is the governing distinction. |
| Opt-out | Any time. Stops future contributions. Schedules removal of prior contributions from the learning pipeline. |
| Transparency | Users can see which observation categories they are contributing to. |

---

### Anonymisation Pipeline

Runs asynchronously after domain events are recorded. Never runs in the hot path of a user request.

```text
Domain Event recorded
        │
        ▼
Consent check  ──── not opted in ──► discard
        │
        ▼ opted in
Anonymisation step
  • Strip household_id, user_id, timestamps beyond month/year
  • Generalise location to metro region
  • Generalise household type (2 adults, family, etc.)
  • Remove quantities that could fingerprint a household
        │
        ▼
Observation record written to
Collective Intelligence Store
        │
        ▼
Learning Engine batch job
(runs offline, not per-request)
```

---

### Observation Schema

Every observation has a type, anonymised attributes, and no household identity.

```text
PriceObservation
  item_category     string        e.g. "Organic Whole Milk"
  store_chain       string        e.g. "Costco"
  region            string        e.g. "Austin Metro"
  price_usd         decimal
  month             YYYY-MM

RecipeObservation
  recipe_id         string        internal recipe identifier
  outcome           enum          accepted | rejected | abandoned
  actual_cook_time  integer       minutes
  household_type    string        e.g. "2 adults"
  region            string

PantryDepletionObservation
  item_category     string
  avg_days_to_depletion  integer
  household_type    string
  region            string

WasteObservation
  item_category     string
  waste_reason      enum          expired | thrown_away | unknown
  household_type    string
  region            string
```

No `household_id`. No `user_id`. No exact date. No personal identifiers.

---

### Collective Intelligence Store

| Concern | Approach |
|---|---|
| Storage | Separate database from operational PostgreSQL — keeps collective data physically isolated from household data |
| Access pattern | Batch reads by Learning Engine; read-only by Recommendation Engine at request time |
| Retention | Observations are immutable. Opt-out triggers a deletion job scoped to the contributing household's contribution epoch. |
| Encryption | Encrypted at rest. No cross-join possible back to operational household tables. |

---

### MVP Phase Scope

| Phase | Collective Intelligence Scope |
|---|---|
| MVP-0 | Not active. No observations collected. Recommendation Engine uses Household Intelligence Model only. |
| MVP-1 | Opt-in consent UI built. Anonymisation pipeline live. Price and recipe observations collected. Collective model used to bootstrap new households with thin history. |
| Post-MVP | Full Learning Engine. Seasonal models. Regional price forecasting. Recipe success models. Recommendation Engine uses full two-model input. |

---

## 37. Technology Stack Recommendation

The older KitchenOS vision recommends a **Flutter-first mobile architecture**.

### 37.1 Mobile App

Recommendation:

> Flutter

Why Flutter fits KitchenOS:

- Single codebase for iOS and Android.
- Strong offline UI performance.
- Smooth animations for Cook Mode.
- Strong local state handling.
- Good SQLite and sync ecosystem.

Recommended Flutter architecture:

```text
UI Layer
  -> State Management: Riverpod or Bloc
  -> Domain Layer: Use Cases
  -> Repository Layer
  -> Local DB + Sync Engine
```

Recommended mobile stack:

- Flutter.
- Riverpod or Bloc.
- SQLite with Drift.

### 37.2 Backend

Recommendation:

> Modular monolith first, not microservices.

Recommended backend stack:

- Node.js with NestJS.
- PostgreSQL.
- Redis.

Backend structure:

```text
API Layer
  -> Application Layer
  -> Domain Layer
  -> Event Bus
  -> Data Layer
```

### 37.3 Database Strategy

Use three storage layers.

#### Primary Database: PostgreSQL

Stores:

- Users.
- Households.
- Pantry snapshots.
- Shopping lists.
- Recipes.
- Budget summaries.

#### Event Store: PostgreSQL Initially

Stores immutable household events.

#### Cache Layer: Redis

Used for:

- Home screen state.
- AI recommendations.
- Pantry summary.
- Meal suggestions.

### 37.4 Local Database

On-device database:

> SQLite via Drift or equivalent.

Stores:

- Pantry snapshot.
- Shopping list.
- Meal plan.
- Cached recipes.
- Pending sync events.

Principle:

> Mobile DB is not a copy of backend. It is a working local state machine.

### 37.5 AI Layer

Recommended stack in the older vision:

- OpenAI API as primary LLM provider.
- Optional local model fallback later.
- Vector DB such as Pinecone or Weaviate later.

MVP-0 should use AI minimally for:

- Recipe generation.
- Simple suggestions.

No full AI orchestration layer is required in MVP-0.

The Household Decision Engine must call an AI provider through an abstraction interface. Application code should never reference a specific provider (OpenAI, Anthropic, Gemini) directly. This allows provider switching without architectural changes.

### 37.6 Cloud Infrastructure

KitchenOS should run on **Google Cloud Platform (GCP)** for MVP-0.

Rationale specific to KitchenOS:

- Flutter is a Google product. Firebase integrates natively for auth, push notifications, and analytics with excellent Flutter SDK support.
- Gemini multimodal models, reached through the AI Provider Abstraction, cover Document Understanding for receipts within the same ecosystem (ADR-012).
- Cloud Run provides simple serverless container deployment for NestJS without Kubernetes complexity.
- Firebase Authentication handles Google Sign-In and Apple Sign-In cleanly with less configuration than alternatives.
- Future AI expansion using Vertex AI or Gemini stays within the same cloud ecosystem.

Do not start with Kubernetes, service meshes, or distributed event buses. One Cloud Run service with one Cloud SQL instance is sufficient for thousands of households.

**MVP-0 Infrastructure Architecture:**

```text
Flutter App (Firebase Auth, Firebase Cloud Messaging)
       │
    HTTPS
       │
  Cloud Run (NestJS container)
  [Load balancing, HTTPS termination, and autoscaling
   are handled automatically by Cloud Run.
   No separate load balancer required in MVP-0.]
       │
 ├── Cloud SQL (PostgreSQL)
 ├── Memorystore (Redis)
 ├── Cloud Storage (receipt images)
 ├── Multimodal LLM API (Document Understanding — ADR-012)
 └── Secret Manager (API keys, LLM tokens)
```

> Note: An explicit Cloud Load Balancer is only needed when adding Cloud CDN, custom SSL certificates, canary deployments, or Cloud Armor (DDoS/WAF). None of these are required in MVP-0.

**Deployment pipeline:**

```text
GitHub
  -> GitHub Actions
  -> Run Tests
  -> Build Docker Image
  -> Push to Artifact Registry
  -> Deploy to Cloud Run
```

**Cloud service map:**

| Layer | GCP Service | Notes |
|---|---|---|
| Compute | Cloud Run | Serverless NestJS container. No server management. |
| Database | Cloud SQL (PostgreSQL) | Managed Postgres with automated backups. |
| Cache | Memorystore (Redis) | Home screen state, AI recommendations, pantry summary. |
| Object Storage | Cloud Storage | Receipt images, attachments. Metadata stored in Postgres. |
| Document Understanding | Multimodal LLM via AI Provider Abstraction | Structured receipt extraction with per-field confidence; model choice per AI Governance Model Evaluation (ADR-012). |
| Authentication | Firebase Authentication | Email, Google, Apple Sign-In. Native Flutter SDK. |
| Push Notifications | Firebase Cloud Messaging | Android and iOS notifications from a single API. |
| Secrets | Secret Manager | API keys and credentials. Never hardcoded. |
| CI/CD | GitHub Actions + Cloud Build | Automated builds, tests, and deployments. |
| Monitoring | Cloud Logging + Cloud Error Reporting + Sentry | Crash tracking and production visibility. |
| Job Queue | Cloud Tasks | Async Document Understanding processing. Add from MVP-0. |

**Connection pooling note:**

The `domain_events` append-only table creates insert-heavy write patterns. Use **Cloud SQL Proxy** or **PgBouncer** for connection pooling from day one, not at scale.

**Do not self-host in MVP-0:**

- Authentication.
- Push notifications.
- AI models.
- Background job infrastructure.

**Scaling path:**

```text
MVP-0 (0–5,000 households)
  -> Cloud Run handles load balancing, HTTPS, and autoscaling automatically
  -> Custom domain via Cloud Run domain mapping (no CLB required)
  -> Cloud SQL + Cloud Storage

MVP-1 to Phase 3 (5,000–50,000 households)
  -> Cloud Run continues to autoscale without configuration changes
  -> Cloud SQL read replicas added for read-heavy queries
  -> Cloud CDN introduced for receipt images and static assets
  -> Explicit Cloud Load Balancer required at this point because
     Cloud CDN can only attach to a CLB backend, not directly to Cloud Run

Post-Phase 3 (50,000+ households)
  -> Cloud Armor added behind the CLB for DDoS protection and WAF rules
  -> Cloud CDN extended to cacheable API responses
  -> Multi-region Cloud Run with CLB global anycast routing
  -> Background workers via Cloud Tasks or Pub/Sub
  -> Dedicated AI service
  -> Search and analytics services
```

> Key rule: Cloud Run handles autoscaling and load distribution automatically at every stage. An explicit Cloud Load Balancer is only introduced when Cloud CDN or Cloud Armor is needed, not for scaling or custom domain purposes. Custom domains are supported by Cloud Run natively from day one.

### 37.7 API Design

Recommended split:

- REST for events and commands.
- GraphQL or state endpoints for UI state.

Core APIs:

```text
POST /events
GET /household/state
POST /ai/recommendations
```

### 37.8 Offline AI Context Constraint

The Household Decision Engine runs on the backend and reads household context from Cloud SQL and Redis. It has no access to the device's local SQLite database.

This creates a known constraint: **if the user makes changes while offline, the AI will recommend against stale context until those changes sync to the backend.**

Example:

```text
User is offline
  -> Cooks a meal and deducts pantry items locally
  -> Marks three items as out of stock
  -> These changes live in local SQLite as pending sync events

User requests AI recommendation while still offline
  -> Request cannot reach backend
  -> App serves last cached recommendation from local SQLite
  -> Cached recommendation may reference items the user just consumed

User comes back online
  -> Pending sync events flush to backend
  -> domain_events table updated
  -> Redis cache invalidated for this household
  -> Next recommendation request reads fresh context from Cloud SQL
  -> Fresh recommendation returned and cached locally
```

Accepted trade-offs:

- Offline recommendations are based on last synced state. This is expected and acceptable.
- The app must show a stale data indicator when serving a cached recommendation.
- The system must never learn from unsynced events. Learning signals are derived from confirmed backend events only.
- Sync must be prioritised immediately when connectivity is restored before any new AI request is triggered.

Cache staleness model:

The local pending queue is not a reliable household-level staleness signal. In a multi-member household, other members on other devices may have already synced high-impact events — cooked meals, consumed pantry items, scanned receipts — that this device has no visibility into while offline.

Staleness ownership belongs to the backend. The device is a consumer of that decision, not the decision maker.

```text
Backend generates recommendation
  -> Calculates recommendation_expires_at
     based on household member count and recent event rate
     (high-activity multi-member household = shorter window)
     (low-activity single-member household = longer window)
  -> Returns recommendation + recommendation_expires_at to device

Device caches recommendation + recommendation_expires_at
  in local SQLite

Device offline — staleness evaluation:
  Check 1: Past recommendation_expires_at
    -> Suppress recommendation

  Check 2: Within expiry, but local high-impact pending events exist
    meal_cooked, pantry_items_consumed,
    receipt_scanned, shopping_completed
    -> Show with stale warning
    (Local queue can only move expiry earlier, never extend it)

  Check 3: Within expiry, no high-impact local pending events
    -> Show as fresh or with subtle last-updated label

Device comes back online
  -> Always request fresh recommendation immediately
  -> Do not wait for expiry
```

See Section 22 for the UX degradation scale applied to each check.

This is a known and deliberate constraint of the offline-first architecture. It should not be worked around by trying to run AI logic on the device in MVP-0.

### 37.9 Architecture Principles

These principles govern all technical decisions in KitchenOS. They are derived from the company's Operating Principles (`Company/Operating_Principles.md`) and specialise them for the technical layer. When a design choice is unclear, apply these principles before escalating to a discussion or an ADR.

**Offline-first.**
The app must be useful without connectivity. Core flows — pantry browsing, shopping list editing, Cook Mode, meal plan viewing — must work offline. Features that cannot work offline must degrade gracefully with a visible indicator, not fail silently.
*→ Operating Principle 3 (Inspire Confident Action): a product that fails silently when offline erodes user confidence.*

**Event-driven.**
Every meaningful household action produces a domain event written to the append-only `domain_events` table. No meaningful state change happens silently. There are no soft-deletes on domain data — corrections are additional events, not mutations.
*→ Operating Principle 5 (Earn Trust Through Transparency): every state change is traceable, explainable, and reversible. Operating Principle 7 (Truth Before Convenience): corrections over mutations.*

**AI recommends, humans decide.**
The Household Decision Engine produces recommendations. It does not take action autonomously. The user approves, rejects, or ignores every suggestion. No automated action changes household state without user visibility and the ability to reverse it.
*→ Operating Principle 4 (AI Recommends. People Decide.): direct architectural implementation of this principle.*

**Safety before intelligence.**
Allergy and dietary safety checks run before any AI output reaches a user. The Allergy Guard is never bypassed, including for expert recommendations. A safe incorrect suggestion is always preferable to an intelligent unsafe one.
*→ Operating Principle 4 (AI Recommends. People Decide.) and Operating Principle 7 (Truth Before Convenience): an unsafe recommendation that appears certain is the most dangerous form of false certainty.*

**Business rules live in the domain layer.**
Pantry deduction logic, budget calculations, allergy filtering, recommendation scoring, and shopping generation live in domain services — not in controllers, UI components, database triggers, or AI prompts. Business rules must be testable in isolation.
*→ Operating Principle 7 (Truth Before Convenience): rules in the wrong layer are invisible, untestable, and untrustworthy. Operating Principle 5 (Earn Trust Through Transparency): if business logic is buried in prompts, it cannot be audited.*

**Infrastructure is replaceable.**
The AI provider (OpenAI, Gemini), cloud provider (GCP), and database (PostgreSQL) are called through abstraction interfaces. No domain code references a specific provider directly. Swapping infrastructure should not require rewriting domain logic.
*→ Operating Principle 6 (Learn Continuously): the AI model landscape changes; we must be able to adopt better models without architectural surgery. Operating Principle 9 (Simplicity Is a Feature): tight coupling to vendors is hidden complexity.*

**Staleness is explicit.**
The system never silently serves outdated state. Cached recommendations, stale pantry data, and unsynced changes must always be visibly signalled to the user. Implicit staleness is a trust failure.
*→ Operating Principle 7 (Truth Before Convenience): direct implementation. Implicit staleness is the most common way systems fake certainty.*

**Manage, don't self-host.**
In MVP-0, authentication, push notifications, AI models, document understanding, and job queue infrastructure are all managed services. Self-hosting commodity infrastructure is a distraction from building the product.
*→ Operating Principle 9 (Simplicity Is a Feature): absorb infrastructure complexity so we can focus on product complexity.*

### 37.10 Architecture Building Blocks

Building blocks are reusable architectural components that appear across multiple features. Naming them explicitly keeps the architecture coherent as the product grows.

| Building Block | Responsibility | Used By |
|---|---|---|
| **Household Decision Engine** | Turns household context (pantry, goals, allergies, history) into safe, trusted food decisions. Coordinates all AI output. | Home, Cook Mode, Shopping, Meal Planning |
| **Allergy Guard** | Checks all recommendations and expert suggestions against household-level allergy rules. Never bypassed. | Decision Engine, Expert Marketplace, Cook Mode |
| **Sync Engine** | Manages the pending event queue in local SQLite, conflict resolution on reconnect, and online/offline state transitions. | All mobile flows, Offline UX |
| **Household Timeline** | The event log read model. A filtered, human-readable projection of domain events for the user-facing activity history. | Household screen, Home, Corrections |
| **AI Provider Abstraction** | Interface layer over AI providers (OpenAI, Gemini). Domain code never calls a provider directly. Enables provider switching without architectural changes. | Decision Engine, Recipe generation |
| **Document Understanding** | Multimodal LLM extraction (via AI Provider Abstraction) → async Cloud Tasks job → structured proposal with per-field confidence → user confirmation → event write → pantry and budget update. | Receipt scanning flow (ADR-012) |
| **Notification Engine** | Firebase Cloud Messaging delivery of household alerts, recommendation nudges, and sync completion events. | Home, Cook Mode, Shopping, Expert Marketplace |
| **Domain Event Bus** | The `domain_events` append-only table and the write/dispatch logic around it. All domain modules emit events through this; none depend on it for reads. | All domain modules |

These building blocks are not separate deployable services in MVP-0. They are well-defined modules within the modular monolith. They are the natural extraction candidates if the monolith is later broken into microservices — the Household Decision Engine and AI Provider Abstraction are the most likely first candidates.

---

## 37.A Authentication Layer

### Overview

Authentication is a foundation service that gates access to the domain. It operates in a separate schema from household data per ADR-009 (Privacy by Design) and is not part of the domain event log — it is an application-layer concern that precedes domain operations.

**Key design principle:** Identity is never mixed with household domain data. The `identities` schema (email, auth provider, password hash) and the `household_members` schema (person_id, household_id, member type, goals, allergies) are physically separated. The only bridge is `identity_id`, and it is never traversed by domain logic, AI, or the Collective Intelligence pipeline.

### MVP-0 Authentication Design

**Signup Method:**
- Email/password registration
- Social authentication via OAuth 2.0 (Google, Apple)
- Single email per identity; no duplicate signups

**Session Management:**
- Full email/password (or social) re-login is NOT required on every app restart
- Instead: the refresh token (stored in iOS Keychain / Android Keystore) resumes the session, gated by a mandatory biometric/PIN check before any household data is shown — see TA §37.B.3 for the full re-authentication model
- Full re-login is required when: the refresh token has expired (30 days of inactivity), the user explicitly logged out, or the session was revoked (e.g., "Sign Out All Devices")
- This mirrors standard practice for apps handling sensitive-but-not-financial data (see industry research summary in TA §37.B); pure in-memory-token/always-re-login models are reserved for banking-grade apps and were evaluated and rejected for MVP-0 as unnecessary friction
- On logout, session and refresh token are destroyed both locally and server-side; no residual session (see TA §37.B.5)

**Multi-Device Policy:**
- Only one active session per user at a time, across all devices
- New login on Device B immediately invalidates Device A's session (this is a deliberate product decision, not a limitation — see rationale below)
- Device A is notified on next connectivity: "You've been logged out on another device"
- Rationale: Household data is sensitive (allergies, goals, budget); single-session model reduces breach surface per GDR-002 §7 and keeps account control unambiguous per Principle 8 (Stewards, Not Owners). This was evaluated against a multi-device-concurrent alternative and intentionally rejected for MVP-0.

**Password Reset:**
- Email-based reset links only
- Reset link includes one-time token; expires after 30 minutes
- Link is single-use; used reset link is invalid
- No security questions, no SMS, no backup codes in MVP-0
- Rationale: Simplicity per Principle 9; email-based is sufficient for MVP-0

**Account Recovery:**
- Email-based account recovery
- User confirms identity via email link before sensitive operations
- 2FA, backup codes, phone-based recovery deferred to MVP-1
- Rationale: Collect only what we need per GDR-002 §1

### Offline Behavior: Logged In vs. Logged Out

**These are two distinct states with different access levels — they must not be conflated.**

**While logged in, offline (normal operation):** Full read access to cached household data (pantry, meal plans, shopping lists, budget, timeline). Edits are queued locally by the Sync Engine and applied on reconnect. Access to the cache is gated by the biometric/PIN re-authentication timeout (TA §37.B.3), not by network connectivity.

**After explicit logout:** No access to household data, cached or otherwise. Logout is a deliberate security action — it invalidates the session server-side and clears the local encrypted cache (TA §37.B.4, §37.B.5). The user sees only the Sign In screen until they re-authenticate. There is no read-only mode after logout.

**Rationale:** An earlier version of this spec permitted read-only cached access after logout. That was superseded — allowing any access after an explicit "Sign Out" weakens the meaning of sign-out and creates a data-leak risk if the device changes hands. See DOC-072 (Authentication Wireframes), "Offline vs. Logged Out" section, for the UX rationale, and GDR-002 §7 (Breach Containment) for the security basis.

**Implementation:**
```text
User Login
  ↓
Session + refresh token issued → stored in secure device storage
  ↓
Offline, still logged in: cached reads always available; biometric/PIN gate applies per §37.B.3
  ↓
User Logout (explicit)
  ↓
Session revoked server-side; refresh token destroyed
  ↓
Local encrypted cache wiped
  ↓
Sign In screen shown; no data accessible until re-authentication
```

### Data Model (Identity Schema)

```sql
CREATE TABLE identities (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  auth_provider VARCHAR(50) NOT NULL,  -- 'email' | 'google' | 'apple'
  password_hash VARCHAR(255),  -- null for social auth
  email_verified BOOLEAN DEFAULT false,
  email_verified_at TIMESTAMPTZ,
  password_reset_token VARCHAR(255),
  password_reset_expires_at TIMESTAMPTZ,
  last_login_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  
  CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE TABLE identity_sessions (
  id UUID PRIMARY KEY,
  identity_id UUID NOT NULL REFERENCES identities(id) ON DELETE CASCADE,
  device_id VARCHAR(255),  -- device fingerprint
  auth_token_hash VARCHAR(255) NOT NULL,  -- hash of the actual token
  last_activity_at TIMESTAMPTZ NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  
  INDEX idx_identity_active (identity_id, expires_at) WHERE expires_at > NOW()
);
```

**Important:** No household information, no PII beyond email. The `identity_sessions` table is the durable, queryable audit record of sessions in PostgreSQL (used for history, support, and security review). Live session state used for request-time validation lives in Redis, keyed as described in TA §37.B.2 — Redis is the source of truth for "is this session currently valid," while this table is the historical log. It never exposes auth details to domain logic.

### API Contracts (Summary)

| Endpoint | Method | Purpose | Auth Required |
|---|---|---|---|
| `/api/v1/auth/signup` | POST | Email/password or social signup | No |
| `/api/v1/auth/login` | POST | Email/password login | No |
| `/api/v1/auth/refresh` | POST | Exchange refresh token for new access token (rotates refresh token; see §37.B.1) | No (refresh token in body) |
| `/api/v1/auth/revoke` | POST | End session on current device (logout) | Yes |
| `/api/v1/auth/revoke-all` | POST | End all sessions for this identity ("Sign Out All Devices") | Yes |
| `/api/v1/auth/password-reset/request` | POST | Email reset link | No |
| `/api/v1/auth/password-reset/confirm` | POST | Confirm reset with token | No |
| `/api/v1/auth/session/validate` | GET | Check session validity | Yes |

**Full API specification is in `Products/KitchenOS/80_API_Reference/`** (deferred to Stage 5–6).

### Security Considerations for Implementation

1. **Password hashing:** Use bcrypt with cost ≥ 12 (or equivalent like Argon2)
2. **Token generation:** Use cryptographically secure random token generator (≥ 32 bytes)
3. **Email verification:** Verify email on signup before allowing household access
4. **Rate limiting:** Protect password reset and login endpoints against brute force (e.g., max 5 attempts/15 minutes)
5. **HTTPS only:** All auth endpoints require HTTPS; no exceptions
6. **Secure cookie flags:** If using cookies, set Secure + HttpOnly + SameSite=Strict
7. **CORS:** Restrict to trusted domains only; no wildcard origins
8. **Audit logging:** Log all authentication events (login, logout, reset) for security monitoring

### Integration with Domain Layer

**Authentication is a gateway, not a domain concern:**

```text
HTTP Request
  ↓
Auth Middleware
  → Validate session token
  → Extract identity_id
  → Check session expiry
  → (If invalid, return 401)
  ↓
Request Handler (identity_id now available)
  ↓
Domain Service (never receives email or password; only receives identity_id and household_id)
```

**The domain layer never sees:**
- Email addresses
- Password hashes
- Auth provider details
- Session tokens

**The domain layer only receives:**
- `identity_id` (to trace actions to an identity)
- `household_id` (to scope all operations)
- `person_id` (household member record)

This separation is non-negotiable per ADR-009 (Privacy by Design) and ensures a breach of authentication does not expose domain data, and vice versa.

### Deferred to MVP-1+

- Two-factor authentication (2FA)
- Backup codes / account recovery codes
- Phone-based password reset
- Passwordless authentication (WebAuthn/FIDO2)
- Session analytics and security dashboards
- IP-based login anomaly detection
- Device trust management

These are security enhancements that add friction to signup/login; MVP-0 prioritizes simplicity per Principle 9 while maintaining baseline security.

### Related Documents

- ADR-009: Privacy by Design — Identity Isolation
- ADR-014: Session Continuity Model — Single Active Session, Biometric-Gated Resume
- ADR-015: Offline Cache Encryption Strategy — Hardware-Backed Keys via Secure Enclave / Android Keystore
- GDR-002: Privacy by Design — Principles 1, 2, 5, 7
- `Products/KitchenOS/70_UX_Design_System/02_Authentication_Wireframes.md` — UX flows and screens
- `Products/KitchenOS/100_Security/` — Detailed security requirements (post-MVP-0)

---

## 37.B Session Management and Offline Cache Protection

**Scope:** JWT token lifecycle, biometric re-authentication, offline cache encryption, session revocation, and multi-device session handling.

**Dependencies:** TA §37.A (Authentication Layer), ADR-009 (Identity Isolation), ADR-014 (Session Continuity Model), ADR-015 (Offline Cache Encryption Strategy), GDR-002 §7 (Breach Containment).

---

### Overview: Session Lifecycle

A KitchenOS user session spans three states:

```text
┌──────────────────────────────────────────────────────────────┐
│                   SESSION LIFECYCLE                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  LOGIN                                                       │
│  (TA §37.A)                                                  │
│  Email + Password verified                                  │
│       ↓                                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ SESSION CREATED                                      │    │
│  │ • JWT access token (15 min expiry)                  │    │
│  │ • JWT refresh token (30 days expiry)                │    │
│  │ • Session stored in redis (ttl: 30 days)            │    │
│  │ • device_id registered in session metadata          │    │
│  │ • Sync Engine cache: SQLite on device               │    │
│  └─────────────────────────────────────────────────────┘    │
│       ↓                                                       │
│  ACTIVE SESSION                                              │
│  • Access token used for API calls                          │
│  • Background task refreshes access token every 13 min      │
│    (rotates refresh token too; never touches biometric      │
│     trust — §37.B.7)                                        │
│  • Offline: Sync Engine queues mutations locally             │
│       ↓                                                       │
│  BIOMETRIC RE-AUTH REQUIRED (§37.B.3) when:                  │
│  • App backgrounded > 15 min, OR                             │
│  • App process was killed and relaunched (cold start —       │
│    always treated as expired, regardless of elapsed time)   │
│  • On success: biometric_auth_at reset, resume with          │
│    existing/refreshed tokens — no full re-login needed       │
│  • On failure, or refresh token expired/revoked: Sign In     │
│    screen (full re-login required)                          │
│       ↓                                                       │
│  LOGOUT (TA §37.A, Screen 4) — explicit user action           │
│  • Refresh token revoked (POST /api/v1/auth/revoke)          │
│  • Access token invalidated on server                        │
│  • Session deleted from redis                                │
│  • Local SQLite cache wiped                                  │
│  • User returned to Sign In screen                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Note:** The session does not have a fixed "app restart kills it" rule. What kills a session is: explicit logout, "Sign Out All Devices," a new login elsewhere (§37.B.6), refresh token expiry (30-day ceiling, §37.B.10), or refresh-token-reuse detection (§37.B.1). App restart alone only triggers a biometric/PIN re-check, not a session end.

---

### 37.B.1 JWT Token Specification

**Access Token (Short-Lived)**

```json
{
  "iss": "kitchenos-api",
  "sub": "identity_id",
  "person_id": "person-uuid",
  "household_id": "household-uuid",
  "aud": "kitchenos-mobile",
  "exp": 1234567890,
  "iat": 1234567890,
  "nbf": 1234567890,
  "jti": "unique-token-id",
  "device_id": "device-uuid",
  "session_id": "session-redis-key"
}
```

**Spec:**
- **Expiry:** 15 minutes (tight window reduces compromise risk)
- **Encoding:** RS256 (RSA public key verification on client; private key on server)
- **Rotation:** Background task refreshes every 13 minutes (before expiry)
- **Audience:** `kitchenos-mobile` (API validates aud claim)
- **Claims:**
  - `sub`: The standard JWT subject claim — `identity_id` only, per RFC 7519 convention
  - `person_id`, `household_id`: Separate top-level claims (not concatenated into `sub`); each scopes a distinct part of the request
  - `device_id`: Device that issued token; used for session binding
  - `session_id`: Links to redis session record; enables server-side revocation

---

**Refresh Token (Long-Lived)**

```json
{
  "iss": "kitchenos-api",
  "sub": "session_id",
  "type": "refresh",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique-refresh-token-id"
}
```

**Spec:**
- **Expiry:** 30 days
- **Use:** POST /api/v1/auth/refresh to obtain new access token
- **Storage:** Secure storage (iOS Keychain, Android Keystore; never localStorage) — this is what allows the app to resume a session across app restart with only a biometric/PIN gate, per §37.A Session Management
- **Rotation:** Mandatory, not optional. Every refresh issues a new refresh token and immediately invalidates the previous one (`jti` retired). This is required, not a nice-to-have — per OWASP MASVS-AUTH guidance.
- **Reuse detection:** If a retired refresh token (`jti`) is ever presented again, treat it as a stolen-token signal: revoke the entire token family (all tokens descended from that session) and force full re-login. A legitimate client never replays a used refresh token; a replay only happens if a copy was exfiltrated and is being used by an attacker in parallel with the legitimate device.
- **Revocation:** Single endpoint invalidates all refresh tokens for user (see 37.B.2)

---

### 37.B.2 Session Management

**Session Storage (Server-Side)**

```
Service: Redis
Key Format: session:{session_id}
TTL: 30 days (matches refresh token expiry)

Value:
{
  "session_id": "uuid",
  "identity_id": "uuid",
  "person_id": "uuid",
  "household_id": "uuid",
  "device_id": "device-uuid",
  "device_name": "Alice's iPhone",
  "created_at": "2026-07-20T10:00:00Z",
  "last_activity": "2026-07-20T10:15:00Z",
  "biometric_auth_at": "2026-07-20T10:15:00Z",
  "auth_provider": "email|google|apple",
  "refresh_tokens": ["jti-1", "jti-2"],
  "revoked": false
}

Secondary Index (required for lookup by user):
Key Format: sessions_by_identity:{identity_id}
Type: Redis Set
Value: {session_id, session_id, ...}
TTL: none (cleaned up explicitly when sessions are deleted)
```

**Key Design Decisions:**

1. **Device Registration:** Each session is bound to a single device (device_id).

2. **Single Active Session Per User:** New login invalidates all other sessions for that user (across all devices — see §37.A Multi-Device Policy).
   - Lookup uses the secondary index, never a `KEYS` scan: `SMEMBERS sessions_by_identity:{identity_id}` returns the small set of session_ids for that user, then each is fetched and deleted directly (`GET`/`DEL` on `session:{session_id}`).
   - `KEYS session:*` is explicitly disallowed in this codebase — it is an O(n) blocking scan across the entire keyspace and does not scale past a trivial dataset. All session lookups must go through the `sessions_by_identity` index.
   - On session creation: `SADD sessions_by_identity:{identity_id} {session_id}`. On session deletion: `SREM sessions_by_identity:{identity_id} {session_id}`.
   - For atomicity (avoiding races between the index and the session record), session creation and deletion should be wrapped in a Lua script or a `MULTI`/`EXEC` transaction.
   - Consequence: User logs in on phone → any existing session (tablet, previous phone session) ends immediately.
   - This prevents orphaned sessions on lost devices.

3. **Biometric Auth Timestamp:** Track when the user last passed an actual biometric/PIN challenge. This field is updated ONLY on a successful biometric/PIN prompt (§37.B.3) — never by a background token refresh. See §37.B.7 for why this distinction is a hard security boundary, not a convenience.

4. **Last Activity:** Updated on every API call; used for idle timeout (separate from biometric timeout).

---

### 37.B.3 Biometric Re-Authentication

**Hard rule: `biometric_auth_at` is updated ONLY by a successful biometric/PIN prompt.** A background access-token refresh proves the refresh token is valid — it does not prove the person holding the device is the account owner. Conflating the two would mean a stolen, unlocked phone could stay "trusted" indefinitely as long as the app keeps silently refreshing in the background. This is treated as a hard security boundary, not a UX nicety.

**When to Re-Prompt**

```
Scenario 1: App in foreground, token not expired, within 15-min biometric window
  → No re-prompt needed; user is active

Scenario 2: App backgrounded, returns to foreground
  → Check: (now - biometric_auth_at) > 15 minutes?
  → If YES: prompt FaceID/Fingerprint/PIN before showing data
  → If NO: resume transparently

Scenario 3: Background access-token refresh fires (§37.B.7)
  → Refresh happens silently; does NOT touch biometric_auth_at
  → If the 15-min biometric window later expires while token is still valid,
    the next foreground event still triggers a biometric prompt (Scenario 2)

Scenario 4: App fully restarted (process was killed, not just backgrounded)
  → Refresh token read from Keychain/Keystore
  → If refresh token valid: prompt FaceID/Fingerprint/PIN before showing any data
    (biometric_auth_at is treated as expired on cold start, regardless of elapsed time)
  → On success: obtain new access token, set biometric_auth_at = now()
  → If refresh token invalid/expired/revoked: show Sign In screen (full re-login required)

Scenario 5: User switches apps (backgrounding), returns after 20 min
  → Prompt FaceID/Fingerprint
  → On success: update biometric_auth_at = now()
  → Resume with existing tokens (refreshing if needed)
```

**Implementation Flow**

```kotlin
// Pseudo-code (iOS/Kotlin)

AppDelegate.onColdStart() {
  // App process was killed and relaunched — always treat as biometric-expired,
  // regardless of stored biometric_auth_at timestamp
  let refreshToken = SecureStorage.getRefreshToken()

  if refreshToken == null || refreshToken.isExpired {
    showSignInScreen()  // full re-login required
    return
  }

  BiometricPrompt.show(
    title: "Verify identity to access household",
    onSuccess: {
      let accessToken = api.refresh(refreshToken)  // may also rotate refreshToken
      session.biometric_auth_at = now()            // ONLY set here, on actual success
      showHomeScreen()
    },
    onFailure: {
      showSignInScreen()
    }
  )
}

AppDelegate.onWillEnterForeground() {
  // App was merely backgrounded, process stayed alive
  let timeSinceBiometric = now() - session.biometric_auth_at

  if timeSinceBiometric > 15.minutes {
    BiometricPrompt.show(
      title: "Verify identity to access household",
      onSuccess: {
        session.biometric_auth_at = now()  // ONLY set here, on actual success
        showHomeScreen()
      },
      onFailure: {
        showSignInScreen()
      }
    )
  } else {
    // Recent biometric; skip re-prompt
    showHomeScreen()
  }
}

// Background token refresh (§37.B.7) — runs independently, NEVER touches biometric_auth_at
BackgroundTask.onTokenRefresh() {
  api.refresh(refreshToken)
  // no session.biometric_auth_at update here — this is the fix for the
  // "stolen unlocked phone stays trusted forever" issue
}
```

**Rationale (per GDR-002 §7 Breach Containment):**
- If device is stolen/lost while unlocked, the 15-min window limits offline access to cache before a biometric challenge is required
- Cold start (app was killed) always requires a fresh biometric/PIN check before showing data, independent of the 15-min window — this closes the gap where an attacker force-quits and relaunches the app hoping to skip the prompt
- Background token refresh keeps the session alive server-side but never substitutes for proving device possession
- Biometric check is on-device (not server) — works offline
- Balance: usability (not interrupting every few minutes during active use) + security (bounded offline window, no silent trust extension)

---

### 37.B.4 Offline Cache Encryption

**Storage Layer**

```
Database: SQLite on mobile device
Encryption: SQLCipher (AES-256)
Encryption Key: Derived from device passcode + app-level secret

Library: 
  iOS: SQLCipher/ios (via CocoaPods)
  Android: sqlcipher/android (via Gradle)
  Flutter: sqflite + sqlcipher plugin
```

**Key Derivation**

**A key baked into client code or app config is not a secret** — anything shipped in the app binary can be extracted via decompilation or runtime inspection, regardless of encoding or obfuscation. `APP_SECRET`-style constants must not be used as part of the cipher key. The SQLCipher key must instead be generated and held inside the platform's hardware-backed keystore, never fully materialized in application memory or code:

```
// Pseudo-code

// iOS: generate/store key in Secure Enclave, gated by biometric/device passcode
let cipherKey = SecureEnclave.generateOrRetrieveKey(
  tag: "kitchenos.sqlcipher.key",
  accessControl: .biometryCurrentSetOrDevicePasscode,  // requires a device lock to exist
  keySize: 256
)

// Android: generate/store key in Android Keystore, gated by biometric/device credential
let cipherKey = AndroidKeystore.generateOrRetrieveKey(
  alias: "kitchenos_sqlcipher_key",
  requireUserAuthentication: true,
  keySize: 256
)

// Pass to SQLite pragma (key retrieved from keystore at runtime, held only transiently in memory):
// PRAGMA key = "x'{cipherKey}'";
```

**If the device has no passcode/biometric configured:** the hardware keystore cannot gate the key on user authentication. In that case, the app must warn the user explicitly (e.g., "Set a device passcode to protect your household data offline") rather than silently falling back to an ungated key. This is a deliberate degrade-with-warning, not a silent security downgrade.

**Rationale:**
- Encryption at rest (data + DB file encrypted on disk)
- Key generation and storage happen entirely inside the Secure Enclave / Android Keystore hardware boundary; the raw key material never exists in app code, app config, or plaintext on disk
- Key access requires the same biometric/PIN gate as session re-authentication (§37.B.3), tying offline data access to proof of device possession
- SQLCipher is battle-tested (Signal, WhatsApp, and Wire all use variants of this pattern with keystore-backed keys, not embedded secrets)

**Offline-Accessible Data (Cached)**

```
✓ Encrypted & cached:
  • Pantry items (name, quantity, expiry)
  • Meal plan entries
  • Shopping lists
  • Household member names (person_id only, not emails)
  • Budget periods & transactions
  • Household timeline events
  
✗ NOT cached:
  • Identity info (email, auth provider)
  • PII (phone, addresses, payment methods — not in MVP-0 anyway)
  • Settings that require server validation
```

---

### 37.B.5 Session Revocation

**Single Device Logout**

```
POST /api/v1/auth/revoke
Headers: Authorization: Bearer {access_token}
Body: { "device_id": "current-device-id" }

Response:
{
  "revoked": true,
  "message": "Session ended. This device's cache cleared."
}

Server-Side:
1. Delete session record from redis
2. Mark all refresh tokens in session as revoked
3. Return 200 OK
4. Client: wipe SQLite cache, redirect to Sign In
```

**"Sign Out All Devices"**

```
POST /api/v1/auth/revoke-all
Headers: Authorization: Bearer {access_token}
Body: {}

Response:
{
  "sessions_revoked": 3,
  "message": "Signed out on all devices. All sessions ended."
}

Server-Side:
1. Query redis: all sessions for this identity_id
2. Mark each session as revoked: session.revoked = true
3. Mark all refresh tokens across all sessions as revoked
4. TTL those sessions to expire immediately
5. Return count of sessions revoked
6. Each device (on next API call or foreground): detects revocation, clears cache, shows Sign In
```

**Note on Cross-Device Revocation:**
- If User A is offline on phone, then signs out all devices on web
- Phone won't know immediately (no connectivity)
- On phone reconnect: API returns 401 (refresh token revoked)
- Client detects revocation, clears cache, shows Sign In
- Maximum delay: time until next API call or user opens app

---

### 37.B.6 Multi-Device Session Handling

**Policy: Single Active Session Per User, Across All Devices**

This section previously described two contradictory models (single-session in one place, concurrent multi-device sessions in another). The authoritative policy — confirmed and unchanged — is the one stated in TA §37.A: **only one active session per user, period.** A household member can only be signed in on one device at a time.

```
User A logs in on Device 1 (iPhone):
  → Session created, session_id_1
  → sessions_by_identity:{identity_id} = {session_id_1}

User A logs in on Device 2 (iPad):
  → Server looks up sessions_by_identity:{identity_id} → finds session_id_1
  → session_id_1 is revoked (redis DEL + refresh tokens marked revoked)
  → Device 1 is marked for "logged out elsewhere" notification on next connectivity
  → Session created, session_id_2
  → sessions_by_identity:{identity_id} = {session_id_2}

Result: Only session_id_2 (iPad) is active. Device 1 (iPhone), on next
foreground or API call, receives 401, clears its local cache, and shows
"You've been logged out on another device."
```

**Why single-session, not concurrent multi-device (rationale, for completeness):**

The alternative — allowing simultaneous sessions on phone and tablet — is a common and reasonable pattern for many household apps, and was explicitly considered. It was rejected for MVP-0 because:
- It doubles the number of live sessions that must be tracked, revoked, and reasoned about for breach containment (GDR-002 §7)
- It requires an explicit "sign out other devices" UX affordance and cross-device notification model that adds scope to MVP-0
- Single-session keeps "who currently has access to this household's data" a one-line answer, which supports Principle 8 (Stewards, Not Owners) — the account holder always knows exactly where they're logged in

**Household members are not the same as multi-device.** Multiple people in a household each have their own identity, their own login, and their own single session. This policy governs one person using two devices, not two people sharing an account. "Sign Out All Devices" (§37.B.5) remains available as an explicit, user-initiated way to end all sessions for one identity.

**If this policy needs to change** (e.g., user research in MVP-1 shows single-session is a significant friction point for household use), that is a product decision requiring explicit sign-off — not something to silently drift into during implementation, which is what happened in an earlier draft of this document.

---

### 37.B.7 Token Refresh Background Task

**Responsibility:** Keep access token fresh while app is in use.

```
Every 13 minutes (while app is running):
  1. Check: access_token.exp < now() + 2 minutes?
  2. If YES:
     a. POST /api/v1/auth/refresh with refresh_token
     b. Server validates refresh_token (not revoked, not expired)
     c. Server checks for reuse of a retired refresh token jti — if detected,
        revoke the entire token family and force full re-login (§37.B.1)
     d. Server issues new access_token AND new refresh_token (mandatory rotation)
     e. Client stores new access_token and new refresh_token
     f. Do NOT update biometric_auth_at — this refresh proves the refresh
        token is valid, not that the current holder of the device is the
        account owner. Biometric trust is only ever set by §37.B.3.
  3. If NO:
     a. Do nothing; token still has life
     
On Failure (refresh_token invalid/expired/revoked):
  → Redirect to Sign In screen
  → Clear session, clear cache
```

**Why 13 Minutes (vs 15)?**
- Access token expires in 15 minutes
- Refresh at 13 min provides 2-minute safety margin
- If network slow, refresh still completes before expiry
- Avoids "token expired mid-API-call" scenarios

---

### 37.B.8 API Security Headers

Every authenticated request must include:

```
Authorization: Bearer {access_token}
X-Device-ID: {device_id}
Content-Type: application/json
```

**Note:** `session_id` is already carried inside the JWT claims (§37.B.1) — it does not need to be duplicated as a separate `X-Session-ID` header. A prior draft of this spec included both, which is redundant and creates two sources of truth for the same value. `X-Device-ID` is kept as a header (not a claim) because it is validated against the token's `device_id` claim as an integrity check; if a header-only field is ever needed for debugging/tracing, use a clearly-marked `X-Debug-Session-ID` that is stripped in production builds.

**Server Validation:**

```
On every auth-required endpoint:
  1. Extract Authorization header → parse JWT
  2. Verify JWT signature (RS256, public key)
  3. Verify expiry: exp > now()
  4. Verify X-Device-ID header matches device_id claim in JWT
  5. Look up session via session_id claim in JWT; verify session.revoked == false
  6. Verify session.identity_id matches token subject (sub claim)
  
If any check fails:
  → Return 401 Unauthorized
  → Client clears session, redirects to Sign In
```

---

### 37.B.9 Edge Cases & Recovery

**Case 1: Access Token Expires During API Call**

```
Client makes request with valid access_token
Server receives request, token is valid ✓
Server processes request (takes 5 seconds)
Server tries to issue response → checks token again
Token expired (unlucky timing)

Solution:
  • Client: detect 401 in response
  • Trigger refresh: POST /auth/refresh
  • Retry original request with new token
  • (Transparent to user)
```

**Case 2: Refresh Token Expired**

```
User phone offline for 31+ days
Comes back online, tries to use app
Refresh endpoint returns 401: "Refresh token expired"

Solution:
  • Clear session, cache
  • Redirect to Sign In
  • User re-authenticates (standard login flow)
```

**Case 3: Device Lost, User Signs Out All Devices**

```
User realizes iPhone is missing
Logs into web dashboard (or calls support)
Signs out on all devices

On lost iPhone (when/if it reconnects):
  • Background sync attempts: 401 (refresh token revoked)
  • Next API call: detects revocation
  • Clears SQLite cache
  • Shows Sign In screen (no sensitive data exposed)
```

**Case 4: User Logs In on New Device While Old Device Still Has a Session**

```
User logs in on Device 2 (new phone)
Device 1 (old phone) still holds a session

Behavior (per §37.A single-session policy, §37.B.6):
  • Device 1's session is revoked immediately as part of Device 2's login
  • Device 1, on next foreground or API call, receives 401
  • Device 1 clears its local cache and shows "You've been logged out on another device"
  • Device 2 is now the sole active session

Rationale:
  • Matches the single-session-per-user policy (§37.A) — there is no
    "gradual migration" window where both devices are trusted
  • If a user is intentionally migrating devices, the old device simply
    needs to be signed back in if they want to keep using it, which will
    in turn end the new device's session — the policy is symmetric
```

**Case 5: App Restarted (Process Killed) with a Valid Refresh Token**

```
User force-quits the app or the OS kills it in the background
User reopens the app

Behavior (per §37.A Session Management, §37.B.3 Scenario 4):
  • Refresh token read from Keychain/Keystore
  • biometric_auth_at is treated as expired on cold start, regardless of
    how much time actually elapsed
  • Biometric/PIN prompt is shown before any household data renders
  • On success: new access token obtained, biometric_auth_at set to now()
  • On failure or no biometric available: Sign In screen shown

This is NOT the same as "sessions don't persist across restart" in the
literal sense — the refresh token does persist and is used. What does NOT
persist is standing access to data without re-proving device possession.
```

---

### 37.B.10 Related Decisions & Deferred Features

**Absolute Session Ceiling:** Regardless of activity, a refresh token is hard-capped at 30 days (§37.B.1). This is the system's backstop against indefinite session life, per OWASP MASVS guidance to force full re-authentication after a fixed window even for continuously-active sessions. No design in this spec allows a session to outlive 30 days without a full email/password (or social) re-login.

**Deferred to MVP-1+:**

- Session analytics (time-to-refresh, revocation patterns)
- Concurrent session limit (e.g., max 3 devices per user) — only relevant if the multi-device policy in §37.B.6 is revisited
- Device trust / "Remember this device" option
- Device fingerprinting (to detect suspicious logins)
- Passwordless auth (WebAuthn / FIDO2 registration after login)
- Two-factor authentication
- SSL/TLS certificate pinning (recommended before handling any financial account linking or payment features; not required for MVP-0's record-and-display-only budget scope per Vision §60)

---

### Related Documents

- TA §37.A: Authentication Layer (signup, signin, password reset)
- ADR-009: Identity Isolation — session must not leak identity into domain layer
- ADR-014: Session Continuity Model — authoritative record of the single-session and biometric-gated-resume policies specified in this section
- ADR-015: Offline Cache Encryption Strategy — authoritative record of the SQLCipher + hardware-backed key approach specified in §37.B.4
- GDR-002 §7: Breach Containment — revocation prevents spread if device compromised
- DOC-072: Authentication Wireframes (Session lifecycle visual)
- `100_Security/`: Detailed threat modeling and incident response

---

---

## 41. MVP Architecture Simplification

The full architecture is event-driven, graph-based, and AI-orchestrated.

For MVP-0, simplify implementation to:

```text
Mobile SQLite DB
  -> REST API
  -> PostgreSQL primary tables
  -> append-only domain_events table
  -> simple materialized household state views
  -> basic Household Timeline read model
```

Events are still the source of truth for meaningful household actions, but MVP-0 does not need full event replay infrastructure, a distributed event bus, complex projections, or a perfect knowledge graph. The pragmatic rule is to store domain events from day one while keeping read models simple.

---

