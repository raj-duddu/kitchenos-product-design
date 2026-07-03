---
id: PDR-008
title: WeeklyMealPlan as Planning Horizon — AI Predicts the Routine, Asks Only About Exceptions
type: pdr
status: accepted
owner: product
depends_on: [PDR-002, PDR-005, PDR-007, ADR-010]
referenced_by: []
tags: [weekly-meal-plan, planning-horizon, household-schedule-model, ai-design, closed-loop, product-philosophy, meal-lifecycle]
date: 2026
---

# PDR-008: WeeklyMealPlan as Planning Horizon — AI Predicts the Routine, Asks Only About Exceptions

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026
**Deciders:** Founding team
**Stage Gate:** Stage 3 — Product Definition

---

## Context

PDR-007 established the three-object meal lifecycle: `MealRecommendation → MealPlan → MealSession`. This covers individual meal decisions well. But households don't plan one meal at a time — they think in weeks.

The question is: **what is the right model for weekly meal planning?**

Two failure modes to avoid:

1. **Too much friction**: asking the household to plan every meal slot for the week, every week. This is the recipe app experience — 20 minutes of manual selection that most users abandon.
2. **Too little structure**: generating recommendations on demand per meal, with no weekly view. This loses the planning benefits: shopping list generation, budget forecasting, and expiry-aware scheduling.

The insight from household behaviour research: most households have **a predictable weekly routine with occasional exceptions**. Monday is pasta night. Tuesday is leftovers. Wednesday the kids have football so it's something quick. Friday is takeaway. The AI should learn this routine and generate the week's plan automatically — surfacing only the slots it's uncertain about for the user to confirm.

The goal stated in Product Vision Section 8.14: **"Weekly meal planning in under 2 minutes."**

---

## Decision

**We will model `WeeklyMealPlan` as a planning horizon — a time-scoped grouping of `MealPlan` items for a household week — and the AI will generate a full draft week automatically, surfacing only exceptions and low-confidence slots for user confirmation.**

The `WeeklyMealPlan` is accepted in a single user action. Planning is a review-and-confirm experience, not a build-from-scratch experience.

---

## Reasons

- **Effort reduction is the core value proposition.** If the user has to plan every meal every week, KitchenOS is not saving effort — it is repackaging effort. The AI must absorb the routine planning work.
- **The Household Schedule Model enables this.** The intelligence layer learns typical participants per slot per day of week, absence patterns, takeout nights, and guest frequency. This is precisely the data needed to auto-generate a week's draft. See `40_Technical_Architecture.md`, Household Schedule Model.
- **Weekly view unlocks downstream features.** A committed `WeeklyMealPlan` drives: shopping list generation for the week, budget forecasting, expiry-aware meal slot ordering (use the chicken before it expires → plan it Thursday not Saturday).
- **Closed-loop system**: `WeeklyMealPlan accepted → MealPlans created → MealSessions executed → events feed Schedule Model → next week's draft is more accurate`. The system improves with use.
- **"Planning horizon" is the right mental model.** `WeeklyMealPlan` owns no business rules of its own beyond time-scoping. It is a container for `MealPlan` items. Its invariants are thin: one per household per week, atomic acceptance. It is not a thick aggregate with complex lifecycle management.

---

## Alternatives Considered

### Option A: Per-meal planning only (no WeeklyMealPlan)

The user plans meals individually on demand. No weekly view.

Rejected because: loses shopping list generation accuracy, budget forecasting, and expiry-aware scheduling. More importantly, it maximises user effort — every meal is a separate decision. The AI cannot amortise the routine across a week.

### Option B: WeeklyMealPlan as a thick aggregate (user-built)

The user constructs the weekly plan slot by slot, dragging recipes into a calendar.

Rejected because: this is a meal planning app experience, not a food intelligence experience. It puts the cognitive load entirely on the user. The AI's role becomes decoration rather than substance.

### Option C: WeeklyMealPlan as AI-generated draft, user reviews exceptions (chosen)

The AI generates the full week. The user sees the draft, confirms confident slots, and adjusts the exceptions. Accepted in one action.

This is the chosen approach. It inverts the default: the AI does the work; the user approves or corrects.

---

## Consequences

### Positive

- Weekly planning in under 2 minutes is achievable because the user is reviewing, not building.
- Shopping list generation becomes accurate and automatic — it derives from the accepted `WeeklyMealPlan`.
- Budget forecasting becomes feasible — a committed week of meals has a predictable grocery cost.
- Expiry-aware scheduling is possible — the AI orders meal slots to consume near-expiry items first.
- The system improves with every week of use — the Schedule Model learns the household's routine progressively.

### Negative

- The Household Schedule Model must be built and maintained in the intelligence layer. Cold-start quality will be low for new households — the first few weeks will show more low-confidence slots requiring confirmation.
- Mid-week plan changes (a MealPlan swap within the week) must propagate correctly: shopping list deltas, budget updates, pantry reservation changes. This is non-trivial event choreography.
- The AI must handle the case where it has very little data gracefully — defaulting to a higher-friction but honest experience ("We're still learning your routine — here are some suggestions to start with") rather than generating a low-quality week silently.

### Scope Boundary

- `WeeklyMealPlan` acceptance does not update pantry, shopping list, or budget directly. These are derived downstream when `MealSessions` are confirmed and `ShoppingTrips` are completed. See ADR-010.
- `WeeklyMealPlan` is modelled as an Aggregate Root in Version 1 for clarity. In a future version it should be reconsidered as a thin `planning_horizon` (week_start + household_id FK) with MealPlans referencing it — as noted in the Domain Model design note.
- This PDR covers household-level weekly planning. Individual meal customisation (portions, substitutions, member-specific variants) is a downstream concern of `MealPlan` and `MealSession`.

---

## Related

- `Products/KitchenOS/10_Product_Vision.md`, Section 8.14 — closed-loop weekly planning and WeeklyMealPlan UX flow
- `Products/KitchenOS/20_Domain_Model.md` — WeeklyMealPlan aggregate root and planning horizon design note
- `Products/KitchenOS/40_Technical_Architecture.md` — Household Schedule Model (sub-model of Household Intelligence Model)
- `Knowledge/60_Decision_Records/ADR-010_Pantry_Derived_From_Confirmed_Activities.md` — pantry lifecycle rules and weekly planning layer
- PDR-005 — Ask only what the AI cannot reasonably learn on its own
- PDR-007 — Three-object meal lifecycle (MealRecommendation → MealPlan → MealSession)
