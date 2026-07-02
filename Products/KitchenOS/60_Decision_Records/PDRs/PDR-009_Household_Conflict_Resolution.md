---
id: PDR-009
title: Household Conflict Resolution Policy — Six-Level Priority Hierarchy
type: pdr
status: accepted
owner: product
depends_on: [GDR-001, PDR-002, PDR-007]
referenced_by: []
tags: [household-conflict, recommendation-engine, priority-hierarchy, safety, goals, product-behaviour, multi-member]
date: 2026
---

# PDR-009: Household Conflict Resolution Policy — Six-Level Priority Hierarchy

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026
**Deciders:** Founding team
**Stage Gate:** Stage 3 — Product Definition

---

## Context

KitchenOS serves households, not individuals. A household of four might include:

- **Dad** — goal: muscle gain, no restrictions
- **Mum** — goal: weight loss, lactose intolerant
- **Child (8)** — nut allergy, picky eater
- **Grandmother** — low sodium requirement, no personal goal

There is no single "correct" dinner recommendation that satisfies all constraints equally. The AI must apply a consistent, documented priority policy when generating any household-level recommendation.

Without a documented policy, engineers will implement their own implicit priority ordering. Different features will apply different orderings. The result is an AI that behaves inconsistently, fails safety-critical checks in edge cases, and cannot be explained or audited.

This is not an architecture decision. It is a product behaviour decision that drives architecture. The recommendation engine, the Allergy Guard, and the Household Decision Engine all implement this policy.

---

## Decision

**The KitchenOS recommendation engine will resolve household member conflicts using a six-level priority hierarchy. Higher levels always take precedence over lower levels. No AI confidence score, no user preference, and no optimisation target may override a higher-level constraint.**

---

## The Six-Level Priority Hierarchy

```text
Level 1 — Safety (highest priority)
  Allergies, medical restrictions, household safety rules
  Source: PersonProfile (dietary_constraints), household_safety_rules
  Rule: If any member has an allergy or medical restriction that conflicts
        with a recommendation, the recommendation is BLOCKED. No exceptions.
        The Allergy Guard enforces this before any output reaches the user.

        ↓

Level 2 — Mandatory Constraints
  Religious requirements (halal, kosher, etc.)
  Ethical constraints (vegan, vegetarian as a stated value, not preference)
  Household-level rules set by admin
  Source: PersonProfile (dietary_constraints), household settings
  Rule: Constraints marked as mandatory are treated as non-negotiable.
        The distinction between mandatory constraint and preference is
        set by the member, not inferred by AI.

        ↓

Level 3 — Life-Stage Requirements
  Children's nutritional needs, elderly dietary requirements
  Pregnancy or breastfeeding flags (if stated)
  Source: PersonProfile (age_group, active goals with life-stage flag)
  Rule: Age-appropriate nutrition and portion sizing are applied for
        children and elderly members even when no explicit goal is set.
        AI does not infer medical conditions — only age group is used.

        ↓

Level 4 — Individual Goals
  Weight loss, muscle gain, calorie targets, macro targets
  Source: PersonProfile (user_goals)
  Rule: Goals influence recommendation ranking and meal composition
        but do not block recommendations. A meal that is suboptimal
        for one member's goal is still valid if it satisfies levels 1–3.
        Goals are satisfied on a best-effort basis, not guaranteed.

        ↓

Level 5 — Preferences
  Cuisine affinity, ingredient preferences, cooking complexity preference
  Source: Household Intelligence Model (Preference Model)
  Rule: Learned preferences rank recommendations but never filter them.
        A household that rarely cooks Indian food will see fewer Indian
        recommendations by default, but the AI may still suggest one
        if it strongly satisfies higher-level constraints.

        ↓

Level 6 — Optimisation (lowest priority)
  Cost minimisation, waste reduction, convenience, pantry utilisation
  Source: Pantry state, Budget context, Shopping history
  Rule: Optimisation targets are applied last. A cheaper meal is preferred
        over a more expensive one only when all other levels are equal.
        Pantry utilisation (use expiring items first) is an optimisation
        signal, not a safety signal — it does not override any higher level.
```

---

## Conflict Resolution Rules

When a recommendation cannot satisfy all members at any level, the following applies:

