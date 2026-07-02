---
id: GDR-001
title: Trusted Decision Support, Not Autonomous Diagnosis
type: gdr
status: accepted
owner: founders
scope: company-wide
applies_to: [KitchenOS, HealthOS, FinanceOS, LearningOS, all future products]
depends_on: []
referenced_by: [PDR-001, PDR-007, PDR-008, PDR-009]
tags: [ai-governance, medical-advice-boundary, decision-support, autonomous-ai, company-wide, trusted-intelligence]
date: 2026
---

# GDR-001: Trusted Decision Support, Not Autonomous Diagnosis

**Type:** GDR (Governance Decision Record)
**Status:** Accepted
**Scope:** Company-wide — applies to all current and future products
**Date:** 2026
**Deciders:** Founding team

> **GDRs are company-wide policies. They are not superseded by PDRs or ADRs. A PDR may specify how a product implements this principle, but may not override it.**

---

## Context

As we build AI-powered products that touch health, food, finance, education, and other consequential domains, we must define a clear and enduring position on what our AI is — and what it is not.

The risk is real and specific:

- A meal recommendation that fails to account for an undetected medical condition.
- A nutrition suggestion interpreted as medical advice by a user with a serious illness.
- A financial guidance feature that a user treats as professional financial advice.
- An expert recommendation on our marketplace that causes harm.

The question is not whether our AI will ever be wrong. It will be. The question is: **when it is wrong, what is the nature of the failure, and who bears responsibility?**

The answer depends entirely on how we position the product and what safeguards we build. A product that presents itself as a decision support tool — one that assists human judgment — is categorically different from a product that presents itself as an autonomous diagnostic or prescriptive system.

This is not primarily a legal decision. It is a product identity decision. We are building trusted intelligence that amplifies human agency. We are not building a system that replaces it.

---

## Decision

**All products we build will be positioned, designed, and implemented as trusted decision support tools — not as autonomous diagnostic, prescriptive, or advisory systems in regulated domains.**

Specifically:

- **KitchenOS recommends. It does not diagnose.**
- **KitchenOS suggests. It does not prescribe.**
- **KitchenOS assists decisions. People make them.**

This applies to all current and future products in all domains.

---

## What This Means in Practice

### What AI systems in our products may do

- Generate meal, shopping, financial, or learning recommendations based on household context.
- Surface relevant information to support a decision.
- Provide confidence scores and explain the basis for recommendations.
- Flag potential issues (an ingredient that conflicts with a stated restriction, a budget item that exceeds a limit).
- Learn from user behaviour and refine future recommendations.

### What AI systems in our products may never do

- Present output as a medical, nutritional, financial, legal, or professional diagnosis.
- Act on safety-critical decisions without explicit user confirmation.
- Bypass or override safety checks (Allergy Guard, safety rules) on the basis of AI confidence.
- Autonomously modify household state (pantry, meal plan, shopping list, budget) without user confirmation on any High or Critical decision.
- Claim certainty on recommendations that are probabilistic.

### The language test

Before any AI output reaches a user, apply this test:

> Does this output read as "here is what we suggest and why" or "here is what you must do"?

The former is permitted. The latter is not, regardless of how confident the AI is.

---

## Decision Criticality Framework

Not all recommendations carry the same risk. This GDR establishes a four-level criticality framework that governs how AI outputs are handled across all products:

| Level | Examples | Safeguard required |
|---|---|---|
| **Low** | Suggest pasta for dinner, recommend apples | AI may recommend automatically |
| **Medium** | Substitute one ingredient for another, adjust shopping list | Recommend with explanation; user sees reasoning |
| **High** | Meal for a member with known allergies, calorie reduction suggestion, recipe modification for a specific goal | Explicit user confirmation required before any action |
| **Critical** | Any recommendation that conflicts with a safety rule; anything affecting a medical restriction; anything an expert has flagged as requiring their approval | Never autonomous; safety check must pass; explicit confirmation required; expert involvement may be mandated |

This framework is implemented in `Knowledge/85_Governance/AI_Governance.md`. Product and engineering teams must map every AI output to a criticality level before implementation.

---

## Reasons

- **Legal risk reduction**: positioning as decision support rather than diagnosis is the clearest way to remain outside the scope of medical device regulations, financial advice regulations, and professional licensing requirements in most jurisdictions.
- **Trust architecture**: users who know the AI is *suggesting* rather than *deciding* are more likely to engage critically, catch errors, and maintain trust when the AI is wrong.
- **Expert marketplace integrity**: experts on our marketplace give professional advice. Our AI must not compete with or undermine that advice by presenting AI output as equivalent. The AI assists; the expert advises; the user decides.
- **Company identity**: "trusted intelligence" as a brand promise requires that trust be earned through transparency and human agency, not through AI assertiveness.
- **Future-proofing**: AI regulations globally are moving toward requiring explainability, human oversight, and clear accountability for consequential AI outputs. This decision positions us ahead of that regulatory direction.

---

## Alternatives Considered

### Option A: Position as an AI assistant with professional-grade output

Present recommendations with professional authority ("As a nutritional AI, we recommend...").

Rejected because: this conflates AI probabilistic output with professional accountability. It creates regulatory exposure and, more importantly, sets user expectations that cannot be reliably met. Trust failures at this level of claimed authority are catastrophic.

### Option B: Differentiate by domain (medical = decision support; food = autonomous)

Apply the decision support principle only to explicitly medical or regulated domains; allow more autonomous behaviour in lower-stakes domains like food.

Rejected because: the boundaries between domains are not clear in practice. Food recommendations touch allergies, medical restrictions, goal-based nutrition, and expert advice. A "lower-stakes" food recommendation can be critical for a user with a severe allergy or a serious health condition. The principle must apply uniformly.

### Option C: Decision support as the company-wide principle (chosen)

Apply the principle to all products and all domains. Implement the criticality framework to calibrate safeguards appropriately without being uniformly restrictive.

This preserves the company identity while allowing the product to be genuinely helpful at low criticality levels without unnecessary friction.

---

## Consequences

### Positive

- Clear regulatory positioning in all markets and all domains.
- Product language, AI prompts, UX copy, and expert marketplace terms all align to a single principle.
- Expert marketplace participants understand their role: they advise, the AI assists, the user decides.
- Engineers have a clear test for every AI output they implement.
- Future products (HealthOS, FinanceOS, LearningOS) are governed by the same principle from day one.

### Negative

- Some features that would be possible in a more autonomous model will not be built, or will require additional confirmation steps. This is a deliberate tradeoff.
- The criticality framework requires ongoing maintenance as new features are added. Every new AI output must be classified.

### Scope Boundary

- This GDR governs AI outputs and product positioning. It does not govern the technical architecture of the AI systems (see ADR-007, ADR-008).
- The specific implementation of the criticality framework for KitchenOS is in `Knowledge/85_Governance/AI_Governance.md`.
- The household conflict resolution policy (how competing constraints are prioritised in recommendations) is a product decision — see PDR-009.

---

## Related

- `Company/Operating_Principles.md`, Principles 1 and 2
- `Knowledge/85_Governance/AI_Governance.md` — implementation of the criticality framework
- `Knowledge/10_Product_Vision.md`, Section 8.13 — AI predicts the routine, asks only about exceptions
- `Knowledge/20_Domain_Model.md`, Actor Model — Support Agent, Expert, AI actor definitions
- ADR-007 — Household Intelligence Model as separate architectural layer
- PDR-007 — Three-object meal lifecycle (MealRecommendation → MealPlan → MealSession)
- PDR-009 — Household Conflict Resolution Policy
