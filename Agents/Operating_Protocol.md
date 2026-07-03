---
id: AGENT-000
title: Role Operating Protocol
type: agent-protocol
status: active
owner: founders
scope: company-wide
applies_to: [all agent roles, human or AI]
date: 2026
---

# Role Operating Protocol

> This document defines how every Amanaska role operates, regardless of who fills it — an AI agent, a human, or a human working with an AI. Role manuals (`Architect.md`, `Product_Manager.md`, `Engineering_Manager.md`, and future roles) define *what* each role is responsible for; this document defines *how* every role works. Each role manual references this protocol instead of restating it.

A role manual defines a professional role, not a prompt. The same manual must work whether the role is filled by a person, a model, or both.

---

## Thinking Framework

Before producing any recommendation, decision, or artifact:

1. **Understand the problem** — restate it; if the request is ambiguous, resolve the ambiguity before working.
2. **Read existing knowledge** — the role's Inputs list first, then follow references. Never work from memory of a document; read the current version.
3. **Search for precedent** — existing decision records, patterns, and prior art in the repo. A decision that contradicts precedent requires superseding it, not ignoring it.
4. **Check Operating Principles and governance** — `Company/Operating_Principles.md`, applicable GDRs, and the governance documents for the role's domain.
5. **Consider alternatives** — at minimum three, including doing nothing.
6. **Evaluate trade-offs** — using the decision criteria owned by the role's governance documents (e.g., Decision Priorities in `Company/Governance/Architecture_Governance.md`).
7. **State confidence** — see Confidence Reporting below.
8. **Produce the output** — in the format the role's manual specifies, in the location it specifies.

---

## Confidence Reporting

Every recommendation from every role must state confidence explicitly, with its basis:

| Level | Meaning | Basis required |
|---|---|---|
| **High** | Strong precedent in existing decision records, or the conclusion follows directly from governance | Cite the precedent or rule |
| **Medium** | Reasoned judgment consistent with principles, but no direct precedent | State the reasoning and what evidence would change it |
| **Low** | A judgment call between defensible options, or made under significant unknowns | State the unknowns; flag for human review |

A Low-confidence recommendation is never presented as settled. Presenting uncertainty as certainty violates Principle 5 (Earn Trust Through Transparency) and Principle 7 (Truth Before Convenience).

This is the role-level counterpart of the product rule in `Company/Governance/AI_Governance.md` (Confidence and Explanation Requirements): the product's AI must tell users how confident it is; every role must tell its reviewers the same.

---

## Universal Escalation Rules

These apply to every role, in addition to the role manual's specific escalation table:

- **Conflict with governance** — if the requested work would violate a GDR or governance document, block and escalate. Do not produce a compliant-looking workaround.
- **Tied alternatives** — if two options remain genuinely tied after applying the role's decision criteria, document both and escalate. Do not pick arbitrarily.
- **Authority boundary** — if the work belongs to another role's authority, hand it off. Do not decide across the boundary.
- **Rule ambiguity** — if a governance rule is ambiguous as applied to the situation, escalate the ambiguity so the rule's owner can clarify it in the rule's home. Do not privately interpret.

---

## Working with Records and Living Documents

Documentation Philosophy rule 7 (`00_Knowledge_Map.md`) divides every artifact into two classes. Every role treats them oppositely:

- **Decision records** (types listed in `enforced_decision_types`, `Company/Governance/Architecture_Governance.md`): append and annotate only — History rows, amendment notes, `referenced_by` edges, lifecycle status changes via the PR ceremony. Never rewrite accepted content. A role asked to "fix" or "update" an accepted record's substance escalates: the correct instrument is an amendment or a superseding record.
- **Living documents** (everything else governed): the duty runs the other way — keep them current. Edit, simplify, reorganize, remove obsolete content through the normal PR flow. When a record is accepted or amended, update every living document it affects in the acceptance follow-up; a living document that lags its records is a defect, not history.

Which class a document belongs to is derived from its `type:` frontmatter — it is never declared separately.

---

## Relationship to Other Documents

| Document | Relationship |
|---|---|
| Role manuals (`Agents/*.md`) | Define each role's responsibilities, inputs, outputs, and authority. All inherit this protocol. |
| `Company/Operating_Principles.md` | The principles steps 4 and 7 check against. |
| `Company/Governance/` | Owns the rules roles enforce. Roles contain behavior, not policy. |
| `Process/Product_Development_Lifecycle.md` | The stages within which roles produce their outputs. |

---

## Related

- `Agents/Architect.md`, `Agents/Product_Manager.md`, `Agents/Engineering_Manager.md` — the current role manuals
- `Company/Governance/Architecture_Governance.md` — Decision Priorities and ADR rules
- `Company/Governance/AI_Governance.md` — product-level confidence and explanation requirements
