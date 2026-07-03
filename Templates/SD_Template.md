# SD-XXX: [Feature Name] — Solution Design

**SD ID:** SD-XXX
**PRD Reference:** PRD-XXX
**Status:** Draft | In Review | Approved
**Author:** [Engineer / Architect name]
**Tech Lead Review:** [Reviewer name]
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

> This document is the feature-level technical design (LLD) for [Feature Name]. It bridges the system-level architecture in `Products/KitchenOS/40_Technical_Architecture.md` and the actual code. It answers: **"How specifically is this feature designed at the module, class, and data level?"**

---

## Context

Brief summary of what this feature does and why it exists.
Reference: `Knowledge/30_PRDs/PRD-XXX_Feature_Name.md`

---

## Scope of This Design

What is and isn't covered by this Solution Design.

**In scope:**
-

**Out of scope:**
-

---

## Architecture Fit

How does this feature fit into the existing system architecture?

- **Bounded context:** Which bounded context does this feature live in? (Reference: `Products/KitchenOS/20_Domain_Model.md`)
- **Backend module:** Which NestJS module handles this?
- **Flutter layer:** Which feature folder / Riverpod provider manages this?
- **New infrastructure:** Any new GCP services, queues, or storage needed?

---

## Domain Model Changes

List any changes to the Domain Model required before implementation.

| Change | Type | Document |
|---|---|---|
| New entity: `ExampleEntity` | New | Update `Products/KitchenOS/20_Domain_Model.md` |
| New event: `ExampleHappened` | New | Update `Products/KitchenOS/20_Domain_Model.md` |
| Modified invariant: ... | Modified | Update `Products/KitchenOS/20_Domain_Model.md` |

---

## Data Model

### New Tables / Columns

```sql
-- Example
CREATE TABLE example_table (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id  UUID NOT NULL REFERENCES households(id),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### New Domain Events

```json
{
  "event_id": "uuid",
  "event_type": "ExampleHappened",
  "household_id": "uuid",
  "actor_user_id": "uuid",
  "occurred_at": "ISO8601",
  "payload": {},
  "source": "mobile|backend|ai",
  "learning_impact": "high|medium|low|none"
}
```

---

## Sequence Diagram

Key flows for this feature — use text-based sequence diagrams for version control friendliness.

### Flow 1: [Primary Happy Path]

```text
Mobile App          Backend API         Database
    │                    │                  │
    │── POST /example ──►│                  │
    │                    │── INSERT ────────►│
    │                    │◄─ OK ────────────│
    │◄── 201 Created ────│                  │
    │                    │                  │
```

### Flow 2: [Error / Edge Case]

```text
[describe error flow]
```

---

## API Contract

Endpoints introduced or modified by this feature.

### POST /example

**Request:**
```json
{
  "field": "value"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "field": "value",
  "created_at": "ISO8601"
}
```

**Error Responses:**
- `400` — Validation failure
- `403` — Insufficient permissions
- `409` — Conflict (e.g., duplicate)

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
- What is the conflict resolution strategy when offline and online states diverge?

---

## Security Considerations

- What authorization checks are required? (household membership, role, consent)
- Does this feature access PII?
- Are there new consent requirements?
- Does this require a security review before Stage 7?

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

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | ... | ... | Open |

---

## Approval

| Role | Name | Date | Decision |
|---|---|---|---|
| Tech Lead | | | Approved / Revisions needed |
| Architect | | | Approved / Not required |
