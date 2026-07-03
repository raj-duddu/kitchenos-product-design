---
id: PDR-010
title: Cook Mode Is the Primary MVP-0 Habit Loop
type: pdr
status: proposed
owner: product
depends_on: [PDR-002, PDR-007]
referenced_by: [DOC-010]
operating_principles: ["2. Turn Information into Guidance", "3. Inspire Confident Action"]
tags: [product-strategy, mvp, cook-mode, habit-loop, retention, meal-session]
date: 2026
---

# PDR-010: Cook Mode Is the Primary MVP-0 Habit Loop

**Status:** Proposed *(backfill — decision made pre-record-system; reconstructed from Product Vision Sections 39.4 and 60)*
**Date:** 2026-07-03
**Deciders:** Founders
**Stage Gate:** Stage 3 of Product Development Lifecycle
**Operating Principles:** 2 (Turn Information into Guidance), 3 (Inspire Confident Action)

---

## Context

MVP-0 needs one habit-forming loop that proves the product thesis and feeds the data flywheel. Candidate hero features each touch the household food lifecycle at a different point: planning, shopping, scanning, or cooking. The choice determines build order, the retention metric, and which data KitchenOS learns from first.

Cooking is the moment where intention becomes reality: a completed MealSession is the only event that deducts pantry state (ADR-010, PDR-007), confirms who actually ate (feeding the Schedule and Preference models), and delivers immediate user value (guided cooking, automatic pantry bookkeeping). A habit loop anchored anywhere else produces intentions without ground truth.

---

## Decision

**Cook Mode is the hero feature and primary habit loop of MVP-0.** Build order, onboarding, the Home screen's default suggestion, and MVP-0 retention metrics centre on driving and completing MealSessions through Cook Mode.

---

## Reasons

- Completed MealSessions are the richest learning events in the system — participants, portions, leftovers, and recipe acceptance in one confirmed activity.
- Cook Mode makes pantry accuracy a side effect of getting value, not a chore — the deduction happens because the user cooked, not because they did data entry.
- Cooking recurs daily; receipts weekly; planning weekly. The highest-frequency touchpoint builds the habit.
- It demonstrates the product philosophy directly: step-by-step guidance instead of raw information (Principle 2), ending in a confident, completed action (Principle 3).

---

## Alternatives Considered

### Option A: Meal planning as the hero
Weekly frequency; produces intentions, not ground truth. Plans without execution data cannot teach the intelligence layer what actually happens. Rejected.

### Option B: Receipt scanning as the hero
Valuable data entry, but weekly and utilitarian — nobody builds a daily habit around receipts. It supports the loop; it is not the loop. Rejected.

### Option C: Shopping list as the hero
Commodity feature with strong incumbents; differentiates nothing. Rejected.

### Option D: No hero — breadth-first MVP
Spreads effort across the whole lifecycle; nothing reaches habit-forming quality. Contradicts MVP discipline (Section 38). Rejected.

---

## Consequences

### Positive
- Clear build order: Cook Mode + MealSession completion path gets polish first.
- MVP-0 retention metric is concrete: weekly Cook Mode completions per household.
- The data flywheel starts at the highest-value event stream.

### Negative
- Households that rarely cook get less MVP-0 value — accepted; they are not the initial target (Section 12 profiles).
- Cook Mode quality bar is high: a clunky hero feature poisons the whole thesis.

### Risks
- If real usage shows a different loop dominates (e.g., shopping), this record is superseded — the event stream will show it.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-03 | Proposed (backfill — decision predates the record system) | Claude (PM role), sponsored by @raj-duddu | PR # (add on merge) |

---

## Related

- `Products/KitchenOS/10_Product_Vision.md`, Section 39.4 — Cook Mode: Hero Feature (product detail)
- PDR-007 — Three-object meal lifecycle; MealSession is the execution layer this loop drives
- ADR-010 — Pantry derived from confirmed activities; Cook Mode completions are the confirmations
- PDR-002 — Household as primary unit; participants confirmed per session
