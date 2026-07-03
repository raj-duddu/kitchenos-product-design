---
id: PDR-005
title: Ask Only What the AI Cannot Reasonably Learn on Its Own
type: pdr
status: accepted
owner: product
depends_on: [PDR-002, PDR-003]
referenced_by: []
tags: [onboarding, household-intelligence-model, behavioural-learning, ux, product-philosophy, friction]
date: 2026
---

# PDR-005: Ask Only What the AI Cannot Reasonably Learn on Its Own

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product

---

## Context

KitchenOS needs household context to provide value from day one: who lives in the household, what constraints apply, what goals matter. The question is how much of this context should be collected during onboarding versus learned through observed behaviour over time.

Traditional food and grocery apps ask extensive onboarding questions: preferred cuisines, shopping days, typical cooking times, dietary preferences, favourite stores, weekly budget, and more. This approach treats onboarding as the primary mechanism for building household understanding.

The problem is threefold:
1. **Self-reported preferences are less accurate than observed behaviour.** People answer quickly, carelessly, or aspirationally during onboarding. What they say they prefer and what they actually do often differ within weeks.
2. **Long onboarding increases abandonment.** Every additional question is friction that reduces the number of users who reach the first moment of value.
3. **Most preferences can be learned reliably within weeks of use.** If the AI can learn that a household shops at Costco monthly by observing receipt scans, asking the question during onboarding adds no long-term value and adds short-term friction.

The product principle "Simplicity is a feature" applies directly to onboarding. The question is where to draw the line.

---

## Decision

**We will ask during onboarding only what the AI cannot safely or reliably learn on its own. Everything the AI can observe, it will learn — and confirm with the user when confident enough to ask.**

---

## The Rule

> **Ask only what the AI cannot reasonably learn on its own.**

Applied consistently, this produces a short, high-signal onboarding that collects only safety-critical and intention-critical information — then lets the AI earn the right to know more through observation.

---

## What to Ask vs What to Learn

| Signal | Approach | Reason |
|---|---|---|
| Allergies and dietary restrictions | **Ask** | Safety-critical. The AI must never guess something that could harm a household member. |
| Household size (adults, children) | **Ask** | Cannot be inferred reliably at the start. Required immediately for meal sizing and shopping estimates. |
| Primary goal (eat healthier, save money, reduce waste, manage medical diet) | **Ask** | Personal intention. Cannot be inferred from behaviour alone, especially at the start. Goals must be stated. |
| Cooking skill level | **Ask** | Calibrates recipe complexity from day one. Hard to infer quickly without risking poor early recommendations. |
| Preferred stores | **Ask** (lightweight) | Bootstraps shopping suggestions before receipt data exists. Can be updated as receipts are scanned. |
| Favourite cuisine | **Learn** | Emerges reliably from recipe acceptance, grocery purchases, and restaurant patterns within weeks. |
| Preferred shopping day | **Learn** | Visible from receipt scan timestamps within a few shopping cycles. |
| Typical cooking time | **Learn** | Observable from Cook Mode session durations. Confirm if needed after sufficient evidence. |
| Budget | **Ask if goal is "save money"** | Contextual — only ask if the household has stated budget as a goal. Otherwise learn it from spending patterns. |
| Whether they like mushrooms | **Learn, then confirm** | Never ask during onboarding. After enough rejections: "I've noticed you skip mushroom recipes. Recommend them less?" |

---

## How the AI Earns the Right to Know More

The AI does not ask preference questions during onboarding. It observes. When it has enough evidence to be confident, it surfaces what it has learned — and invites the user to confirm, correct, or forget it.

Example:

> After two months: "I have noticed you skip mushroom recipes. Should I recommend them less often?"

This is a much better experience than asking during onboarding because:
- The AI already knows the answer — it is confirming, not guessing.
- The user sees the AI is paying attention and learning, which builds trust.
- The question arrives in context, not as an abstract preference screen.

This behaviour is specified in the "KitchenOS Knows..." transparency screen in the Household Intelligence Model (Section 50A of Product Vision).

---

## Alternatives Considered

### Option A: Comprehensive onboarding questionnaire

Ask all preference questions upfront: cuisines, cooking time, shopping day, budget, meal frequency, dietary preferences beyond restrictions, and more.

Rejected because:
- Increases abandonment before the first moment of value.
- Self-reported preferences are less accurate than observed behaviour — the data is lower quality.
- Violates the product principle "Simplicity is a feature."
- Most of this data becomes available through use anyway, making the upfront collection redundant.

### Option B: Fully silent learning — ask nothing beyond account creation

Collect only the minimum for account creation (name, email) and learn everything else.

Rejected because:
- Safety-critical information (allergies) must never be inferred. A missed allergy is a product-ending failure.
- Without household size and goals, early recommendations will be generic and low-quality, damaging first impressions.
- Some context — especially goals — is intentional and must be stated, not observed.

### Option C: Progressive onboarding — ask questions over multiple sessions

Spread onboarding questions across the first week, asking one or two per session.

Partially accepted — but only for the confirmation pattern described above, not for asking questions the AI could learn through observation. The distinction is: questions the AI cannot learn go in structured onboarding. Questions the AI can learn go through the observational confirmation pattern.

---

## Consequences

### Positive

- Shorter onboarding reduces abandonment and gets users to first value faster.
- Behavioural data is more accurate and more current than self-reported preferences.
- The product feels intelligent from early use — it learns rather than interrogates.
- Reinforces "Trust is earned through transparency": the AI tells users what it has learned rather than silently acting on stale self-reported data.

### Negative

- Early recommendations (before behavioural data accumulates) rely more heavily on onboarding answers and collective intelligence signals, which are less personalised.
- The team must maintain clear documentation of which signals are asked vs learned, and must not add onboarding questions without applying the rule.

### Scope Boundary

- This decision governs the initial onboarding flow only. In-app profile screens allow users to update any preference at any time — this decision does not restrict that.
- The rule applies to preference signals. Account information (name, email, timezone) is always collected at account creation and is not covered by this rule.

---

## Related

- PDR-003: Home Screen Answers a Question (same philosophy — the product should reduce friction, not add it)
- `Products/KitchenOS/10_Product_Vision.md`, Section 50: Onboarding Strategy
- `Products/KitchenOS/10_Product_Vision.md`, Section 50A: Household Intelligence Model — Three Stages of Learning
- ADR-007: Household Intelligence Model Separation (the intelligence model stores what is learned)
