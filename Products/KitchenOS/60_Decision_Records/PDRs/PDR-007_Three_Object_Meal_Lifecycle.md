---
id: PDR-007
title: Three-Object Meal Lifecycle — MealRecommendation, MealPlan, MealSession
type: pdr
status: accepted
owner: product
depends_on: [PDR-001, PDR-002, PDR-005, ADR-010]
referenced_by: []
tags: [meal-lifecycle, meal-recommendation, meal-plan, meal-session, ai-design, progressive-disclosure, pantry, product-philosophy]
date: 2026
---

# PDR-007: Three-Object Meal Lifecycle — MealRecommendation, MealPlan, MealSession

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026
**Deciders:** Founding team
**Stage Gate:** Stage 3 — Product Definition

---

## Context

KitchenOS needs to model the meal planning and cooking journey — from AI suggestion to pantry deduction — in a way that:

- Does not make irreversible changes (pantry deductions) too early in the journey.
- Respects user agency: the user controls when a suggestion becomes a commitment.
- Allows the AI to generate suggestions freely without side effects.
- Preserves a clear audit trail for corrections, reversals, and trust.

The naive approach is a single "meal plan" object that covers all three stages: suggestion, commitment, and execution. This conflates three fundamentally different states:

1. **"Here is an idea."** — No commitment. No pantry effect.
2. **"I intend to cook this."** — Commitment to a plan. Still no pantry effect.
3. **"I cooked this."** — Execution. Pantry deduction happens here.

Mixing these states into one object creates: incorrect pantry deductions (planning without cooking), unclear reversal semantics, and AI suggestions that feel like commitments before the user agrees.

---

## Decision

**We will model the meal journey as three distinct objects with separate lifecycles: `MealRecommendation` (ephemeral AI output), `MealPlan` (user intention), and `MealSession` (execution reality).**

---

## Reasons

- **Pantry correctness**: deductions happen only on `MealSession` confirmation. A planned meal that is never cooked never removes ingredients.
- **User agency**: each transition (recommendation → plan, plan → session) is an explicit user action. Nothing is assumed.
- **AI freedom**: the recommendation engine can generate, rank, and discard `MealRecommendation` objects freely. They are ephemeral — no domain state is created until the user accepts one.
- **Reversal clarity**: each object type has unambiguous reversal semantics. A `MealRecommendation` is simply dismissed. A `MealPlan` is cancelled (`MealPlanCancelled` event). A `MealSession` is reversed (`MealSessionReversed` event with pantry restoration).
- **Progressive disclosure**: the UI presents only the information relevant to the current stage. The user is not shown execution options before they have committed to a plan.
- **Audit trail**: the three objects form a traceable chain. Given any pantry deduction, the system can trace back: which `MealSession` caused it, which `MealPlan` it executed, and which `MealRecommendation` originated it.

---

## Alternatives Considered

### Option A: Single `MealPlan` object with status transitions

One object moves through states: `suggested → planned → in_progress → completed`.

Rejected because: pantry deduction timing becomes ambiguous (which status triggers it?). Reversal semantics are unclear for intermediate states. The AI cannot generate suggestions freely — every suggestion creates a domain object.

### Option B: `MealPlan` + `MealSession` (no separate Recommendation)

AI suggestions are immediately `MealPlan` objects with a `source: ai_suggestion` flag. The user promotes or dismisses them.

Rejected because: this creates domain state for every AI suggestion, including those the user never sees or immediately dismisses. It pollutes the event log and makes pantry derivation rules more complex.

### Option C: Three objects (chosen)

`MealRecommendation` is ephemeral and lives outside the domain event log. `MealPlan` is an intention with a domain event. `MealSession` is execution with pantry effects.

Each object has a single, clear responsibility. This is the chosen approach.

---

## Consequences

### Positive

- Pantry state is always accurate — no phantom deductions from planned-but-not-cooked meals.
- The AI can generate high volumes of recommendations without polluting the domain event log.
- Reversals and corrections are straightforward — each object type has a single reversal event.
- Confidence-based questioning becomes natural: the AI only asks for confirmation when it is uncertain, and the three-stage structure gives it natural checkpoints to do so.

### Negative

- Three domain objects to understand and model instead of one.
- The transition events (`MealRecommendationAccepted`, `MealPlanConfirmed`, `MealSessionCompleted`) must all be tracked for the Household Timeline to tell a coherent story.
- `MealRecommendation` is ephemeral but its acceptance must produce a domain event to link the chain. This requires careful event design.

### Scope Boundary

- This decision covers the meal planning and cooking lifecycle only.
- The shopping lifecycle (ShoppingList → ShoppingTrip → pantry additions) is governed by ADR-010 and follows the same principle: pantry additions only on confirmed `ShoppingTrip`.
- `WeeklyMealPlan` as a higher-level planning horizon is a separate decision — see PDR-008.

---

## Related

- `Products/KitchenOS/10_Product_Vision.md`, Section 8.13 — AI predicts the routine, asks only about exceptions
- `Products/KitchenOS/20_Domain_Model.md` — MealRecommendation, MealPlan, MealSession aggregate roots
- `Knowledge/60_Decision_Records/ADR-010_Pantry_Derived_From_Confirmed_Activities.md` — pantry lifecycle rules
- PDR-005 — Ask only what the AI cannot reasonably learn on its own
- PDR-008 — WeeklyMealPlan as planning horizon
