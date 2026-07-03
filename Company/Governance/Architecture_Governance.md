---
id: GOV-003
title: Architecture Governance
type: governance
status: active
owner: founders
scope: company-wide
applies_to: [KitchenOS, HealthOS, FinanceOS, LearningOS, all future products]
date: 2026
enforced_decision_types: [adr, pdr, uxdr, gdr]
enforced_section_types: [adr, pdr, uxdr]
enforced_required_sections: [Context, Decision, Alternatives Considered, Consequences]
enforced_decision_statuses: [proposed, accepted, superseded, deprecated]
enforced_principles_field: operating_principles
enforced_no_delete_dirs: [60_Decision_Records, GDRs]
enforced_history_section: History
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

## Machine-Readable Enforcement

The `enforced_*` fields in this document's frontmatter are the parameters CI enforces (`governance_check.py` reads them at runtime — it contains no rules of its own). The prose in this document and those fields are two views of the same rule and must change together, in the same commit. If they disagree, the prose is the intent and the frontmatter is a bug.

| Field | Enforces |
|---|---|
| `enforced_decision_types` | Which document types are decision records |
| `enforced_section_types` | Which decision records must carry the required sections |
| `enforced_required_sections` | ADR Quality Requirements — mandatory sections |
| `enforced_decision_statuses` | ADR Lifecycle — legal status values |
| `enforced_principles_field` | Every decision record cites Operating Principles |
| `enforced_no_delete_dirs` | ADR Lifecycle — records under these directories are never deleted, only Superseded or Deprecated |
| `enforced_history_section` | Recording State Changes — every decision record carries a History log of its state transitions |

---

## Decision Priorities

When evaluating architectural alternatives, prefer the option that maximises, in this order:

1. **Alignment with Operating Principles and GDRs** — an option that conflicts with a principle or GDR is disqualified, not deprioritised.
2. **Domain correctness** — respects bounded contexts, aggregate boundaries, business invariants, and the dependency direction. A simple design built on a wrong model is worse than a complex one on a correct model.
3. **Simplicity** — the least machinery that solves the problem (Principle 9: Simplicity Is a Feature). Prefer boring technology and existing patterns over new ones.
4. **Long-term maintainability and reversibility** — how hard is this to change or undo when we learn more?
5. **Reuse across products** — does this create or strengthen a capability future products can share?
6. **Performance** — sufficient for the product requirement; optimise beyond that only with evidence.
7. **Cost** — infrastructure and operational cost, within the constraints above.

A lower criterion never outranks a higher one. If two alternatives are genuinely tied after applying all seven, that is an escalation: document both in the ADR and flag for human decision — do not pick arbitrarily.

This ordering exists so that different evaluators — human architects, AI agents, different AI models — optimise for the same things.

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

### Recording State Changes

Every state change is recorded in two places, with a clear division of roles:

- **The record itself is the authoritative account.** The `status:` frontmatter holds the current state. A **History** section (see the decision-record templates) logs every transition — date, change, who made it, and the evidence link. A decision record must be readable in isolation: knowing who accepted it and when must never require access to GitHub.
- **The pull request is the ceremony and the evidence.** A state change ships as a PR that flips the frontmatter, updates the record header, and adds the History row. The required review on that PR (enforced by CODEOWNERS and branch protection) is what satisfies "no single person approves their own ADR" — the reviewer's approval on the PR *is* the acceptance act, and the History row records its outcome.

If the History section and the PR trail ever disagree, the PR trail is the evidence and the History section is corrected to match it.

CI enforces the presence of the History section (`enforced_history_section`): an error for records changed in a pull request, a warning for pre-existing records until they are backfilled.

### Amendments (Partial Supersession)

A later record sometimes overtakes part of an earlier record's *rationale or context* without touching its *decision*. That is an **amendment**, not a supersession:

- A dated amendment note is added directly below the earlier record's header, in the standard form — every amendment reads identically for humans and parses identically for agents:

  > **Amended YYYY-MM-DD by ADR-XXX** — scope: [what is overtaken]; decision: unchanged. [One-sentence summary.] See History.
- A History row records the amendment.
- The earlier record's `referenced_by` gains the later record, so impact analysis flows in both directions.
- The original text is never edited — it remains what was true at decision time.

If the *decision itself* is overtaken, that is supersession: the whole record moves to `superseded` with a link to its successor.

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
