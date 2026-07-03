---
id: GDR-002
title: Privacy by Design
type: gdr
status: accepted
owner: founders
scope: company-wide
applies_to: [KitchenOS, HealthOS, FinanceOS, LearningOS, all future products]
depends_on: []
referenced_by: [ADR-009, ADR-011]
tags: [privacy, data-minimisation, identity-isolation, consent, company-wide, gdpr, privacy-by-design]
date: 2026
---

# GDR-002: Privacy by Design

**Type:** GDR (Governance Decision Record)
**Status:** Accepted
**Scope:** Company-wide — applies to all current and future products
**Date:** 2026
**Deciders:** Founding team

> **GDRs are company-wide policies. They are not superseded by PDRs or ADRs. A PDR or ADR may specify how a product implements this principle, but may not override it.**

---

## Context

Our products handle sensitive personal data: dietary restrictions, allergies, health goals, household composition, financial patterns, learning progress. Users trust us with information they would not share publicly.

Privacy regulations globally (GDPR, CCPA, PDPA, and equivalents) impose legal obligations. But this GDR is not primarily about legal compliance. It reflects a product identity position: **we are a trusted intelligence company, and trust requires that users have genuine control over their data.**

Privacy must be embedded in product and architecture decisions from the start — not retrofitted when a regulation demands it or a breach occurs.

---

## Decision

**Privacy is designed in from the first line of architecture, not added as a compliance layer. Every product we build will implement the following seven principles.**

---

## The Seven Privacy by Design Principles

### 1. Collect only what you need

Every data field must have a clear answer to: *what decision, recommendation, or safety check does this field enable?*

If there is no clear answer, the field is not collected. Age group (`adult | teen | child | infant`) is sufficient for nutrition estimation. An exact birth date is not collected. Height and weight are collected only when an active goal requires them, and deleted when the goal is removed.

### 2. Separate identity from domain from intelligence

Three physically separate layers, each with its own schema:

- **Auth layer**: email, auth provider. The only PII. Never read by domain logic or AI.
- **Domain layer**: allergies, goals, household relationships. Authoritative facts. Never contains AI beliefs.
- **Intelligence layer**: learned preferences, confidence scores, behavioural patterns. Never contains PII or domain facts.

A breach of one layer must not expose another. The recommendation engine never receives email or name — only `person_id` and `household_id`.

This principle is implemented architecturally in ADR-009.

### 3. Consent is explicit and granular

Consent is required before any data is used beyond its primary purpose.

- Collective Intelligence participation: explicit opt-in, never default. See PDR-006.
- Expert data access: scoped to named data types, time-bounded, revocable. See `ConsentGrant` in Domain Model.
- Data retention: explicit policy, documented in `Knowledge/85_Governance/Risk_Register.md`.

### 4. Give users visibility and control

Users must be able to:
- See what data is held about them.
- Understand what the AI has learned about their household.
- Correct any inference they believe is wrong.
- Delete any sub-model from the Household Intelligence Model.
- Export their data.
- Delete their account and all associated data.

This is a product requirement, not just a legal obligation. See Intelligence Layer transparency requirements in `Products/KitchenOS/20_Domain_Model.md`.

### 5. Minimise data in motion

Data is scoped to the smallest context that requires it. `person_id` and `household_id` travel through the system — never name or email. Collective Intelligence anonymisation strips `household_id` before aggregation.

### 6. Privacy posture scales with sensitivity

Not all data requires the same protection. A household timezone requires less protection than an allergy. A pantry item requires less protection than a health goal. Data handling, access controls, retention, and audit logging must be calibrated to the sensitivity of the data, not applied uniformly at the lowest common denominator.

### 7. Breach containment is a design requirement

Every service boundary, every schema separation, and every access control decision must be evaluated through the lens of: *if this layer is breached, what is exposed?*

The answer must always be: only the data in that layer. Cross-layer exposure is a design failure, not an operational incident.

---

## Reasons

- **User trust**: users who trust KitchenOS with their household's dietary restrictions and health goals are making a significant privacy decision. That trust must be reciprocated with genuine data stewardship.
- **Regulatory coverage**: the seven principles above satisfy the core requirements of GDPR (lawful basis, data minimisation, purpose limitation, user rights, breach notification) and are directionally aligned with CCPA, PDPA, and emerging AI regulations.
- **Architecture integrity**: identity isolation and schema separation are architectural decisions that improve security, testability, and system resilience independent of privacy benefits.
- **Future products**: HealthOS, FinanceOS, and LearningOS will all handle data at least as sensitive as KitchenOS. Establishing the principle now means it is inherited, not reinvented.

---

## Alternatives Considered

### Option A: Compliance-driven privacy (meet legal minimums)

Implement privacy controls reactively as regulations require them, market-by-market.

Rejected because: this produces inconsistent user experiences across markets, creates significant rework costs as regulations evolve, and conflicts with the company identity of "trusted intelligence." Trust cannot be earned by meeting legal minimums.

### Option B: Privacy by Design from day one (chosen)

Embed privacy principles into every architecture decision, every data model, and every product feature from the start.

The upfront cost is higher. The long-term cost — in user trust, regulatory risk, and architectural debt — is far lower.

---

## Consequences

### Positive

- Architecture decisions (schema separation, identity isolation, data minimisation) that benefit privacy also benefit security and testability.
- Strong regulatory positioning in GDPR jurisdictions from launch.
- User trust as a genuine competitive advantage, not just a marketing claim.
- Future products inherit the principles without needing to rebuild them.

### Negative

- Some features are more complex to build (e.g., Collective Intelligence anonymisation pipeline, ConsentGrant scoping).
- Data deletion is more complex when data is used in derived intelligence models — the intelligence layer must be rebuilt or pruned when a user deletes their account.

### Scope Boundary

- This GDR governs principles. The technical implementation is in ADR-009 (identity isolation) and ADR-011 (Person as global domain concept).
- Data retention periods, specific deletion policies, and incident response procedures are in `Knowledge/85_Governance/Risk_Register.md` and `Knowledge/100_Security/`.
- GDPR/CCPA specific compliance procedures are in `Knowledge/100_Security/`.

---

## Related

- `Company/Operating_Principles.md`, Principle 3
- ADR-009 — Privacy-by-design and identity isolation (architectural implementation)
- ADR-011 — Person as a global domain concept
- PDR-006 — Collective Intelligence participation is explicit opt-in
- `Products/KitchenOS/20_Domain_Model.md` — Privacy-by-Design Principle section and Intelligence Layer transparency requirements
- `Products/KitchenOS/40_Technical_Architecture.md`, Section 23 — Four-layer model and physical separation
