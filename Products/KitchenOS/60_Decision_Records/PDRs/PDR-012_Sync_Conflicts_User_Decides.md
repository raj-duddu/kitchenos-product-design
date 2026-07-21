---
id: PDR-012
title: Multi-Device Sync Conflicts — User-Decided Resolution, Not Silent Overwrites
type: pdr
status: accepted
owner: product
depends_on: [PDR-002, GDR-001, ADR-004]
referenced_by: [DOC-010, PRD-001, SD-001]
operating_principles: ["1. Reduce Complexity for Real Users", "4. AI Recommends. People Decide.", "5. Earn Trust Through Transparency"]
tags: [sync, offline, multi-device, conflict-resolution, household, transparency, user-agency, product-behaviour]
date: 2026
---

# PDR-012: Multi-Device Sync Conflicts — User-Decided Resolution, Not Silent Overwrites

**Type:** PDR (Product Decision Record)
**Status:** Accepted
**Date:** 2026-07-20
**Deciders:** Founding team
**Stage Gate:** Stage 3 — Product Definition

**Operating Principles:**
- Principle 1: Reduce Complexity for Real Users
- Principle 4: AI Recommends. People Decide.
- Principle 5: Earn Trust Through Transparency

---

## Context

KitchenOS is built offline-first: households can scan receipts, edit pantry, and cook without network connectivity. Changes are queued locally and sync when the device reconnects.

In multi-member households with multiple devices, conflicts arise naturally:

