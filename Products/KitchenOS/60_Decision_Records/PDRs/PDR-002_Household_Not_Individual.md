---
id: PDR-002
title: Household as Primary Unit, Not Individual
type: pdr
status: accepted
owner: product
depends_on: [PDR-001]
referenced_by: [PDR-003]
tags: [product-strategy, household, individual, data-model, permissions, shared-intelligence]
date: 2026
---

# PDR-002: Household as Primary Unit, Not Individual

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product

---

## Context

Most food, nutrition, and recipe apps are designed for individual users: one account, one meal plan, one shopping list, one set of preferences. This is the default design pattern in the consumer app market.

KitchenOS must decide whether the individual or the household is the primary unit of the product.

---

## Decision

**The Household is the primary unit of KitchenOS.** Every data model, screen, and AI decision is anchored to the Household. Individual Members exist within a Household and have their own profiles, allergies, and goals — but these are always expressed in the context of shared food decisions.

---

## Reasons

**Real kitchens are shared.** Most households have 2–4 people sharing a pantry, budget, and cooking responsibility. Designing for individuals means every multi-person household is a second-class citizen of the product.

**Food decisions are inherently shared.** "What's for dinner?" is a household question, not an individual question. "What should we buy?" is a household question. The shopping list belongs to the household. The pantry belongs to the household. Optimising for the individual alone produces wrong answers.

**Allergy safety requires a household model.** If one member has a nut allergy, every meal planned for the household must respect it — even meals cooked by a different member. Individual-only models cannot express this safety constraint without awkward workarounds.

**The shared pantry is the data advantage.** The household pantry — what was actually bought, consumed, cooked, and wasted — is the richest signal for food intelligence. A single-user app accumulates individual data. KitchenOS accumulates household behavioural data, which is more predictive of actual purchasing and cooking patterns.

**Household moats are harder to leave.** When an individual stops using an app, they take only their data. When a household adopts KitchenOS, the pantry history, shared shopping lists, and household allergy profiles create switching costs that individual apps do not generate.

**Individual goals exist within the household context.** A member pursuing muscle gain doesn't eat separate meals from the household — they eat the household meal with adjustments (portions, add-ons, substitutions). The household model accommodates this; an individual model does not.

---

## Alternatives Considered

**Individual-first with optional household sharing** — Rejected. Household food behaviour cannot be retrofitted from individual data. Starting individual-first means the core data model is wrong from day one.

**Organisation-first (e.g., targeting meal-prep services or corporate cafeterias)** — Deferred. B2B is a separate GTM motion. The household product must be validated before B2B is explored.

---

## Consequences

**Positive:**
- The data model is correct for the actual use case — shared kitchens.
- Allergy and dietary safety can be expressed cleanly at the household level.
- Onboarding captures household composition from the start, enabling better AI recommendations immediately.
- Switching costs are higher than individual apps.

**Negative:**
- Single-person households get less value from shared features.
- Onboarding is slightly more complex (must capture members, not just a profile).
- Household permission and privacy model adds complexity (who can see whose allergies and goals).

**Data model implication:**
- Every domain event carries `household_id`.
- Individual member data (allergies, goals) is always associated with both a `user_id` and a `household_id`.
- `household_safety_rules` are derived from individual `dietary_constraints` — the household view is computed, not independently set.

---

## Related

- `20_Domain_Model.md` — Household aggregate root, Member entity, household_safety_rules
- `10_Product_Vision.md`, Section 56 (Allergies and Household Profiles)
- `10_Product_Vision.md`, Section 14 (Household Lifecycle)
- `40_Technical_Architecture.md`, Section 32 (all events carry household_id)
- PDR-001: Food decisions before fitness
- PDR-003: Home screen answers a question
