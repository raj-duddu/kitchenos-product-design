---
id: DOC-050
title: KitchenOS Engineering Handbook
type: engineering-handbook
status: active
owner: engineering
depends_on: [DOC-040, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006]
referenced_by: []
tags: [engineering, testing, ci-cd, tdd, bdd, ddd, quality, testcontainers, flutter-test, jest]
date: 2026
---

# KitchenOS: Engineering Handbook

> This document is the authoritative source for how the KitchenOS engineering team works: MVP tech stack, testing philosophy, coverage targets, CI/CD pipeline, and engineering principles. Architecture decisions live in `40_Technical_Architecture.md` and `60_Decision_Records/ADRs/`.

---

## 42. MVP-0 Tech Stack

### 42.1 Mobile

- Flutter.
- SQLite with Drift.
- Riverpod.
- Firebase Authentication (Flutter SDK).
- Firebase Cloud Messaging (push notifications).

### 42.2 Backend

- Node.js with NestJS.
- Cloud Run (serverless container deployment).
- Cloud SQL PostgreSQL with Cloud SQL Proxy.

### 42.3 AI

- OpenAI API or Gemini API for recipe generation and simple suggestions, called through an abstraction interface.
- Cloud Vision API for receipt OCR.
- No full orchestration layer in MVP-0.

### 42.4 Storage

- Cloud Storage for receipt images and attachments.
- Cloud Tasks for async OCR job queue.
- Secret Manager for all API keys and credentials.

See Section 37.6 for the full cloud infrastructure architecture and service map.
See Section 42.5 for engineering quality tooling, testing strategy, and CI/CD pipeline.

---

## 42.5 Engineering Quality

Quality is part of the architecture, not an afterthought. KitchenOS has complex business rules — allergy safety, pantry event sourcing, AI recommendations, offline sync, and multi-device conflict resolution — that break in subtle ways without automated testing.

### Testing Philosophy

> Test business decisions, not implementation details.

Do not test whether a private method was called. Test outcomes users and the household depend on:

- Did the pantry update correctly after cooking?
- Was an unsafe ingredient blocked before reaching the user?
- Did undo restore the previous household state?
- Was the shopping list regenerated correctly?
- Was the recommendation appropriate for the user's goals and allergies?

These are stable, product-defining behaviours. Tests centred on them remain valuable even as internal implementation evolves.

### Testing Stack

| Area | Tool | Notes |
|---|---|---|
| Backend unit tests | Jest | Built into NestJS. Fast. No server required. |
| Backend integration tests | Jest + Testcontainers | Runs tests against a real PostgreSQL Docker container. No mocks. |
| API contract tests | Supertest | Tests REST endpoints directly against the running NestJS app. |
| Flutter unit tests | flutter_test | Pure Dart logic. No UI. Very fast. |
| Flutter widget tests | flutter_test | Tests UI components without launching a device. |
| Flutter integration tests | Integration Test package | Full app flows on a simulator or device. |
| Static analysis | Dart Analyzer + ESLint + Prettier | Catches errors and enforces style before tests run. |
| Code coverage | lcov | Standard coverage reporting. |

### Why Testcontainers is Required for KitchenOS

The `domain_events` append-only table, materialized household state views, reversal events, and Household Timeline read model all depend on real PostgreSQL behaviour. Mocking the database will not catch constraint violations, view update failures, or event ordering bugs. Every integration test must run against a clean real Postgres instance via Testcontainers.

### Coverage Targets

- **Business logic and domain services:** 80–90% minimum.
- **Safety-critical paths (allergy rejection, unsafe recommendation block):** 100%. No exceptions.
- **Controllers and UI glue code:** lower coverage is acceptable.

### KitchenOS-Specific Test Priorities

**Event sourcing integrity:**

```text
Command issued
  -> Correct event written to domain_events
  -> Correct fields, aggregate_id, envelope
  -> Materialized household state view updated
  -> Household Timeline read model updated

Reversal issued
  -> Reversal event written, not a delete
  -> Read model reflects reversal
  -> AI learning excluded for reversed events
```

**Safety-critical paths:**

```text
Ingredient contains allergen
  -> Recommendation rejected before reaching user
  -> No partial pass-through

Multiple members, different allergies, same meal
  -> Household-level safety aggregation applied
  -> Meal blocked if any selected eater is at risk

Expert recommendation received
  -> KitchenOS safety check applied before user sees it
  -> Blocked if unsafe
```

**Offline sync and conflict resolution:**

```text
Device A offline: pending events queued in SQLite
Device B online: syncs conflicting events
Device A reconnects: pending events flush
  -> Correct merge in Cloud SQL
  -> No duplicate domain_events
  -> Household state converges correctly
```

**AI prompt builder:**