- **Device A** (Mom's phone, offline): Scans receipt at 3:15pm — adds 2L milk to pantry
- **Device B** (Dad's tablet, online): At 3:16pm, reports that milk was used in dinner — deducts 1L
- **Device B syncs immediately.** Device A reconnects at 3:45pm

When Device A syncs, it sees a conflict: Device A says pantry has 2L milk, Device B says it has 1L. Without a conflict resolution strategy, one of these happens:

1. **Silent overwrite:** Device A's state overwrites Device B's state (loses Dad's consumption record)
2. **Silent overwrite (reversed):** Device B's state overwrites Device A's state (loses Mom's receipt)
3. **Last-write-wins:** Whoever synced last is correct (unpredictable; breaks trust)
4. **Blocking:** The household can't proceed until an admin manually resolves it (frustrating)

None of these options preserve household accuracy or user trust. The conflict contains real information: the receipt is a fact; the consumption is a fact. Both should be preserved and reconciled by the household.

### Why This Matters

KitchenOS's core promise is that the pantry state is accurate and the household can trust recommendations built on it (Vision §8.6 — "Decisions, Not Data"). A system that silently loses information violates this promise. Households won't trust a system that says "your milk is gone" because the system lost track of it, not because it was actually used.

This is not a technical implementation detail. It is a product behaviour decision about whether the household or the algorithm decides what is real.

---

## Decision

**When a multi-device sync conflict is detected, KitchenOS will surface both versions to the user with full context (timestamps, source device, the conflicting state) and require the user to choose which version is correct, or manually merge them. No conflict is resolved silently.**

This decision applies to all household-scoped entities: pantry items, shopping lists, meal plans, budget records, and Timeline entries.

---

## Rationale

### 1. Trust Through Transparency (Principle 5)

A system that silently resolves conflicts teaches users that the system is deciding what is real. Over time, users stop trusting the pantry state because they don't understand how it changed.

Surfacing conflicts teaches users: "The system can't decide. Here's what each device saw. You know your household better than the algorithm does."

Example:
- **Bad:** System silently keeps Device B's state. Household never knows. Later, milk is missing from pantry and recommendations suffer.
- **Good:** System shows both versions. Mom says "Oh, the receipt was wrong — we only bought 1L." Both changes are correct; the household resolves it and learns for next time.

### 2. Principle 4: AI Recommends; People Decide

Conflict resolution is a decision. The household knows their reality better than an algorithm. Per the product principle (Section 8.1), the AI should not make important decisions silently.

Conflict resolution belongs in the user's hands because:
- The conflict is a symptom of missing information (e.g., was the receipt written down before the milk was consumed, or after?)
- The user knows which device's clock is more accurate
- The user knows if the milk was actually bought or if it was a demo/return
- The user knows if it was consumed or spilled or returned

### 3. Learning Opportunity

Conflicts are data. When a household resolves a conflict, the system learns:
- Which device state was correct (for future tie-breaking)
- Whether timestamps are reliable (if Device A's timestamp was wrong)
- Common conflict patterns (consumption often follows receipts)

In MVP-0, the system makes no automatic assumptions. In MVP-1+, patterns in user resolutions can train better auto-resolution policies:
- "We've learned that when a receipt and consumption happen within 30 minutes of each other, you usually keep both. Shall we auto-resolve this pattern?"
- "We've noticed Device A's clock is always 5 minutes fast. Should we account for that?"

This is the operational expression of Principle 4: the system suggests a resolution based on learned patterns, and users approve or override it.

### 4. Prevents Silent Data Loss

Silent overwrites inevitably lose information. The household can't audit what happened, and the Learning Engine can't learn from the conflict.

Surfacing conflicts ensures:
- Nothing is silently deleted
- The household can see why the pantry state changed
- Corrections and reversals are recorded as events, not silent mutations
- The Household Timeline shows the resolution (Vision §8.9 — "Timeline is product memory")

---

## Alternatives Considered

### Option A: Silent Last-Write-Wins

When a conflict is detected, keep the state from whichever device synced last.

**Pros:**
- Simplest to implement
- No UI required
- Determinate outcome (no ambiguity)

**Cons:**
- Loses information silently
- Unpredictable to the user (which device happened to sync last?)
- Breaks trust in pantry accuracy
- No learning signal — the system doesn't know which state was correct
- Violates Principle 5 (Earn Trust Through Transparency)

**Rejected.**

---

### Option B: Silent Automatic Resolution (MVP-1+, not MVP-0)

Implement heuristics immediately: if the entities are the same item and the total quantity is positive, assume both are correct and add them together. If one is higher, assume the lower one is correct.

**Pros:**
- Reduces cognitive load on households
- Scales to frequent small conflicts

**Cons:**
- Wrong heuristics will corrupt pantry state (e.g., "both changes are correct" fails if one is a receipt and one is a return/cancellation)
- No way to validate the heuristic without user feedback
- Violates Principle 4 (AI Recommends; People Decide) in MVP-0
- Requires historical data to train, which we don't have on day one

**Deferred to MVP-1+ based on learned patterns from user resolutions. MVP-0 approach: user decides.**

---

### Option C: User-Decided Resolution (Chosen)

When a conflict is detected, surface both versions to the user. User sees:
- Device A's state, timestamp, and source event
- Device B's state, timestamp, and source event
- Options: [Keep A] [Keep B] [Edit & Merge] [Ask Me Later]

**Pros:**
- Transparent: user sees exactly what happened
- Preserves trust: user controls the truth
- Learning signal: each resolution teaches the system about household patterns
- Defensible: when the user is wrong, it's their choice; the system is honest about its uncertainty
- Aligns with Principle 4 (People Decide) and Principle 5 (Transparency)
- Future-proof: user resolutions train MVP-1+ auto-resolution

**Cons:**
- Requires UI and decision from the user
- Cognitive load in households with frequent conflicts (though this is rare in practice — offline conflicts are unusual)
- Adds latency to sync completion

**Chosen for MVP-0. This is the product behaviour.**

---

## Consequences

### Positive

- **Trust is structural, not hoped-for.** Users know the system never silently loses information. Over time, this builds confidence in pantry state.
- **Transparency teaches household routines.** When a household resolves a conflict, they learn about their own usage patterns. "Oh, we always consume milk within an hour of buying it."
- **Learning foundation for future automation.** MVP-1+ can propose auto-resolution policies based on accumulated user resolutions: "We've seen you keep both changes 95% of the time when they're 30 minutes apart. Shall we auto-resolve this pattern?"
- **Aligns with product philosophy.** The system is honest about what it doesn't know. The household is the authority on their own reality. Conflicts are resolved by the household, not the algorithm.
- **Supports multi-device households from day one.** Families with multiple members on multiple devices work reliably because conflicts are explicit, not hidden.

### Negative

- **Requires user attention for conflict resolution.** If a household has frequent conflicts (e.g., due to poor network or high concurrency), users will need to make decisions. This is uncomfortable.
- **Latency on sync:** The household member who initiates sync might see a "conflict pending resolution" message before changes finish syncing. This is minor but adds complexity.
- **UI complexity:** The conflict resolution screen must be clear and unambiguous. Poor UX here breaks trust immediately.
- **Cognitive load edge case:** A household that is highly concurrent (many devices, many changes, poor network) could accumulate multiple conflicts. However, this is rare in practice — most households have 1–2 active devices and sync frequently.

### Scope Boundary

- **This PDR defines the product behaviour.** Conflict detection logic (how to identify conflicts), the conflict resolution UI design, and the implementation in the Sync Engine are separate concerns documented in Solution Design (SD-001) and Technical Architecture.
- **Conflict resolution applies only to domain-scoped entities** (pantry, shopping, budget, meals, Timeline). Authentication and Identity state (whose account this is) are never synced; they are per-device.
- **MVP-1+ scope:** Patterns in user resolutions will inform auto-resolution policies. Those policies will be documented as future PDRs. This PDR locks the MVP-0 principle (user decides); future policies extend it.
- **Not in scope:** Conflict resolution for collaborative editing (multiple users typing in the same document simultaneously). KitchenOS does not support real-time collaborative editing in MVP-0.

---

## Implementation Impact

**The Sync Engine (Vision §43 Month 1–2) must implement:**

1. **Conflict detection:** Identify when two devices have modified the same entity between their last sync
2. **Conflict surfacing:** Store both versions with full context (timestamp, source device, the actual state)
3. **Conflict resolution UI:** Present both versions clearly; collect user decision
4. **Resolution recording:** Emit a `ConflictResolutionEvent` to the event log (Vision §22A)
5. **State application:** Apply the chosen resolution to the canonical state
6. **Timeline entry:** Record the resolution in the Household Timeline with full context

See `Products/KitchenOS/45_Solution_Designs/SD-001_Receipt_Scanning.md` and future Sync Engine design for technical details.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-20 | Proposed & Accepted | Founding team (Raj Duddu) | Vision §22A (Offline Sync Conflicts); Vision §43 (Sync Engine Month 1–2); [PDR acceptance PR] |

---

## Related

- `Products/KitchenOS/10_Product_Vision.md`, Section 22A (Offline Sync Conflicts) — this PDR's home in the Vision
- `Products/KitchenOS/10_Product_Vision.md`, Section 43 (Three-Month MVP-0 Build Plan) — Sync Engine scheduled Month 1–2
- PDR-002 — Household as primary unit (households decide, not individuals)
- GDR-001 — Trusted Decision Support (the principle that AI doesn't decide alone)
- ADR-004 — Event Sourcing (every decision is an immutable event)
- `Products/KitchenOS/20_Domain_Model.md` — ConflictResolutionEvent, conflict_detected status
- `Products/KitchenOS/40_Technical_Architecture.md` — Sync Engine architecture (future)
- `Company/Operating_Principles.md` — Principle 1 (Reduce Complexity), Principle 4 (AI Recommends; People Decide), Principle 5 (Earn Trust Through Transparency)

---

