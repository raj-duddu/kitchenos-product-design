---
id: UXDR-002
title: Receipts Live in the Shop Tab as a Segmented View
type: uxdr
status: proposed
owner: product
depends_on: [DOC-010]
referenced_by: [PRD-001]
operating_principles: ["1. Transform Complexity into Clarity", "9. Simplicity Is a Feature"]
tags: [uxdr, navigation, shop-tab, receipts, segmented-control, information-architecture]
date: 2026
---

# UXDR-002: Receipts Live in the Shop Tab as a Segmented View

**Status:** Proposed
**Date:** 2026-07-04
**Deciders:** Founders
**Stage Gate:** Stage 4 of Product Development Lifecycle
**Operating Principles:** 1 (Transform Complexity into Clarity), 9 (Simplicity Is a Feature)

---

## Context

The Product Vision splits the receipt concept across two tabs: the scan *entry point* lives in Shop (Section 19.3), while the receipt *archive* lives in Household (Section 19.5). One concept, two homes — the UX equivalent of the documentation duplication this repository forbids. The app-shell wireframe review (2026-07) made the split visible, and founder review proposed consolidating.

Receipts are shopping-lifecycle artifacts by domain definition: a Receipt is evidence of a completed ShoppingTrip (`Products/KitchenOS/20_Domain_Model.md` — "Receipt is evidence, not the reality"). The shopping mission and its evidence belong to the same surface. The segmented-control pattern (two views of one job inside one tab) fits: the List segment is the mission's intention, the Receipts segment is its record.

Frequency check (Vision Section 16): Receipt Scan is weekly/Medium — it does not merit a top-level tab, and it is too central to the Shop mission to bury in the system layer.

---

## Decision

**The Shop tab is a segmented view: `List | Receipts`. The receipt archive — pending, needs-review, and confirmed receipts — moves from Household to the Receipts segment. The Household tab drops its Receipts entry.**

Boundaries of the decision:

- **Scan receipt stays prominent in both segments** — it is the tab's highest-value action and is never buried inside the archive.
- **Notification deep-link remains the primary door to pending-receipt review** (UXDR-001). The Receipts segment is where receipts are *found*, not the only way to reach them.
- **The Household Timeline still shows receipt events** — the Timeline records what happened (PDR-011); the Receipts segment holds the artifacts. Events and artifacts are different things.
- Segment discipline: segments are for multiple views of one job. Adding a third segment to Shop requires a new UXDR, not a habit.

---

## Reasons

- One concept, one home: users looking for a receipt should have exactly one obvious place to look, and it should be where receipts are created.
- Domain alignment: ShoppingList (intention) and Receipt (evidence of the ShoppingTrip) are two faces of the same execution lifecycle — the segments mirror the model.
- Household shrinks from seven buried items to six, easing the system-layer's junk-drawer risk.
- The segmented pattern keeps the five-tab shell intact (Vision Section 18.3) — no new top-level navigation.

---

## Alternatives Considered

### Option A: Keep the current split (do nothing)
Scan in Shop, archive in Household. Two homes for one concept; users must learn where receipts "live" separately from where they make them. Rejected.

### Option B: Receipts as a sixth top-level tab
Violates the frequency map (weekly/Medium feature at top level) and breaks the five-tab decision (Vision Section 18.3) for no navigational gain. Rejected.

### Option C: Consolidate everything into Household (move the scan entry there too)
One home, wrong home: puts a weekly action inside the rarely-visited system layer and severs it from the shopping mission it completes. Rejected.

### Option D (chosen): Segmented Shop tab — List | Receipts

---

## Consequences

### Positive
- Receipts have one home, adjacent to where they are created; the Shop tab tells the whole shopping story from intention to evidence.
- Household simplifies; PDR-011's Timeline remains its trust anchor without artifact clutter.

### Negative
- The Shop tab carries more surface area; its empty states must handle both segments (Vision Section 21 rules apply per segment).
- On acceptance, Vision Sections 19.3 and 19.5 must be updated (living-document follow-up), and PRD-001's screen flow gains the segment context.

### Risks
- Segment creep: Shop accumulating a third and fourth segment would recreate the junk drawer inside a tab. Mitigation: the segment-discipline boundary above.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-04 | Proposed | Claude (PM role), sponsored by @raj-duddu | PR # (add on merge) |

---

## Related

- UXDR-001 — async proposal pattern; notification deep-link remains the review door
- PRD-001 — receipt scanning feature this navigation decision houses
- `Products/KitchenOS/10_Product_Vision.md` — Sections 16 (frequency), 18.3 (five-tab decision), 19.3/19.5 (to be updated on acceptance)
- `Products/KitchenOS/20_Domain_Model.md` — ShoppingTrip/Receipt: evidence vs reality
