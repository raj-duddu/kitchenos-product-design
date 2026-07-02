---
id: KNOW-PAT-002
title: Event Sourcing
type: knowledge-pattern
status: active
owner: founders
scope: company-wide
related: [KNOW-PAT-001, KNOW-PAT-003]
date: 2026
---

# Event Sourcing

> This document captures the event sourcing pattern as applied across Amanaska products. For the KitchenOS-specific event architecture, see `Products/KitchenOS/40_Technical_Architecture.md`, Section 32.

---

## What Event Sourcing Is

Instead of storing the current state of an entity (e.g., pantry contains 2 apples), you store the sequence of events that led to that state (ReceiptScanned → PantryItemAdded × 6, MealCooked → PantryItemConsumed × 4). The current state is a derived read model — a materialised view computed from the event log.

```text
Traditional:      pantry_items { item_id, quantity: 2 }   ← mutable, no history
Event Sourcing:   domain_events [
                    { type: PantryItemAdded, item: apple, qty: 6 }
                    { type: PantryItemConsumed, item: apple, qty: 4 }
                  ]                                         ← immutable, full history
                  pantry_state { item: apple, qty: 2 }     ← derived read model
```

---

## Why We Use It

- **Household Timeline is a first-class product feature.** The event log is what the user sees. Without event sourcing, the timeline is a reconstruction problem. With it, the timeline is the log.
- **AI needs sequential history.** The intelligence layer learns from what happened, in what order, in what context. A mutable state model loses this. The event log preserves it.
- **Corrections are natural.** A correction event amends or reverses a prior event. The original event is preserved. The correction is explicit. There is no silent deletion. This gives users trust and the AI accurate history.
- **Auditability.** Every state change has a traceable cause — a command, an event, an actor, a timestamp. This is essential for safety (why did the AI recommend this?), debugging, and compliance.

---

## How We Apply It

### Append-only `domain_events` table

Every significant domain state change writes an event to `domain_events`. This is the canonical, immutable record.

```sql
domain_events (
  id            uuid primary key,
  household_id  uuid,
  event_type    text,       -- e.g. 'meal.recommendation.accepted'
  event_version integer,    -- schema version of this event type
  payload       jsonb,
  actor_id      uuid,       -- person_id or 'system'
  created_at    timestamptz
)
```

### Materialised state views

Current state (pantry, meal plan, shopping list) is derived from the event log and stored as materialised views or denormalised read tables. These are rebuilt from the event log on demand and treated as caches, not sources of truth.

### Correction events, not deletes

When a user undoes an action or the AI makes a correction:
- Write a `*Reversed` or `*Corrected` event
- Rebuild the materialised state
- Never delete the original event

### Event naming convention

```text
{context}.{entity}.{past_tense_action}

meal.recommendation.accepted
pantry.item.consumed
shopping.trip.confirmed
receipt.scanned
household.member.added
```

---

## What Event Sourcing Is Not

- It is not a log of everything. Logging infrastructure events (HTTP requests, errors) is separate. Domain events capture business meaning, not system activity.
- It is not a message queue. The `domain_events` table is a persistent store, not a transient queue. Events are written to it directly and processed from it.
- It is not a replacement for a domain model. The events express what happened. The domain model expresses what is true and what is allowed.

---

## Trade-offs

| Benefit | Cost |
|---|---|
| Full audit history | Schema evolution requires `event_version` on all events |
| Household Timeline for free | Materialised views must be kept in sync |
| Corrections are explicit | Developers must think in events, not mutations — steeper learning curve |
| AI gets sequential context | Event log grows over time — partitioning and archiving required at scale |

---

## Related

- `Products/KitchenOS/40_Technical_Architecture.md`, Section 32 — KitchenOS event architecture implementation
- `Products/KitchenOS/20_Domain_Model.md` — domain events catalogue and standard event envelope
- ADR-004 — Why KitchenOS uses domain-driven event sourcing
- `Knowledge/Patterns/DDD.md` — domain-driven design
- `Knowledge/Patterns/Privacy_By_Design.md` — events must never contain PII in payload