| Situation | Resolution |
|---|---|
| Any member's Level 1 constraint is violated | Recommendation is blocked entirely. Never shown. |
| Level 2 constraint conflicts between members (e.g., one halal, one vegan) | Recommend meals that satisfy both. If no meal satisfies both, recommend separate components or flag the conflict to the user. |
| Level 3–4 conflicts (e.g., weight loss vs. muscle gain macros) | Recommend the meal that best satisfies the household aggregate. Surface per-member goal impact in the recommendation explanation. |
| Level 5–6 conflicts | Apply household-level preference and optimisation signals. No conflict resolution needed — these are soft rankings, not hard constraints. |

### The Explanation Obligation

When a recommendation is modified, constrained, or ranked due to this hierarchy, the AI must be able to explain which level caused the change. The user must be able to ask "why not X?" and receive a meaningful answer.

Example: *"We didn't suggest the pesto pasta because it contains pine nuts, which conflicts with [Child]'s nut allergy."*

---

## Reasons

- **Safety cannot be implicit.** Without a documented hierarchy, safety constraints compete with goal optimisation in the recommendation engine. A well-intentioned engineer could accidentally implement a system where a high-confidence meal recommendation bypasses a critical allergy check. The hierarchy makes Level 1 inviolable by policy, not by hope.
- **Consistency across features.** The same hierarchy applies to meal recommendations, shopping suggestions, expert plan reviews, and WeeklyMealPlan generation. A consistent policy prevents features from diverging.
- **Explainability.** A documented hierarchy enables auditable explanations. When the AI blocks or modifies a recommendation, the reason is traceable to a specific level.
- **User trust.** Members who know their constraints are always respected — even when they conflict with other members' goals — trust the system more than one that treats all constraints as soft preferences.

---

## Alternatives Considered

### Option A: Weighted scoring (no hard hierarchy)

All constraints and preferences are scored and combined into a single recommendation score. Allergy conflicts carry a very high negative weight.

Rejected because: weighted scoring makes Level 1 safety constraints probabilistic, not absolute. A sufficiently high positive score from other factors could theoretically override an allergy block. This is unacceptable. Safety must be a hard filter, not a high-weight term.

### Option B: Per-member recommendations only (no household-level resolution)

Generate separate recommendations for each member and let the household choose.

Rejected because: this ignores the household as the primary unit (PDR-002) and dramatically increases cognitive load. A household of four would need to choose from four separate recommendation sets for every meal. The value proposition of KitchenOS is household-level intelligence, not individual-level.

### Option C: Six-level hierarchy with hard filters at Level 1–2, soft ranking at Level 3–6 (chosen)

Levels 1 and 2 are hard filters — violations block recommendations. Levels 3–6 influence ranking and composition but do not block. This is the chosen approach.

---

## Consequences

### Positive

- Safety is architecturally guaranteed, not just hoped for.
- Recommendation engine implementation has a clear, auditable policy to implement.
- The explanation system has a documented basis for generating meaningful constraint explanations.
- New household member types (guest, caregiver, elderly relative) can be added without redesigning the hierarchy.

### Negative

- In households with many conflicting Level 1–2 constraints, the recommendation space may be significantly narrowed. The AI must communicate this honestly rather than silently degrading recommendation quality.
- Life-stage requirements (Level 3) require careful definition — the system uses age group, not medical inference. The boundary between "age-appropriate nutrition" and "medical advice" must be maintained. See GDR-001.
- Goal conflicts (Level 4) may require per-member explanations in the recommendation output, adding UI complexity.

### Scope Boundary

- This PDR defines the policy. The technical implementation (how the Household Decision Engine applies the hierarchy) is in `Knowledge/45_Solution_Designs/` when that solution design is written.
- Individual goal tracking and nutritional calculations are a separate concern — this PDR only defines their *priority* relative to other constraints.
- Guest members (temporary, no profile) default to Level 5–6 only. They have no stored constraints or goals.

---

## Related

- `Company/Operating_Principles.md`, Principle 1 — AI recommends; people decide
- GDR-001 — Trusted Decision Support, Not Autonomous Diagnosis (the policy that Level 1 conflicts are never autonomous)
- PDR-002 — Household as primary unit, not individual
- PDR-007 — Three-object meal lifecycle
- `Knowledge/20_Domain_Model.md` — PersonProfile invariants (allergies and goals), household_safety_rules derivation
- `Knowledge/40_Technical_Architecture.md` — Household Decision Engine, Allergy Guard
