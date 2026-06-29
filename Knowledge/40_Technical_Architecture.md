---
id: DOC-040
title: KitchenOS Technical Architecture
type: architecture
status: active
owner: architecture
depends_on: [DOC-020, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006]
referenced_by: [DOC-050]
tags: [architecture, backend, ai, event-sourcing, offline, technology-stack, ddd, household-decision-engine, building-blocks]
date: 2026
---

# KitchenOS: Technical Architecture

> This document is the authoritative source for how KitchenOS is built: the AI architecture, backend design, event sourcing model, offline strategy, technology stack, architecture principles, and building blocks. Product decisions live in `10_Product_Vision.md`. Domain entity definitions live in `20_Domain_Model.md`. Specific technology choices are recorded in `60_ADRs/`.

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

- OCR extraction.
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
  -> scanning, OCR, item extraction, duplicate detection, reversal

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

- OCR ingestion.
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
- Google Cloud Vision API is best-in-class for receipt and document OCR, which is a core MVP-0 feature.
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
 ├── Cloud Vision API (receipt OCR)
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
| Receipt OCR | Cloud Vision API | Best-in-class document and receipt text extraction. |
| Authentication | Firebase Authentication | Email, Google, Apple Sign-In. Native Flutter SDK. |
| Push Notifications | Firebase Cloud Messaging | Android and iOS notifications from a single API. |
| Secrets | Secret Manager | API keys and credentials. Never hardcoded. |
| CI/CD | GitHub Actions + Cloud Build | Automated builds, tests, and deployments. |
| Monitoring | Cloud Logging + Cloud Error Reporting + Sentry | Crash tracking and production visibility. |
| Job Queue | Cloud Tasks | Async receipt OCR processing. Add from MVP-0. |

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

These principles govern all technical decisions in KitchenOS. When a design choice is unclear, apply these principles before escalating to a discussion or an ADR.

**Offline-first.**
The app must be useful without connectivity. Core flows — pantry browsing, shopping list editing, Cook Mode, meal plan viewing — must work offline. Features that cannot work offline must degrade gracefully with a visible indicator, not fail silently.

**Event-driven.**
Every meaningful household action produces a domain event written to the append-only `domain_events` table. No meaningful state change happens silently. There are no soft-deletes on domain data — corrections are additional events, not mutations.

**AI recommends, humans decide.**
The Household Decision Engine produces recommendations. It does not take action autonomously. The user approves, rejects, or ignores every suggestion. No automated action changes household state without user visibility and the ability to reverse it.

**Safety before intelligence.**
Allergy and dietary safety checks run before any AI output reaches a user. The Allergy Guard is never bypassed, including for expert recommendations. A safe incorrect suggestion is always preferable to an intelligent unsafe one.

**Business rules live in the domain layer.**
Pantry deduction logic, budget calculations, allergy filtering, recommendation scoring, and shopping generation live in domain services — not in controllers, UI components, database triggers, or AI prompts. Business rules must be testable in isolation.

**Infrastructure is replaceable.**
The AI provider (OpenAI, Gemini), cloud provider (GCP), and database (PostgreSQL) are called through abstraction interfaces. No domain code references a specific provider directly. Swapping infrastructure should not require rewriting domain logic.

**Staleness is explicit.**
The system never silently serves outdated state. Cached recommendations, stale pantry data, and unsynced changes must always be visibly signalled to the user. Implicit staleness is a trust failure.

**Manage, don't self-host.**
In MVP-0, authentication, push notifications, AI models, OCR, and job queue infrastructure are all managed services. Self-hosting commodity infrastructure is a distraction from building the product.

### 37.10 Architecture Building Blocks

Building blocks are reusable architectural components that appear across multiple features. Naming them explicitly keeps the architecture coherent as the product grows.

| Building Block | Responsibility | Used By |
|---|---|---|
| **Household Decision Engine** | Turns household context (pantry, goals, allergies, history) into safe, trusted food decisions. Coordinates all AI output. | Home, Cook Mode, Shopping, Meal Planning |
| **Allergy Guard** | Checks all recommendations and expert suggestions against household-level allergy rules. Never bypassed. | Decision Engine, Expert Marketplace, Cook Mode |
| **Sync Engine** | Manages the pending event queue in local SQLite, conflict resolution on reconnect, and online/offline state transitions. | All mobile flows, Offline UX |
| **Household Timeline** | The event log read model. A filtered, human-readable projection of domain events for the user-facing activity history. | Household screen, Home, Corrections |
| **AI Provider Abstraction** | Interface layer over AI providers (OpenAI, Gemini). Domain code never calls a provider directly. Enables provider switching without architectural changes. | Decision Engine, Recipe generation |
| **Receipt OCR Pipeline** | Cloud Vision API call → async Cloud Tasks job → pantry update chain → event write → budget update. | Receipt scanning flow |
| **Notification Engine** | Firebase Cloud Messaging delivery of household alerts, recommendation nudges, and sync completion events. | Home, Cook Mode, Shopping, Expert Marketplace |
| **Domain Event Bus** | The `domain_events` append-only table and the write/dispatch logic around it. All domain modules emit events through this; none depend on it for reads. | All domain modules |

These building blocks are not separate deployable services in MVP-0. They are well-defined modules within the modular monolith. They are the natural extraction candidates if the monolith is later broken into microservices — the Household Decision Engine and AI Provider Abstraction are the most likely first candidates.

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

