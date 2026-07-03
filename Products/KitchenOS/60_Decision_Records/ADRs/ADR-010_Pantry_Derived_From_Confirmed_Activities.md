---
id: ADR-010
title: Pantry State Is Derived Exclusively from Confirmed Household Activities
type: adr
status: accepted
owner: architecture
depends_on: [ADR-004, ADR-007]
referenced_by: []
tags: [pantry, meal-session, shopping-trip, domain-model, event-sourcing, cook-mode, household-activity-lifecycle]
date: 2026
---

# ADR-010: Pantry State Is Derived Exclusively from Confirmed Household Activities

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS's pantry is the foundation for every downstream calculation: recipe recommendations, shopping list generation, budget tracking, nutrition analysis, and waste reduction. If pantry state is inaccurate, every AI recommendation built on top of it is inaccurate.

The naive implementation of pantry deduction is to trigger it from the recipe or from Cook Mode: when a user completes Cook Mode, subtract the recipe's ingredients from the pantry. This is simple but introduces several problems:

1. **Portion assumptions are wrong.** Recipes specify servings, but not who is eating, how many people are actually present, or what portion each person consumed. Deducting by recipe servings ignores reality.
2. **Leftovers are invisible.** If a user cooked 6 portions and only 4 were eaten, 2 portions worth of food remains. That food is now missing from the pantry because the recipe deducted all 6.
3. **Cook Mode conflates UI with domain.** Making a UI component responsible for pantry state means the pantry cannot be updated via other paths (voice, manual logging, smart appliance integration) without duplicating or bypassing Cook Mode logic.
4. **AI recommendations trigger pantry changes.** If accepting a recipe recommendation triggers pantry deduction, the pantry changes based on intention, not action. The user may accept a recommendation and never cook it.
5. **No concept of guests or variable portions.** Households sometimes cook for more or fewer people than the recipe assumes. The domain model needs to capture who actually ate, not who was expected to eat.

More broadly: a pantry that can be mutated by AI predictions, recipe selections, or UI events is not trustworthy. An AI cannot build reliable recommendations on a pantry that reflects intent rather than reality.

---

## Decision

**Pantry state is derived exclusively from confirmed household activities. The pantry is never updated by a recommendation, a recipe, a prediction, or a UI component. Only completed and user-confirmed domain activities may produce pantry update events.**

The four activities that may update the pantry, and their confirmation triggers:

| Activity | Updates Pantry | Confirmation Required |
|---|---|---|
| ShoppingTrip (via Receipt) | Adds items | User confirms items from receipt |
| MealSession | Deducts items | User confirms participants, portions, and completion |
| WasteEvent | Removes items | User confirms disposal |
| PantryCorrection | Adjusts quantities | User confirms corrected quantity |

No other mechanism may produce a `PantryItemConsumed`, `ItemAddedToPantry`, `PantryItemThrownAway`, or `PantryItemQuantityCorrected` event.

---

## The Four-Layer Cooking Lifecycle

The full path from weekly planning to pantry update passes through four distinct layers with progressively stronger commitments:

```text
WeeklyMealPlan  (Strategy Layer)
  ├── Household's committed meal strategy for a week
  ├── Accepted in one tap; creates MealPlans atomically
  ├── NO pantry change — strategy ≠ execution
  ├── Living document: individual meals swapped as week unfolds
  └── Abandoned / completed → no state change to pantry

        ↓ per-meal, when cooking time approaches

MealRecommendation  (Planning Layer)
  ├── Ephemeral AI output (or the slot from WeeklyMealPlan surfaced as a reminder)
  ├── Predicted participants + confidence score
  ├── NO household state committed
  └── Accepted → creates / confirms MealPlan
      Rejected / expired → discarded

        ↓ user taps "Start Cooking"

MealPlan  (Intention Layer)
  ├── Committed intention for a single meal
  ├── Confirmed participants + planned portions (domain facts, not AI beliefs)
  ├── NO pantry change — intention ≠ execution
  └── Transitions to MealSession when cooking starts
      Cancelled / never started → expires with no state change

        ↓ cooking completes, user confirms

MealSession  (Execution Layer)
  ├── Reality: what actually happened
  ├── Actual participants + actual portions + leftovers
  └── PantryItemConsumed events emitted on completion
      This is the ONLY pantry deduction trigger
```

**The key invariant holds at every layer:**

| Layer | Pantry change? |
|---|---|
| WeeklyMealPlan accepted | No |
| MealPlan created / confirmed | No |
| MealSession started | No |
| MealSession **completed + confirmed** | **Yes — the only trigger** |

A household can plan every meal for the next month, accept every weekly plan, and start cooking a dozen times — if they abandon each MealSession before confirming completion, the pantry is unchanged. Pantry state is never speculative.

---

## The MealSession Aggregate

This decision requires introducing `MealSession` as a first-class domain aggregate — the authoritative source for all pantry deductions from food consumption.

A MealSession owns:
- The recipe (optional — meals can be cooked without a recipe)
- The confirmed participants (which household members ate)
- The planned and actual portions
- The leftovers (prepared minus consumed, optionally returned to pantry)
- The completion confirmation

`PantryItemConsumed` events are emitted by the MealSession aggregate when it reaches `status: completed` and the user confirms. They are never emitted by Cook Mode, recipe selection, or the recommendation engine.

---

## Cook Mode's Role

Cook Mode is a UI capability that facilitates a MealSession. It provides step-by-step cooking guidance. It does not own pantry state.

```text
Cook Mode (UI) → drives → MealSession (domain) → on completion → PantryItemConsumed events
```

