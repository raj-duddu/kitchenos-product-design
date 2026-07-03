---
id: PDR-003
title: Home Screen Answers a Question, Not a Dashboard
type: pdr
status: accepted
owner: product
depends_on: [PDR-002]
referenced_by: []
tags: [product-strategy, ux, home-screen, ai, decision-layer, dashboard]
date: 2026
---

# PDR-003: Home Screen Answers a Question, Not a Dashboard

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product, Design

---

## Context

Most food, pantry, and nutrition apps use their home screen as a data dashboard: pantry summary, recent activity, nutrition stats, trending recipes. This is the default pattern — show the user their data and let them decide what to do with it.

KitchenOS has an AI layer capable of synthesising household context (pantry state, budget, meal plan, history, goals, allergies) into actionable recommendations. The question was how to present this on the Home screen.

---

## Decision

**The KitchenOS Home screen answers one question: "What should I do in the kitchen today?"**

The Home screen is a decision layer, not a data dashboard. It surfaces 1–3 prioritised, actionable recommendations grounded in household context. It does not present raw data for the user to interpret.

---

## Reasons

**Users have a job to do, not data to analyse.** When someone opens KitchenOS, they want to know what to cook, what to buy, or what needs attention — not to review statistics. Presenting data forces the user to do the reasoning the AI should do for them.

**Decisions, not data, is a core product principle.** Section 8.6 of the Product Vision states: *"The product should deliver decisions, not data."* The Home screen is the most important surface to embody this principle. If the flagship screen is a dashboard, the principle is contradicted at the highest-visibility point in the product.

**AI value is invisible on dashboards.** A pantry summary showing "23 items" is data. "You have chicken, tomatoes, and pasta — dinner is covered" is a decision. The second form is what makes the AI layer visible and valuable. Dashboards bury AI insight under data; a decision layer makes it the primary content.

**Cognitive load reduction is the product's core UX promise.** Households are busy. The product exists to reduce the mental effort of food management. A dashboard increases cognitive load (the user must read, interpret, and decide). A decision layer reduces it (the system reads, interprets, and presents a ready answer).

**Precedent:** The iPhone home screen shows apps, not a system dashboard. Google's homepage has one field, not a data summary. The most successful consumer products put the action first.

---

## Alternatives Considered

**Dashboard home screen** — Rejected. Requires users to do the reasoning the AI should do. Buries the AI value proposition under data. Creates cognitive load instead of reducing it.

**AI-centric conversational home (chat interface)** — Rejected for MVP. Explicitly evaluated and rejected in `Products/KitchenOS/10_Product_Vision.md`, Section 18.2. A chat interface increases interaction cost and is not natural for daily household food management. Considered again post-MVP if conversational patterns emerge naturally from usage.

**Activity feed home** — Rejected. Shows what happened, not what to do. Useful as a secondary surface (Household Timeline under Household screen) but not as the primary home.

---

## Consequences

**Positive:**
- The AI layer's value is immediately visible on the most-visited screen.
- Cognitive load is low — the user sees a ready action, not data to interpret.
- The product feels different from existing food apps from the first screen.
- Daily habit formation is easier when the app immediately provides value.

**Negative:**
- Empty state for new households is harder — no household context means no good recommendations. Requires a deliberate empty state strategy (Section 21 of Product Vision).
- Recommendation quality must be high from day one — a bad recommendation on the home screen undermines trust immediately.
- Engineering complexity is higher than a simple data display — the Home screen depends on the Household Decision Engine producing good output.

**Implementation rule:**
- Home screen shows maximum 3 recommendations at any time.
- Each recommendation must be actionable (tappable, leading to Cook Mode, shopping, or a decision).
- Stale recommendations must show a staleness indicator, not hide the staleness.
- When household context is insufficient for a good recommendation, show a contextual prompt, not a generic suggestion.

---

## Related

- `Products/KitchenOS/10_Product_Vision.md`, Section 8.6 (Decisions, Not Data — core principle)
- `Products/KitchenOS/10_Product_Vision.md`, Section 18 (Information Architecture — dashboard rejected)
- `Products/KitchenOS/10_Product_Vision.md`, Section 19.1 (Home Screen Responsibilities)
- `Products/KitchenOS/10_Product_Vision.md`, Section 21 (Empty States)
- `Products/KitchenOS/40_Technical_Architecture.md`, Section 24 (Household Decision Engine)
- PDR-002: Household as primary unit
