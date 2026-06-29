# PRD: [Feature Name]

**PRD ID:** PRD-XXX
**Status:** Draft | In Review | Approved | Shipped
**Owner:** [Product Owner name]
**Stage Gate:** Stage 3 of Product Development Lifecycle
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

---

## Problem Statement

> One sentence: what problem are we solving and for whom?

---

## Background / Discovery

What do we know about this problem? What have we learned from users, data, or research?

---

## Product Vision Alignment

Which Product Vision principles does this feature serve?
Reference: `Knowledge/10_Product_Vision.md`, Sections 1–9.

- Principle: ...
- Principle: ...

Does this increase Weekly Trusted Household Decisions Completed (North Star Metric)? How?

---

## Scope

### In Scope

-

### Out of Scope

-

### MVP Boundary

What is the minimum version that delivers the core value?

---

## User Stories

### Story 1: [Title]

**As a** [persona]
**I want to** [action]
**So that** [outcome]

**Acceptance Criteria:**
- [ ] ...
- [ ] ...

---

### Story 2: [Title]

...

---

## BDD Scenarios

### Scenario: [Scenario Name]

```gherkin
Given [initial context]
When [action taken]
Then [expected outcome]
```

---

## UX Notes

### Screen Flow

```text
[Screen A]
    │
    ▼
[Screen B]
    │
    ▼
[Confirmation]
```

### Empty State

What does the user see when there is no data?

### Error State

What does the user see when something goes wrong?

### Loading State

What does the user see while data is loading?

---

## Technical Design

> For simple features, a brief technical design section here is sufficient. For complex features (new services, significant data model changes, or non-trivial flows), create a full Solution Design document at `Knowledge/45_Solution_Designs/SD-XXX_Feature.md` using `Templates/SD_Template.md`.

### Key Technical Decisions

- ...

### Sequence / Flow (brief)

```text
[Mobile] → [API] → [DB]
```

### New API Endpoints (summary)

| Method | Path | Purpose |
|---|---|---|
| POST | /example | Create example |

Full API contract belongs in: `Knowledge/45_Solution_Designs/SD-XXX.md` or `Knowledge/80_API_Reference/`.

---

## Domain Model Impact

Does this feature introduce new entities, events, or rules?

- [ ] New entity: ...
- [ ] New domain event: ...
- [ ] New business invariant: ...
- [ ] No domain model changes.

If yes, update `Knowledge/20_Domain_Model.md` before Stage 7.

---

## Architecture Impact

- [ ] New API endpoint(s): ...
- [ ] New backend service or module: ...
- [ ] Database schema change: ...
- [ ] New infrastructure component: ...
- [ ] No architecture changes.

If yes, Architecture Review required (Stage 5). ADR may be needed.

---

## Security and Privacy

- [ ] Touches user PII: yes / no
- [ ] Touches household financial data: yes / no
- [ ] Requires new permissions or consent: yes / no
- [ ] Requires security review: yes / no

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | ... | ... | Open |

---

## Definition of Done

- [ ] All acceptance criteria verified by QA.
- [ ] BDD scenarios pass.
- [ ] Domain Model updated if changed.
- [ ] Architecture documentation updated if changed.
- [ ] Feature flagged for staged rollout.
- [ ] No critical bugs open.
