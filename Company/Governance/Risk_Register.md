---
id: GOV-002
title: Risk Register
type: governance
status: active
owner: founders
scope: KitchenOS
review_cadence: quarterly
date: 2026
---

# Risk Register

> This is a living document. Review quarterly or when a new risk materialises. Risks are never deleted — closed risks are marked `Closed` with a resolution note.

---

## Risk Categories

```text
Business          product, competitive, market
Regulatory        legal compliance, jurisdiction-specific
Privacy           data protection, consent, breach
Security          auth, access control, infrastructure
AI                recommendation quality, bias, autonomy
Marketplace       expert credentials, disputes, quality
Operational       support, incident response, reliability
Financial         payments, fraud, tax
```

---

## Active Risk Register

| ID | Category | Risk | Likelihood | Impact | Owner | Mitigation | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Privacy | Privacy breach exposing household health data | Medium | Very High | Architecture | Identity/domain/intelligence schema separation (ADR-009); least-privilege access; encrypted at rest and in transit | Active |
| R-002 | AI | Incorrect AI recommendation causes harm (allergy conflict, unsafe substitution) | Medium | Critical | Product + Engineering | Allergy Guard (hard block, Level 1 hierarchy); Critical criticality classification; explicit confirmation required; never autonomous (GDR-001, PDR-009) | Active |
| R-003 | Regulatory | Product positioned as medical advice by users or regulators | Medium | Very High | Founders | GDR-001 (decision support, not diagnosis); product language audit; UX copy review; expert marketplace terms | Active |
| R-004 | Marketplace | Expert gives unsafe or unqualified advice through platform | Low | High | Expert Operations | Credential verification at onboarding; ConsentGrant scope limits; KitchenOS Allergy Guard runs on all expert recommendations; user approval required before any household state change | Active |
| R-005 | AI | Pantry state becomes inaccurate, reducing AI recommendation quality | Medium | High | Product + Engineering | Pantry only updated on confirmed activities (ADR-010); correction events; user-visible staleness indicators; confidence score decay | Active |
| R-006 | Privacy | Children's data collected or used in Collective Intelligence | Low | High | Engineering | `age_group: child` excluded from Collective Intelligence pipeline; child AI outputs always High criticality minimum; no AI-inferred goals for children (AI Governance) | Active |
| R-007 | Regulatory | GDPR / CCPA non-compliance at launch in target markets | Medium | High | Founders | GDR-002 (Privacy by Design); data minimisation; explicit consent; user rights implementation (view, correct, delete, export); DPA engagement pre-launch in EU | Active |
| R-008 | AI | Recommendation engine develops systematic bias (cuisine, cost, demographic) | Medium | Medium | Product | Bias monitoring framework (AI Governance); acceptance/rejection rate tracking per demographic segment; quarterly review | Active |
| R-009 | Security | Unauthorised cross-household data access | Low | Very High | Engineering | Authorization evaluated server-side on every request; `household_id` resolved from JWT, never trusted from client; cross-household attempt rejected before query executes (Technical Architecture, Section 23B) | Active |
| R-010 | Operational | Support volume overwhelms founding team pre-product-market-fit | High | Medium | Founders | Customer & Expert Operations framework (`Products/KitchenOS/95_Customer_Expert_Operations/`); self-service correction and undo flows reduce support volume; Household Timeline gives users context to self-resolve | Active |
| R-011 | Marketplace | Expert credential expires or is revoked post-onboarding | Low | High | Expert Operations | Credential expiry tracking in Expert Operations; automated re-verification prompts; ConsentGrant revocation if credential lapses | Active |
| R-012 | Financial | Payment fraud or tax compliance in Expert Marketplace | Low | Medium | Founders | Use payment provider (Stripe or equivalent) that handles PCI compliance and tax; KitchenOS does not store payment data; marketplace financial compliance reviewed before Expert Marketplace launch | Active |
| R-013 | Business | Trust erosion from repeated poor AI recommendations | Medium | High | Product | Recommendation quality metrics (acceptance rate, confidence calibration); Household Timeline gives users visibility; correction events feed back to learning engine; explicit confidence indicators | Active |
| R-014 | AI | Collective Intelligence model propagates biased household data at scale | Low | High | Architecture | Explicit opt-in only (PDR-006); anonymisation pipeline strips household_id; collective model is separate from household intelligence; model evaluation framework (AI Governance) | Active |

---

## Closed Risks

| ID | Risk | Closed Date | Resolution |
|---|---|---|---|
| *(none yet)* | | | |

---

## Risk Review Log

| Date | Reviewer | Changes Made |
|---|---|---|
| 2026 | Founding team | Initial register created |

---

## How to Use This Register

**Adding a new risk:**
1. Assign the next available R-ID.
2. Classify the category.
3. Assess likelihood (Low / Medium / High) and impact (Low / Medium / High / Very High / Critical).
4. Assign an owner (a role, not a person name).
5. Document the current mitigation — even if it is partial.
6. Set status to Active.

**Reviewing an existing risk:**
- Update `Mitigation` when new controls are implemented.
- Change `Status` to `Closed` only when the risk is fully mitigated or no longer applicable.
- Never delete a row — closed risks provide audit history.

**Quarterly review checklist:**
- [ ] Are all Active risks still relevant?
- [ ] Have mitigations been implemented as planned?
- [ ] Are there new risks from product changes, new features, or regulatory developments?
- [ ] Are Likelihood and Impact assessments still accurate?
