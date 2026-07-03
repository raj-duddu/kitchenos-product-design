---
id: GOV-001
title: AI Governance
type: governance
status: active
owner: founders
scope: KitchenOS (implements GDR-001 and GDR-002)
depends_on: [GDR-001, GDR-002, ADR-007, ADR-008]
date: 2026
---

# AI Governance

> This document implements GDR-001 (Trusted Decision Support, Not Autonomous Diagnosis) and GDR-002 (Privacy by Design) for KitchenOS. It defines the operational rules that govern every AI output in the product.

---

## Decision Criticality Framework

Every AI output in KitchenOS must be classified at one of four criticality levels before it is implemented. The level determines the safeguards required.

| Level | Definition | Examples | Required safeguard |
|---|---|---|---|
| **Low** | Recommendation with no safety implications; easily reversible | Suggest pasta for dinner, recommend apples, reorder a shopping list | AI may recommend automatically. No confirmation required. |
| **Medium** | Recommendation that affects household decisions but carries no safety risk | Substitute one ingredient, adjust shopping quantities, suggest a different store | Recommendation shown with explanation. User sees basis for suggestion. One-tap accept. |
| **High** | Recommendation that could affect a member's health goals, involves a known constraint, or is difficult to reverse | Calorie reduction suggestion, recipe for a member with dietary restrictions (non-allergy), expert plan suggestion | Explicit user confirmation required before any action. Explanation mandatory. |
| **Critical** | Any recommendation that touches a Level 1 or Level 2 constraint (see PDR-009), conflicts with a safety rule, or involves a regulated domain | Any ingredient that is an allergen for any household member, anything affecting a stated medical restriction, anything an expert has flagged as requiring their review | **Never autonomous.** Allergy Guard must pass. Explicit confirmation required. Expert involvement may be mandated. A failed safety check blocks the output entirely — it is never shown to the user with a warning. |

### Classification Rules

- Classification is assigned at feature design time, not runtime.
- If there is any uncertainty about the level, assign the higher level.
- A feature that *could* produce Critical output at runtime must be implemented as Critical even if most outputs are Low.
- Classification must be documented in the Solution Design (`45_Solution_Designs/`) for any feature that produces AI output.

---

## Autonomous Action Policy

| Condition | AI may act autonomously? |
|---|---|
| Low criticality, user has previously confirmed similar action | Yes |
| Low criticality, first time | Yes, with explanation surfaced |
| Medium criticality | No. Recommendation shown; user confirms |
| High criticality | No. Explicit confirmation with explanation mandatory |
| Critical criticality | Never. Safety check must pass first. Explicit confirmation. |
| Any action affecting pantry, budget, or shopping list | No. Always user-confirmed via domain event (MealSessionCompleted, ShoppingTripConfirmed, etc.) |
| Any action based on an Expert recommendation | No. `ExpertRecommendationApproved` event required first |

---

## Confidence and Explanation Requirements

Every AI recommendation must carry:

| Field | Required | Notes |
|---|---|---|
| `confidence_score` | Yes | 0.0–1.0. Shown to user when Medium or higher |
| `explanation` | Yes for Medium+ | One sentence minimum: why this recommendation |
| `constraint_applied` | Yes when a constraint influenced the output | Which household constraint shaped this output |
| `data_used` | Yes for High+ | Which household context was used (pantry state, goals, preferences) |
| `reversible` | Yes | Can the user undo this action? |

Low-confidence outputs (below threshold defined per feature) must either:
- Not be shown, or
- Be shown with an explicit low-confidence indicator and a "tell us more" prompt

The AI must never present a low-confidence output as if it were certain.

---

## What Is Never Delegated to AI

The following decisions are always human:

1. Accepting or rejecting any meal plan, shopping trip, or expert recommendation.
2. Overriding an allergy or dietary restriction.
3. Adding or removing a household member.
4. Granting or revoking expert consent.
5. Deleting household data or resetting the intelligence model.
6. Confirming a pantry update (consumption, addition, or removal).

These are domain actions that produce domain events. AI may suggest them. Only the user can confirm them.

---

## Prompt and Model Governance

### Prompt Versioning

- Every AI prompt is versioned.
- Prompt versions are tagged in the codebase alongside the feature version.
- A prompt change that alters the nature of AI output (not just phrasing) requires a new prompt version and a re-evaluation of the criticality classification.

### Model Evaluation

Before any new AI model is deployed to production:

- Evaluate on a household dataset representing the full range of household configurations (single person, multi-member, mixed dietary constraints, children, elderly).
- Test all Critical scenarios explicitly: does the model ever produce output that conflicts with an active allergy?
- Evaluate explanation quality: does the model produce meaningful, accurate explanations for its outputs?
- Evaluate confidence calibration: does a confidence score of 0.9 actually correspond to correct outputs 90% of the time?

### Model Change Policy

- A model change that affects Critical or High outputs requires an explicit evaluation sign-off before deployment.
- A model change that affects only Low outputs may be deployed with standard CI/CD gates.
- All model changes are logged with the deployment event for audit purposes.

---

## AI Quality Metrics

| Metric | Target | Notes |
|---|---|---|
| Allergy Guard false negative rate | 0% | Any allergy conflict that reaches the user is a critical failure |
| Recommendation acceptance rate | > 60% | Accepted / (Accepted + Rejected + Ignored) |
| Explanation usefulness score | > 4.0 / 5.0 | User-rated; surfaced in feedback flow |
| Confidence calibration error | < 0.05 | Mean calibration error across all output types |
| High/Critical output with missing explanation | 0% | Every High+ output must carry an explanation |

---

## Children's Data

Households containing members with `age_group: child` or `age_group: infant` are subject to additional constraints:

- No behavioural data from child members is used in Collective Intelligence, even with household opt-in.
- AI recommendations for child members are always High criticality minimum.
- Child members cannot have individual goals set by AI inference — goals must be explicitly set by an adult household admin.
- Age-appropriate portion sizes and nutritional guidelines are applied using age group only. Medical or developmental conditions are never inferred.

---

## Bias Monitoring

The recommendation engine must be monitored for systematic bias across:

- Cuisine diversity (does the AI over-recommend one cuisine type?)
- Cost distribution (does the AI systematically recommend more expensive options?)
- Member goal equity (are some members' goals consistently deprioritised?)

Bias monitoring is a post-MVP operational concern. The framework is documented here so it is designed into the recommendation engine from the start.

---

## Related

- `Company/Operating_Principles.md` — Principles 1, 2, 4, 7
- GDR-001 — Trusted Decision Support, Not Autonomous Diagnosis
- GDR-002 — Privacy by Design
- PDR-009 — Household Conflict Resolution Policy (six-level hierarchy)
- ADR-007 — Household Intelligence Model as separate architectural layer
- `Products/KitchenOS/40_Technical_Architecture.md` — Household Decision Engine, Allergy Guard
- `Products/KitchenOS/20_Domain_Model.md` — Intelligence Layer section
