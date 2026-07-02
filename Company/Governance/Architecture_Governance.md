---
id: GOV-003
title: Architecture Governance
type: governance
status: active
owner: founders
scope: company-wide
applies_to: [KitchenOS, HealthOS, FinanceOS, LearningOS, all future products]
date: 2026
---

# Architecture Governance

> This document owns the rules for architecture governance across all Amanaska products. It is referenced by agents, engineers, and reviewers — but it is not owned by any of them. The governance exists independently of whoever enforces it.

Agents follow these rules. They do not define them.

---

## The Governing Principle

> **Agents contain behavior, not policy. Policies belong to the knowledge system.**

This means:
- Architecture governance rules live here, not in `Agents/Architect.md`.
- Every agent, engineer, and reviewer references this document.
- If the rules change, they change here — once — and every actor that references this document is immediately governed by the new rule.
- No agent owns governance. Agents enforce it.

This applies to all governance documents: `AI_Governance.md`, `Risk_Register.md`, GDRs, and this document.

---

## When an ADR is Required

Write an ADR when any of the following is true:

- A new external dependency or service is introduced (a new cloud service, AI provider, third-party SDK).
- A technology is replaced (switching from one database, queue, or provider to another).
- A module boundary changes (a module is split, merged, or a new bounded context is introduced).
- A cross-cutting architectural pattern is established (a new pattern for error handling, auth, caching, or event processing that will be used across modules).
- A decision that was previously informal becomes a standard (e.g., agreeing on a retry policy, connection pooling strategy, or API versioning scheme).
- A proposed design would deviate from an existing ADR — a superseding ADR is required before work proceeds.

## When an ADR is NOT Required

- Implementation details within a module (how a function is structured, variable names, algorithm choice for an internal problem).
- Library versions or minor tooling upgrades (unless they introduce a new architectural dependency).
- UI component choices within the established design system.

---

## ADR Lifecycle

```text
Proposed   → under discussion, not yet in effect
Accepted   → decision made, in effect
Superseded → a later ADR replaces this one (link to successor)
Deprecated → no longer relevant (document why)
```

An ADR is never deleted. Superseded ADRs are kept for historical context. They are part of the audit trail.

---

## ADR Quality Requirements

Every ADR must contain:

- **Context** — why this decision was needed; what problem it solves.
- **Decision** — what was decided, stated clearly.
- **Alternatives considered** — at minimum three, including the option of doing nothing.
- **Consequences** — what becomes easier, what becomes harder, what is now locked in.
- **Operating Principles** — which of the 10 Operating Principles this decision implements or trades off against. This is required, not optional.

An ADR that cannot cite at least one Operating Principle is probably not grounded in the company's purpose.

---

## Approval

- ADRs must be reviewed by at least one other engineer before being marked Accepted.
- Changes that affect two or more modules require a second reviewer.
- The founding team reviews ADRs that introduce new cloud services, new external AI providers, or external cost implications.
- No ADR that conflicts with GDR-001 or GDR-002 may be Accepted without founder sign-off.

---

## What Triggers a Review of Existing Architecture

The following events require reviewing affected ADRs and updating the Knowledge Map Source of Truth table:

- A module boundary changes.
- A new building block is introduced.
- A building block is extracted into a separate deployable service.
- A managed service is replaced.
- A principle is violated in practice and a deliberate exception is agreed.
- A new product (HealthOS, FinanceOS, etc.) is started — existing ADRs should be reviewed for cross-product applicability.

---

## Architecture Review Board

At founding stage, the Architecture Review Board is the two founders. As the team grows:

- The Architect Agent or designated Lead Architect chairs reviews.
- Any engineer may propose an ADR.
- No single person approves their own ADR.
- A second reviewer (human or agent) is always required.

---

## Relationship to Other Governance Documents

| Document | Relationship |
|---|---|
| `Company/Operating_Principles.md` | Every ADR traces to at least one Operating Principle. This document is downstream of Operating Principles. |
| `Company/Governance/GDRs/GDR-001` | All AI architecture decisions must satisfy GDR-001. Architecture Governance enforces this at the ADR level. |
| `Company/Governance/GDRs/GDR-002` | All privacy and identity architecture decisions must satisfy GDR-002. Architecture Governance enforces this at the ADR level. |
| `Company/Governance/AI_Governance.md` | AI-specific architecture decisions (model selection, inference architecture, confidence handling) are additionally governed by AI_Governance.md. |
| `Templates/ADR_Template.md` | The canonical format for all ADRs. Follows the quality requirements defined here. |
| `Agents/Architect.md` | The Architect Agent enforces this document. It does not own it. |

---

## Related

- `Company/Operating_Principles.md` — the principles every ADR must trace to
- `Company/Governance/GDRs/` — company-wide governance policies
- `Company/Governance/AI_Governance.md` — AI-specific governance
- `Templates/ADR_Template.md` — the ADR format
- `Products/KitchenOS/60_Decision_Records/ADRs/` — KitchenOS decision history
