---
id: SD-XXX
title: [Feature Name] — Solution Design
type: solution-design
status: draft | in-review | accepted
feature: [PRD-XXX or feature name]
depends_on: [ADR-XXX, PDR-XXX]
tags: []
date: YYYY-MM-DD
---

# SD-XXX: [Feature Name] — Solution Design

**Type:** Solution Design (Low-Level Design)
**Status:** Draft | In Review | Accepted
**Date:** YYYY-MM-DD
**Author:** [Name or role]
**Reviewer:** [Name or role]
**Stage Gate:** Stage 5 — Technical Design

> **Scope:** This document covers the module-level design for [feature]. System-level architecture is in `Products/KitchenOS/40_Technical_Architecture.md`. This document describes *how* this feature is built, not *why* the architectural choices were made (that is in the relevant ADRs).

---

## Feature Summary

One paragraph: what does this feature do, what user need does it serve, and what is the intended user outcome?

Reference the PRD: `Products/KitchenOS/30_PRDs/[PRD-XXX]`

---

## Affected Building Blocks

List the architectural building blocks from `00_Knowledge_Map.md` (Architecture Building Blocks section) that this feature touches:

| Building Block | Nature of change |
|---|---|
| [e.g. Household Decision Engine] | [e.g. Adds new recommendation type] |
| [e.g. Domain Event Bus] | [e.g. New event: MealRecommendationAccepted] |

---

## Domain Events

New domain events introduced or modified by this feature:

| Event | Trigger | Payload fields | Criticality |
|---|---|---|---|
| `[context.entity.action]` | [what causes this event] | [key fields] | Low / Medium / High / Critical |

All events must follow the Standard Event Envelope in `Products/KitchenOS/20_Domain_Model.md`.

---

## Data Model Changes

### New tables or columns

```sql
-- describe new schema additions here
```

### Modified tables

```sql
-- describe changes to existing schema here
```

### Four-layer impact check

| Layer | Affected? | Notes |
|---|---|---|
| Auth (identities) | Yes / No | |
| Person (persons, person profiles) | Yes / No | |
| Domain (household, pantry, meals, etc.) | Yes / No | |
| Intelligence (ai beliefs, confidence) | Yes / No | |

> **Invariant check:** Does this change risk reversing the dependency direction (intelligence depending on domain is correct; domain depending on intelligence is NOT)?

---

## Module Responsibilities

For each module involved, describe its responsibility in this feature:

### [Module Name]

**Responsibility in this feature:**
**Inputs:**
**Outputs:**
**Domain events consumed:**
**Domain events produced:**

---

## Architecture Fit

- **Bounded context:** which context this feature lives in (`Products/KitchenOS/20_Domain_Model.md`)
- **Backend module:** which NestJS module handles this
- **Flutter layer:** which feature folder / Riverpod provider manages this
- **New infrastructure:** any new GCP services, queues, or storage (if yes: ADR trigger — check `Company/Governance/Architecture_Governance.md`)

---

## Sequence Diagram

```text
[Actor/Client]          [Service/Module]          [Database]

      │                        │                       │
      │── [Action] ──────────► │                       │
      │                        │── [Query] ───────────►│
      │                        │◄─ [Result] ───────────│
      │                        │── [Write Event] ─────►│
      │◄─ [Response] ──────────│                       │
```

---

## AI Decision Criticality

If this feature produces AI output:

- **Criticality level:** Low | Medium | High | Critical (reference `Company/Governance/AI_Governance.md`)
- **Allergy Guard required:** Yes / No
- **Explanation field required:** Yes / No
- **Explicit user confirmation required:** Yes / No
- **Safeguard implementation:** [how the criticality level is enforced in code]

---

## Error Cases and Edge Cases

| Case | Expected behaviour |
|---|---|
| [e.g. AI returns no results] | [e.g. Show empty state, do not show low-confidence fallback] |
| [e.g. Network unavailable] | [e.g. Serve last cached recommendation with staleness indicator] |
| [e.g. Allergy Guard blocks all options] | [e.g. Explain to user why no options are shown; do not silently degrade] |

---

## Security Considerations

- What authorization checks are required? (household membership, role, consent)
- Does this feature access PII?
- Are there new consent requirements?
- Does this require a security review before Stage 7?

---

## Privacy Impact

- Does this feature collect any new data? If yes, justify against GDR-002 (data minimisation).
- Does any new data flow through the AI layer? If yes, confirm no PII is included.
- Does this feature require a new or modified ConsentGrant?

---

## API Contract

Endpoints introduced or modified. Full request/response/error schemas per endpoint:

| Method | Path | Purpose | Error cases |
|---|---|---|---|
| POST | /example | ... | 400, 403, 409 |

---

## Module Responsibilities

| Module / Layer | Responsibility |
|---|---|
| `[feature].controller.ts` | HTTP interface, request validation |
| `[feature].service.ts` | Business logic, orchestration |
| `[feature].repository.ts` | Database access, query logic |
| `[feature]_provider.dart` | Flutter state management (Riverpod) |
| `[feature]_screen.dart` | Flutter UI layer |

---

## Offline Behaviour

- Does this feature work offline? Yes / No / Partial
- If partial: what works offline and what requires connectivity?
- How are pending sync events handled for this feature?
- Conflict resolution strategy when offline and online states diverge?

---

## Testing Strategy

| Test Type | What to Test | Tool |
|---|---|---|
| Unit tests | Service logic, business rules | Jest |
| Integration tests | API endpoints end-to-end | Supertest + Testcontainers |
| BDD scenarios | Acceptance criteria from PRD | As defined in PRD |
| Flutter widget tests | UI states (empty, loading, error, data) | flutter_test |
| Flutter golden tests | Visual regression for new components | golden_toolkit |

---

## Acceptance Criteria (Technical)

BDD format. These are the technical acceptance criteria that engineering tests against. User-facing BDD scenarios are in the PRD.

```gherkin
Given [technical precondition]
When [technical action]
Then [verifiable technical outcome]
```

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | [question] | [who needs to answer] | Open / Resolved |

---

## Related

- PRD: `Products/KitchenOS/30_PRDs/[PRD-XXX]`
- Technical Architecture: relevant sections
- ADRs: any ADRs governing decisions in this design
- GDRs: GDR-001 and/or GDR-002 if relevant
