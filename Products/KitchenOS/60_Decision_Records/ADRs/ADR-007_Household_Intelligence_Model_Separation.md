---
id: ADR-007
title: Household Intelligence Model as a Separate Architectural Layer
type: adr
status: accepted
owner: architecture
depends_on: [ADR-004, ADR-005]
referenced_by: []
tags: [ai-architecture, household-intelligence-model, domain-model, separation-of-concerns, recommendation-engine]
date: 2026
---

# ADR-007: Household Intelligence Model as a Separate Architectural Layer

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS must reason about household behaviour to produce personalised recommendations — preferred cuisines, typical cooking times, pantry depletion rates, meal acceptance patterns, and more. There are three natural places this data could live:

1. Inside the **Domain Model** — as additional fields on household or member entities.
2. Inside the **User Profile** — as preferences stored alongside account settings.
3. As a **separate intelligence layer** — an AI-owned model distinct from both.

The first two approaches are commonly used in simpler apps. They conflate factual business data with AI-derived beliefs, making it difficult to swap AI components, reason clearly about what is a stored fact versus an inference, or scale the intelligence layer independently of the business domain.

The product also requires a clear separation between what the system *knows* (facts recorded from events) and what the AI *believes* (inferences derived from patterns), because beliefs carry confidence scores, decay over time, and must be explainable and editable by users.

---

## Decision

**We will treat the Household Intelligence Model as a first-class architectural artifact, distinct from the Domain Model and the User Profile.**

The Domain Model stores business facts. The Household Intelligence Model stores AI beliefs. The Recommendation Engine reads both at request time to produce guidance.

---

## Reasons

**Facts and beliefs are fundamentally different.**
The Domain Model records what happened: milk was purchased, a receipt was scanned, a meal was cooked. The Intelligence Model infers what is likely: milk is consumed every 8 days with 91% confidence. Mixing these into the same model makes both harder to reason about, test, and evolve independently.

**AI components must be replaceable without touching business domain logic.**
If KitchenOS moves from OpenAI to a different provider, introduces reinforcement learning, or builds custom recommendation models, none of that should require changes to the Domain Model or event schema. A separate Intelligence Model makes this possible.

**Confidence scores and evidence tracking are AI concepts, not domain concepts.**
Every learned preference in the Intelligence Model carries a confidence value and an evidence count that decays without reinforcing signals. These are AI constructs that have no place in a business domain model.

**The separation applies to all future Amanaska products.**
This pattern — Personal Intelligence Model alongside Domain Model — is reusable across Amanaska Health, Finance, and Learning. Establishing the clean separation in KitchenOS defines the company-level architectural pattern.

**Transparency and user control require explicit ownership.**
The product principle "Trust is earned through transparency" requires that learned preferences be explainable, editable, and resettable by users. A dedicated Intelligence Model makes it straightforward to surface, correct, and forget individual beliefs without affecting the underlying domain events.

---

## Three Layers

| Layer | Owns | Example |
|---|---|---|
| Domain Model | Business facts — what happened | Milk purchased at Costco, $3.99, June 14 |
| Household Intelligence Model | AI beliefs — what is inferred | Milk consumed every 8 days, confidence 91% |
| User Profile | Account identity | Name, email, timezone, notification settings |

These three layers must never be merged.

---

## Alternatives Considered

### Option A: Preferences stored on Household entity in Domain Model

Simplest approach — add `preferred_cuisines`, `typical_cooking_time`, and similar fields directly to the household or member tables.

Rejected because:
- Domain Model becomes polluted with AI inference artifacts.
- Confidence scores and evidence tracking have no natural home in a relational entity.
- Replacing the AI layer requires migrating domain tables.
- The boundary between "what the user told us" and "what the AI inferred" is lost.

### Option B: Preferences stored in User Profile / settings

Treat learned preferences as editable user settings, storing them alongside account configuration.

Rejected because:
- User preferences are static and user-initiated. AI-learned beliefs are dynamic and system-initiated. They have different ownership, update frequencies, and trust levels.
- Confidence scores and decay logic cannot be cleanly modelled as user settings.
- Does not scale to the Collective Intelligence Model, which has no user-level equivalent.

---

## Consequences

### Positive

- Replacing or upgrading AI components never requires Domain Model changes.
- Confidence-scored beliefs can be surfaced, corrected, and forgotten cleanly.
- The pattern generalises to all future Amanaska products.
- Engineers and data scientists have a clear ownership boundary: domain events are an engineering concern; intelligence model training is an AI/data science concern.

### Negative

- More complexity than storing preferences on the household entity.
- Engineers must understand the boundary and enforce it consistently.

### Risks

- Boundary drift: if individual features start adding AI-derived fields to domain tables for convenience, the separation erodes. Code review must enforce the boundary.
- The Intelligence Model requires its own storage and update pipeline — additional operational surface area that MVP-0 does not activate.

---

## MVP Scope

| Phase | Intelligence Model Scope |
|---|---|
| MVP-0 | Static Facts only — onboarding data seeds the model; no behavioural learning |
| MVP-1 | Basic behavioural signals: meal acceptance/rejection, pantry depletion rates |
| Post-MVP | Full confidence-scored model, Learning Engine, transparency screen |

---

## Related

- ADR-004: Domain-Driven Event Sourcing (domain events are the input to the Intelligence Model)
- ADR-005: Modular Monolith (intelligence model lives in its own module)
- ADR-008: Collective Intelligence Model (the network-level counterpart to this per-household model)
- `Knowledge/10_Product_Vision.md`, Section 50A: Household Intelligence Model (product explanation)
- `Knowledge/40_Technical_Architecture.md`, Section 24A: Household Intelligence Model (architectural specification)