Cook Mode domain events (`CookModeSessionStarted`, `CookModeStepCompleted`) are UI state events. They do not produce pantry changes. This means:
- The pantry update path is independent of the Cook Mode UI.
- A user can log a MealSession manually without using Cook Mode and produce the same pantry outcome.
- Future cooking interfaces (voice, smart appliance) produce the same MealSession — same pantry outcome.

---

## Reasons

**Pantry accuracy requires real-world confirmation, not prediction.**
Every AI recommendation KitchenOS makes depends on knowing what is actually in the pantry. Deducting based on recipe selection or acceptance captures intent, not action. A user can accept a recipe and not cook it. They can cook fewer portions than planned. They can have unexpected guests. Only a confirmed MealSession captures what actually happened.

**Leftovers are real food.** If 6 portions are prepared and only 4 consumed, 2 portions of food remain. A pantry that deducts all 6 is wrong. MealSession models this correctly: `prepared - consumed = leftovers`, which can optionally be returned to the pantry as a new item.

**Separating Cook Mode (UI) from MealSession (domain) is correct DDD.**
Cook Mode is a screen. MealSession is a business event. Coupling pantry updates to a UI component makes the domain model fragile, prevents alternative UI paths, and violates the principle that domain aggregates should be independent of the presentation layer.

**The symmetry with ShoppingTrip is architecturally clean.**
Both ShoppingTrip (adds food) and MealSession (removes food) follow the same Household Activity Lifecycle pattern. Both require confirmation. Both produce domain events that update the pantry. This consistency makes the backend predictable and the Household Timeline readable.

**AI can pre-fill; humans confirm.** The AI can suggest likely participants, estimate portions from recipe servings, and flag leftovers. The user reviews and confirms. The domain event is written on confirmation, not on suggestion. This keeps the AI in an advisory role and pantry state in the user's control.

---

## Alternatives Considered

### Option A: Cook Mode deducts pantry on completion

Cook Mode is the primary interface for cooking. When Cook Mode reaches the final step and the user taps "Done," the recipe's ingredient quantities are subtracted from the pantry.

Rejected because:
- Deducts by recipe servings, not actual consumption — leftovers are invisible.
- No concept of variable participants — guests, absent household members.
- Couples pantry state to a UI component — alternative cooking interfaces cannot update the pantry without using Cook Mode.
- A user who completes Cook Mode but stores leftovers has their pantry incorrectly depleted.

### Option B: Recipe acceptance deducts pantry

When a user accepts a recipe recommendation, pantry items are reserved or deducted.

Rejected because:
- Intention ≠ action. A user may accept a recommendation and not cook.
- Deduction happens before the user has cooked anything — pantry state reflects plans, not reality.
- Leads to frequent pantry corrections as users whose plans changed must manually restore items.

### Option C: AI infers pantry depletion from patterns

The AI tracks how long items typically last and infers consumption rather than waiting for explicit events.

Retained as a supplementary signal for the Household Intelligence Model only. Rejected as the primary mechanism for pantry state. Inferred depletion is a prediction, not a fact. It cannot be the source of truth for downstream calculations.

### Option D: Automatic deduction with easy undo

Deduct pantry automatically (on Cook Mode completion or recipe acceptance) but make it easy to undo.

Rejected because:
- Frequent incorrect deductions followed by corrections trains users to distrust the pantry.
- The Household Timeline would be cluttered with automatic deductions and their corrections.
- The product principle is "AI recommends, users decide." Automatic pantry deduction inverts this — the system acts, the user corrects.

---

## Consequences

### Positive

- Pantry state is accurate: it reflects what actually happened, not what was planned or predicted.
- AI recommendations built on pantry state are trustworthy — they reflect real availability.
- Leftovers are tracked and can reduce waste and shopping list generation errors.
- Cook Mode becomes UI-only — future cooking interfaces work the same way.
- The Household Activity Lifecycle is a consistent, extensible pattern for all pantry-affecting events.
- Nutrition tracking per member becomes accurate — based on confirmed participants and portions, not recipe averages.

### Negative

- Requires a confirmation step after cooking — one extra tap/screen compared to automatic deduction.
- MealSession is a new aggregate that engineers must understand before building any cooking or pantry feature.
- Manual meal logging (without Cook Mode) requires a lightweight entry flow that does not yet exist in the product design.

### Risks

- **Confirmation fatigue:** If the confirmation step is poorly designed, users skip it or abandon it. Mitigation: pre-fill everything the AI can reasonably infer (participants, portions, ingredient quantities), minimise required input, make confirmation feel like a natural end to cooking rather than an additional task.
- **Partial adoption:** Engineers building features may be tempted to add direct pantry updates for "simple" cases. Mitigation: the invariant is documented as non-negotiable in the Domain Model and must be enforced in code review.

---

## Engineering Rules (Non-Negotiable)

1. `PantryItemConsumed` events may only be emitted by the MealSession aggregate on `MealSessionCompleted`.
2. `ItemAddedToPantry` events may only be emitted by the Receipt aggregate on `ReceiptItemsConfirmed` or by PantryCorrection on correction confirmation.
3. `PantryItemThrownAway` events may only be emitted by WasteEvent on confirmation.
4. No recipe, recommendation, planning, or Cook Mode component may write directly to the `pantry_items` table or emit pantry domain events.
5. A PR that adds a pantry update path outside these four activities must be rejected in code review.

---

## Related

- ADR-004: Domain-Driven Event Sourcing (events are the source of truth for pantry state)
- ADR-007: Household Intelligence Model (intelligence model learns from confirmed MealSession events, not predictions)
- `Products/KitchenOS/20_Domain_Model.md`: MealSession aggregate, Pantry invariants, Household Activity Lifecycle
- `Products/KitchenOS/40_Technical_Architecture.md`, Section 25: Household Activity Lifecycle Pattern