```text
Context pack generated for recommendation
  -> Includes household allergies
  -> Includes individual goals
  -> Includes current pantry state
  -> Includes recent household history
  -> AI provider is mocked in tests
  -> No external API calls in test suite
```

### CI/CD Pipeline

```text
Developer pushes code
        │
        ▼
  GitHub Actions
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Lint  Unit   Widget
      Tests   Tests
        │
        ▼
Backend Integration Tests
(Testcontainers + real PostgreSQL)
        │
        ▼
Safety Regression Gate
(allergy rejection, unsafe recommendation block)
        │
        ▼
Build Flutter App
        │
        ▼
Build Docker Image
        │
        ▼
Deploy to Staging (Cloud Run)
        │
        ▼
Smoke Tests
        │
        ▼
Manual Approval
        │
        ▼
Production
```

The Safety Regression gate must never be skipped, including for hotfixes.

No code merges unless the full pipeline passes.

### What Not to Test

- Do not unit test the LLM response. Mock the AI provider and test the prompt builder and context pack instead.
- Do not test implementation details or private method calls. Test observable outcomes only.
- Do not aim for 100% coverage everywhere. Focus coverage investment on the decision engine, safety paths, and event sourcing flows.

### Engineering Principles

Five principles that govern how KitchenOS code is written, tested, and shipped:

**Principle 1: Behavior First**
Every feature begins with expected user behavior before any implementation starts. Write the scenario first. Code second.

**Principle 2: Business Logic is Tested**
Critical business rules — pantry deduction, budget logic, allergy filtering, shopping generation, recommendation scoring — must have automated unit tests. No exceptions.

**Principle 3: Integration Before Release**
All critical user workflows must have automated integration tests that run against real infrastructure before code reaches staging.

**Principle 4: Decisions Are Verifiable**
Every recommendation produced by the Household Decision Engine must be testable in isolation. If you cannot write a test that asserts a recommendation is correct or incorrect, the decision logic is not well-defined enough to ship.

**Principle 5: Events Are Observable**
All major household events must be testable independently of the UI. The event chain is the product. Test it directly.

### TDD, BDD, and When to Apply Each

Do not adopt either as dogma. Apply each where it provides clear value.

**Decision guide:**

```text
Is this deterministic business logic?
  Yes -> Apply TDD
  Examples: pantry deduction, budget calculation, shopping generation,
            allergy filtering, recommendation scoring, event processing,
            sync conflict resolution, undo logic

Is this a user-facing decision the product makes on behalf of the household?
  Yes -> Apply BDD (Given / When / Then)
  Examples: allergy rejection, pantry-based recommendation,
            budget-aware meal suggestion, correction reversal,
            offline staleness evaluation

Is this UI layout, animation, or visual polish?
  Yes -> Exempt from TDD. Use widget tests for interactions only.
  Examples: Cook Mode step transitions, Home screen card layout,
            Household Timeline scroll behaviour

Is this an AI prompt or exploratory UX?
  Yes -> Exempt from TDD. Test the prompt builder, not the LLM output.
  Examples: recipe generation prompt, recommendation context pack
```

### BDD Scenario Format for KitchenOS

Because KitchenOS is event-driven, the standard Given / When / Then format maps directly to household state + domain event + expected outcome. Use this format for every significant product decision.

**Template:**

```text
Given:  [Current household state]
When:   [A domain event occurs]
Then:   [Expected household state]
And:    [Expected recommendation or Timeline entry]
```

**Example 1 — Pantry deduction after cooking:**

```text
Given:  Milk quantity = 1, Eggs quantity = 3
When:   Breakfast cooked (uses 1 milk, 2 eggs)
Then:   Milk quantity = 0, Eggs quantity = 1
And:    Shopping recommendation: Add Milk
And:    Household Timeline: "Breakfast cooked — pantry updated"
```

**Example 2 — Allergy rejection:**

```text
Given:  Child profile has peanut allergy (severity: critical)
When:   Recipe recommendation is generated for household dinner
Then:   Any recipe containing peanuts or peanut derivatives is excluded
And:    No partial pass-through for sub-ingredients
And:    Household Timeline: no blocked recipe appears in suggestions
```

**Example 3 — Budget-aware recommendation:**

```text
Given:  Weekly budget is exceeded by 15%
When:   Dinner recommendations are generated
Then:   Premium ingredients are not recommended
And:    Lower-cost alternatives for the same meal type are preferred
```

**Example 4 — Duplicate receipt rejection:**

```text
Given:  Receipt from Whole Foods on Monday at 9:14am already imported
When:   Same receipt is scanned again (same store, date, OCR hash match)
Then:   Receipt is flagged as duplicate, not imported
And:    Pantry is not updated again
And:    Household Timeline: "Duplicate receipt detected and skipped"
```

