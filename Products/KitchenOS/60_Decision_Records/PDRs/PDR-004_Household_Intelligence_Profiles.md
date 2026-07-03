---
id: PDR-004
title: Personas as Household Intelligence Profiles, Not UX Personas
type: pdr
status: accepted
owner: product
depends_on: [PDR-002]
referenced_by: []
tags: [personas, household-intelligence-profiles, ai-design, product-philosophy, ux]
date: 2026
---

# PDR-004: Personas as Household Intelligence Profiles, Not UX Personas

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product

---

## Context

KitchenOS's product documentation included five traditional UX personas: Busy Family, Working Professional, Budget Household, Health-Focused Household, and Cooking Enthusiast. These personas described user demographics, pain points, and general needs — the standard format inherited from UX practice.

The problem is that traditional UX personas answer the wrong question for an AI-first product. They describe *who the user is* but not *how the system must reason differently for each household type*. A product manager can use them to prioritise features. An AI engineer or data scientist cannot use them to understand what context the Household Decision Engine needs, what signals it must learn, or what behaviours it must exhibit.

KitchenOS is not a feature set that maps to user types. It is an intelligence layer that adapts to each household's context, goals, constraints, and habits. The personas need to reflect that.

---

## Decision

**We will replace traditional UX personas with Household Intelligence Profiles — AI design documents that specify, for each household type, what KitchenOS must understand, how it must behave proactively, and what success looks like.**

The section in the Product Vision is renamed from "Personas" to "Household Intelligence Profiles."

---

## Reasons

**Personas must be useful to AI engineers and data scientists, not just product and UX.**
A traditional persona saying "pain point: doesn't know what to cook" tells an AI engineer nothing. A profile saying "KitchenOS must understand pantry state, available cooking time, energy context, and takeout patterns to recommend dinner for this household type" is an AI design specification.

**The five-question structure forces the right thinking.**
Primary Goal, Daily Friction, KitchenOS Must Understand, KitchenOS Behaviors, and Success Looks Like are not cosmetic changes. They force the team to articulate what intelligence is required, not just what users want. "KitchenOS Must Understand" is the AI design layer. "KitchenOS Behaviors" are the proactive outputs. This thinking does not emerge from traditional pain point / needs lists.

**Proactive AI outputs make the product philosophy concrete.**
The profiles include example AI outputs (quoted guidance the system should produce) for each household type. This grounds abstract AI capability in real, reviewable product behaviour. Teams can debate whether an example output is realistic, achievable, and aligned with the product before a line of code is written.

**"Information becomes guidance" needs to be demonstrated, not stated.**
The product principle is that KitchenOS turns information into guidance. Traditional personas state what users want. Household Intelligence Profiles demonstrate what guidance looks like for each household type. The principle becomes visible.

**Consistent structure across all household types.**
Five questions applied uniformly makes the profiles comparable, reviewable, and evolvable. Adding a sixth household type in the future follows the same structure. No persona is a special case.

---

## The Five-Question Structure

| Question | Purpose |
|---|---|
| Primary Goal | Anchors the profile in a real household outcome, not a feature request |
| Daily Friction | Grounds the profile in observed reality — what actually gets in the way |
| KitchenOS Must Understand | AI design specification — what context and intelligence is required |
| KitchenOS Behaviors | Proactive AI outputs — what the system does without being asked |
| Success Looks Like | Measurable outcomes — how life improves, not just how features are used |

---

## Alternatives Considered

### Option A: Keep traditional UX personas with AI opportunity bullets

Retain the existing format but add an "AI opportunities" section listing potential AI features per persona.

Rejected because:
- AI opportunities as a bullet list ("predict shopping needs") is too vague to guide AI design.
- The format still centres on user characteristics, not system intelligence requirements.
- Product, UX, AI, and backend teams still have different interpretations of the same document.

### Option B: Separate documents — UX personas + AI requirement specs

Maintain traditional UX personas for product/UX teams and create separate AI requirement documents for engineering teams.

Rejected because:
- Maintaining two documents for the same household type creates divergence and duplication.
- The goal is a single document that all disciplines find useful — one source of truth.
- The five-question structure achieves this without needing two formats.

---

## Consequences

### Positive

- Product, UX, AI engineers, backend engineers, and data scientists can all read the same profile and extract actionable direction.
- Example AI outputs serve as acceptance criteria anchors for AI feature development.
- "KitchenOS Must Understand" becomes an explicit input to data model and feature decisions.
- Profiles are directly usable in hiring, onboarding new team members, and investor conversations.

### Negative

- Requires more thinking per profile than a traditional persona — the team must articulate AI requirements, not just user needs.
- Example AI outputs may become stale as the product evolves and must be maintained alongside the profile.

### Scope Boundary

- Household Intelligence Profiles describe household types, not individual users. Individual member-level differences (e.g. one member wants muscle gain, another wants weight loss) are handled within the Health-Focused profile through the Household Decision Engine's per-member goal model.
- These profiles do not replace user research. They are design documents that should be validated against real household behaviour.

---

## Related

- PDR-002: Household as Primary Unit (profiles are household-level, not individual-level)
- `Products/KitchenOS/10_Product_Vision.md`, Section 12: Household Intelligence Profiles
- ADR-007: Household Intelligence Model Separation (the intelligence each profile requires lives in the Household Intelligence Model)
