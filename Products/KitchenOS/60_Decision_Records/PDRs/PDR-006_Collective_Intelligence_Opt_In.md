---
id: PDR-006
title: Collective Intelligence Participation is Explicit Opt-In, Never Default
type: pdr
status: accepted
owner: product
depends_on: [PDR-001, PDR-002]
referenced_by: []
tags: [collective-intelligence, consent, privacy, trust, product-philosophy, opt-in]
date: 2026
---

# PDR-006: Collective Intelligence Participation is Explicit Opt-In, Never Default

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product

---

## Context

KitchenOS's Collective Intelligence Model (Section 54A, Product Vision) learns from anonymised household observations — price signals, recipe outcomes, pantry depletion rates, food waste patterns — contributed across the user base. This collective learning improves recommendations for every household, including new ones with thin personal history.

For the Collective Intelligence Model to work, households must contribute observations. The product decision is: **how should participation be structured?**

There are three common approaches in the industry:

1. **Opt-out (default on):** All users contribute by default unless they actively disable it. Used by many analytics and improvement programmes. Maximises data collection. Often buried in terms of service.
2. **Opt-in (default off):** Users are asked explicitly to participate and must take a positive action to contribute. Lower participation rates, but fully informed.
3. **Silent collection:** Data is collected without any user-facing consent mechanism, under broad terms of service coverage.

The choice is not purely a legal or compliance question. It is a product philosophy question that directly shapes the relationship KitchenOS has with its users.

---

## Decision

**We will require explicit opt-in for household participation in the Collective Intelligence Model. Contribution is off by default. No household observation is contributed to the collective model without a positive consent action from the household.**

This is a company principle, not just an implementation detail.

> **Collective intelligence is built through informed participation, never silent collection.**

---

## Reasons

**"Trust is earned through transparency" is a founding product principle.**
Silent collection — even of anonymised data — is inconsistent with a product that tells users what it has learned, lets them correct it, and gives them full control over household data. The trust model cannot be selective. If KitchenOS is transparent about what it knows about a household, it must also be transparent about what it shares from that household.

**Explicit opt-in is a long-term brand asset.**
The food and grocery category will face increasing scrutiny around data practices. Being the platform that asked first — clearly, honestly, and with user benefit framed accurately — is a differentiated position that compounds over time. It is much harder to recover from a "they were collecting our data silently" story than to build from a "they always asked" reputation.

**Informed participation produces better long-term data quality.**
Users who actively opted in are more likely to continue using the product in ways that generate useful signals, less likely to feel betrayed and churn, and more likely to advocate for the product. Coerced or uninformed participation produces more data short-term but worse product relationships long-term.

**The consent model must survive regulatory scrutiny.**
GDPR, CCPA, and emerging privacy regulations increasingly require genuine consent for data sharing beyond what is necessary to deliver the core service. An explicit opt-in design is more defensible in any regulatory environment than opt-out or silent collection, regardless of current minimum requirements.

**The opt-in framing can be compelling without being manipulative.**
The consent prompt can honestly communicate real user benefit: "Help us tell you where chicken is cheapest in your area this week. Your data is anonymised and never linked to you." This is true, meaningful, and likely to achieve reasonable opt-in rates without misleading users.

---

## Consent Design Requirements

The opt-in must be:

- **Post-onboarding:** Never presented during the initial onboarding flow. Users must experience product value before being asked to contribute to improving it for others.
- **Triggered by first meaningful action:** Present the opt-in prompt after the first receipt scan, first completed meal, or first week of active use — when the user has seen what the product can do.
- **Honest about what is shared:** The prompt must describe what categories of observations are contributed (prices, recipes, pantry patterns) in plain language.
- **Easy to decline:** Declining must be as easy as accepting. No dark patterns, no guilt framing, no repeated prompting after a user declines.
- **Revisable:** Users can change their participation status at any time from Household settings.
- **Transparent about scope:** Users can see what categories of observations are currently being contributed.
- **Reversible:** Opting out removes previously contributed observations from the learning pipeline (subject to technical feasibility of batch deletion).

---

## Alternatives Considered

### Option A: Opt-out (default contribution, user can disable)

All households contribute by default. An opt-out setting is available in account or privacy settings.

Rejected because:
- Inconsistent with "Trust is earned through transparency." Most users will not notice the default-on setting, which means their data is being used without genuine awareness.
- Contradicts the product's explicit commitment to user control and explainability.
- Creates regulatory risk as privacy standards tighten globally.
- If discovered by users or press, the reputational damage far outweighs the short-term data volume benefit.

### Option B: Silent collection under broad terms of service

Include data sharing in the terms of service without a specific consent prompt. Standard industry practice for many analytics and improvement programmes.

Rejected because:
- Legally defensible in some jurisdictions today but increasingly not in others.
- Fundamentally incompatible with the product principle that the AI is not a black box.
- A product that tells users "here is what I know about you, correct me if I'm wrong" cannot simultaneously be collecting and sharing that data without their specific awareness.

### Option C: Mandatory participation as a condition of free tier

Require collective data contribution as the "price" of free access; offer a paid tier that is private-only.

Rejected because:
- Misaligns the product's value proposition. KitchenOS earns trust; it does not extract data as a toll.
- Creates a two-tier trust model that undermines the product philosophy for the majority of users.
- Deferred — could be reconsidered at scale if a genuine privacy-premium tier has product market fit, but should not be the founding model.

---

## Consequences

### Positive

- Fully consistent with "Trust is earned through transparency" — the product's most important trust-building principle.
- Defensible under current and anticipated privacy regulation in major markets.
- Long-term brand differentiation: KitchenOS is the platform that asked.
- Users who opt in are more engaged and more likely to generate high-quality signals.

### Negative

- Lower initial participation rates compared to opt-out or silent collection means the Collective Intelligence Model takes longer to accumulate useful signal density.
- Requires investment in a clear, honest, and well-designed consent experience — not a checkbox buried in settings.
- Opt-out deletion pipeline adds engineering complexity (see ADR-008).

### Scope Boundary

- This decision governs contribution to the Collective Intelligence Model only. Household-level analytics used internally to improve the product (not contributed to a shared model) are governed separately by the privacy policy and standard analytics practices.
- This decision does not prevent Amanaska from building a paid privacy tier in the future, but that is not the founding model.

---

## Related

- PDR-001: Food Decisions Before Fitness (product boundary — household data is used for food decisions first)
- PDR-002: Household as Primary Unit (the unit of contribution is the household, not the individual)
- ADR-008: Collective Intelligence Model with Explicit Opt-In Consent (architectural implementation)
- `Knowledge/10_Product_Vision.md`, Section 54A: Collective Intelligence and Strategic Moat
- `Knowledge/40_Technical_Architecture.md`, Section 36A: Collective Intelligence Architecture
