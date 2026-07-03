---
id: PDR-011
title: Household Timeline Is a First-Class Product Surface
type: pdr
status: proposed
owner: product
depends_on: [GDR-001]
referenced_by: [DOC-010]
operating_principles: ["5. Earn Trust Through Transparency", "7. Truth Before Convenience"]
tags: [product-strategy, household-timeline, trust, transparency, corrections, event-sourcing]
date: 2026
---

# PDR-011: Household Timeline Is a First-Class Product Surface

**Status:** Proposed *(backfill — decision made pre-record-system; reconstructed from Product Vision Sections 59 and 60)*
**Date:** 2026-07-03
**Deciders:** Founders
**Stage Gate:** Stage 3 of Product Development Lifecycle
**Operating Principles:** 5 (Earn Trust Through Transparency), 7 (Truth Before Convenience)

---

## Context

KitchenOS acts on the household's behalf: it deducts pantry items, records spend, learns preferences, and proposes meals. A system that changes household state invisibly cannot be trusted, and a system that learns invisibly cannot be corrected. The event-sourced backend (ADR-004) already produces a complete, immutable account of everything that happened — the question is whether users see it.

The correction flows (Section 59) need an anchor: somewhere a user can find what happened, understand why, and reverse or reclassify it. Corrections are also learning signals — but only if users can find the thing to correct.

---

## Decision

**The Household Timeline is a first-class product surface** — a human-readable read model over the domain event stream, living under the Household tab and surfaced from Home after important changes. It is not a settings-page audit log.

---

## Reasons

- Trust requires visibility: every pantry deduction, budget entry, AI recommendation, and correction is inspectable where users actually look.
- The Timeline is the anchor for the entire correction system — undo, reversal, and reclassification all start from a visible event.
- The event-sourced backend makes it nearly free: the Timeline is a read model, always reconstructable (Domain Model invariant 9).
- It surfaces the AI's behaviour ("recommended", "learned", "adjusted") in the same stream as user actions — transparency as a feature, not a disclosure document.

---

## Alternatives Considered

### Option A: Audit log buried in settings
Satisfies compliance instincts, builds no trust — nobody looks there. Corrections would need their own scattered entry points. Rejected.

### Option B: Notifications only
Transient; no persistent account to review or correct against. History disappears into the notification tray. Rejected.

### Option C: No user-facing history
Cheapest; makes every automatic action invisible and every AI mistake uncorrectable by the user. Directly contradicts Principles 5 and 7. Rejected.

---

## Consequences

### Positive
- One consistent surface for trust, review, and correction; correction UX (Section 59) has a home.
- The AI's actions are accountable to the household in the household's own language.

### Negative
- A first-class surface must be maintained to first-class quality — grouping, readability, and performance of the read model are product work, not just infrastructure.

### Risks
- Timeline noise: raw event streams are unreadable. Mitigation: `HouseholdTimelineGroupCreated` grouping (Domain Model, Correction & Activity context) — one user action reads as one Timeline entry.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-03 | Proposed (backfill — decision predates the record system) | Claude (PM role), sponsored by @raj-duddu | PR # (add on merge) |

---

## Related

- `Products/KitchenOS/10_Product_Vision.md`, Section 59 — negative flows, corrections, and Household Timeline (product detail)
- `Products/KitchenOS/20_Domain_Model.md` — Household Timeline term; business invariant 9 (read model, reconstructable)
- ADR-004 — the event-sourced foundation the Timeline projects
- GDR-001 — trusted decision support; visibility of AI actions
- PDR-003 — Home screen answers a question; the Timeline is where "what happened?" is answered