**Example 5 — Offline staleness:**

```text
Given:  recommendation_expires_at is in the past
When:   User opens Home screen while offline
Then:   Cached recommendation is suppressed
And:    Empty state shown with prompt to reconnect
```

These BDD scenarios serve three purposes simultaneously: product requirement, QA test case, and automated test specification. Write them before implementation, not after.

### Event-Driven Integration Testing

For KitchenOS, integration tests should verify the full event chain, not just individual API responses. Testing whether an endpoint returns 200 is not enough — test that the correct events were written and the correct state was produced.

**Pattern:**

```text
1. Set up initial household state in test database
2. Issue a command (POST /events or equivalent)
3. Assert: correct event written to domain_events
4. Assert: correct fields, aggregate_id, event_type in event envelope
5. Assert: materialized household state view updated correctly
6. Assert: Household Timeline read model updated correctly
7. Assert: recommendation or notification triggered if expected
```

**Example — Receipt scan chain:**

```text
Command: ReceiptScanRequested

Verify event chain:
  ReceiptImported written to domain_events ✓
  PantryUpdated written to domain_events ✓
    -> pantry table reflects new quantities ✓
  BudgetUpdated written to domain_events ✓
    -> budget summary reflects receipt total ✓
  RecommendationGenerated written to domain_events ✓
    -> recommendation references updated pantry state ✓
  HouseholdTimelineUpdated ✓
    -> Timeline entry: "Receipt from [Store] imported"
```

This pattern is more valuable than unit tests alone because it proves the entire product behaviour works end to end, not just individual pieces in isolation.

### Domain-Driven Design (DDD) Connection

KitchenOS already has DDD embedded in its architecture through Section 32. This is intentional and important for long-term maintainability.

DDD is not a testing methodology. It is the architectural discipline that keeps complexity organised as the product grows. Engineers should understand that the domain-driven event architecture in Section 32 is applying DDD concepts directly:

| DDD Concept | KitchenOS Implementation |
|---|---|
| Bounded contexts | Pantry domain, Shopping domain, Cooking domain, Household domain, AI/Recommendation domain, Expert Marketplace domain |
| Aggregates | Household (root aggregate), Recipe, PantryItem, ShoppingList |
| Domain events | ReceiptScanned, MealCooked, PantryItemConsumed, CorrectionIssued, RecommendationGenerated |
| Ubiquitous language | Household Timeline, Household Decision Engine, Cook Mode, Allergy Guard, Correction Event |
| Value objects | Ingredient, Portion, AllergyRule, GoalType |

The ubiquitous language is critical. Engineers, product managers, and QA should all use the same terms. If an engineer says "the food list" and a product manager says "the pantry", that is a terminology mismatch that will eventually cause a specification bug. Section 32 defines the canonical language. Use it consistently in code, tests, tickets, and documentation.

BDD and TDD ensure the behaviours defined by the domain model remain correct as the codebase evolves. DDD ensures the domain model itself stays coherent as features are added.

---

## 42.6 AI-Native Documentation Principle

> **Agents contain behavior, not policy. Policies belong to the knowledge system.**

This is the foundational rule for how documentation is structured in an AI-native organisation.

**What it means:**

- Governance rules (when to write an ADR, who approves, what is required) live in governance documents under `Company/Governance/`. They do not live inside agent definitions.
- Agent documents (`Agents/Architect.md`, `Agents/Product_Manager.md`, etc.) define *how the agent behaves* — its responsibilities, inputs, outputs, escalation rules, and which governance documents to consult.
- An agent enforces policy. It does not own it.

**Why this matters:**

If governance rules were stored inside agent definitions, adding a second agent (Security Architect, Platform Architect, Senior Engineer) would require duplicating or cross-referencing the same rules. As the team — human or AI — grows, this creates fragmented, contradictory, and unmaintainable governance.

With policy in the knowledge system:

```text
Company/Governance/Architecture_Governance.md
        │
        ├── referenced by → Agents/Architect.md
        ├── referenced by → Agents/Engineering_Manager.md
        ├── referenced by → future Security Architect Agent
        ├── referenced by → human engineers
        └── referenced by → Architecture_Review_Checklist.md
```

One document. One source of truth. Every actor references it.

**The legal system analogy:**

The law is not stored inside the police officer. The law exists independently. Police enforce it. Judges interpret it. Citizens follow it. This is how knowledge systems scale — and it applies equally to human teams and AI agent teams.

**In practice:**

When writing a new agent definition, ask: *"Am I defining behavior, or am I defining policy?"*

- If behavior → write it in `Agents/[AgentName].md`.
- If policy → write it in `Company/Governance/` and reference it from the agent.

---

