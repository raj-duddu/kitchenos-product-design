---
id: PRD-001
title: Receipt Scanning to Pantry Update
type: prd
status: draft
owner: product
depends_on: [DOC-010, DOC-020, ADR-010, ADR-012, GDR-002]
referenced_by: []
tags: [prd, receipt, document-understanding, pantry, shopping-trip, budget, mvp-0]
date: 2026
---

# PRD-001: Receipt Scanning to Pantry Update

**PRD ID:** PRD-001
**Status:** Draft
**Owner:** Product (drafted via PM role, sponsored by @raj-duddu)
**Stage Gate:** Stage 3 of Product Development Lifecycle
**Created:** 2026-07-03
**Last Updated:** 2026-07-03

---

## Problem Statement

> After shopping, households have no low-effort way to tell KitchenOS what they bought — so the pantry drifts from reality, and every recommendation built on it degrades.

---

## Background / Discovery

The pantry is the foundation for every downstream capability (ADR-010 context). Manual entry after every trip is too much friction to sustain; a pantry that drifts silently destroys trust in recommendations.

Receipt scanning is the lowest-effort data-in path: one photo captures an entire trip. The extraction approach is decided — ADR-012: a Document Understanding capability (multimodal LLM behind the AI Provider Abstraction) converts the image into a structured proposal with per-field confidence; the user confirms; only confirmation touches the pantry (ADR-010).

Founder experience with OCR-based receipt systems showed the failure mode to avoid: extraction that needs manual correction *every time* teaches users to skip scanning entirely. The trust bar for this feature is that most receipts need zero or near-zero correction.

---

## Product Vision Alignment

- Principle 1 (Transform Complexity into Clarity) — a crumpled 40-line receipt becomes a clean list of pantry items.
- Principle 2 (Turn Information into Guidance) — the receipt is not stored as text; it becomes pantry state, budget position, and learning signals.
- Principle 4 (AI Recommends. People Decide.) — extraction is a proposal; the user's confirmation is the only thing that changes household state.
- Principle 5 (Earn Trust Through Transparency) — per-field confidence is shown, uncertain rows are highlighted, and the totals check is visible.

**North Star (Weekly Trusted Household Decisions Completed):** every confirmed receipt is a trusted decision completed, and pantry accuracy raises the acceptance rate of every downstream recommendation.

---

## Scope

### In Scope

- Receipt capture (camera) with client-side quality check and retake prompt.
- Async extraction via Document Understanding (ADR-012): store, date, total, line items (name, quantity, unit, price), per-field confidence.
- Totals reconciliation check (line items vs printed total, ± tax logic) as the primary fabrication guard.
- Review-and-confirm screen: uncertain rows highlighted, editable guesses, add/remove items, "not a food item" handling for tax/deposit/bag lines.
- Confirmation completes a ShoppingTrip → `PantryItemsAddedFromReceipt`, `BudgetSpendRecorded` (Domain Model events; no new events required).
- Pending state in Household Timeline; push notification when ready to review.
- Offline capture: image queued locally (Sync Engine), processed on reconnect.
- Duplicate receipt detection at confirmation time (`ReceiptMarkedDuplicate` blocks pantry additions).
- Manual quick-entry fallback when extraction fails or the user prefers it.
- Corrections during review emit correction-classed learning signals (Domain Model `learning_impact`).

### Out of Scope

- Item-to-canonical-food normalization beyond what extraction provides (deep normalization is MVP-1 — Vision §39.5).
- Price analytics, store comparison (Vision §39.5 skip list).
- Document types other than receipts (ADR-012 scope discipline: one type in MVP-0).
- Linking receipt items back to a pre-existing ShoppingList (`ShoppingItemsMatched` exists in the Domain Model but matching UX is MVP-1).
- Warranty/return tracking, receipt search.

### MVP Boundary

Photograph a receipt → review the proposal → confirm → pantry and budget updated. Everything else is enhancement.

---

## User Stories

### Story 1: Scan and forget

**As a** household member unloading groceries
**I want to** photograph the receipt and put my phone away
**So that** the pantry updates without me standing there waiting

**Acceptance Criteria:**
- [ ] Capture-to-pocket takes under 15 seconds including quality check.
- [ ] A pending card appears in the Household Timeline immediately.
- [ ] I receive a push notification when the proposal is ready to review.
- [ ] Nothing about my pantry, budget, or shopping list changes before I confirm.

### Story 2: Review only what needs me

**As a** household member reviewing a scanned receipt
**I want to** see which extracted items the system is unsure about
**So that** I correct two rows instead of auditing forty

**Acceptance Criteria:**
- [ ] Rows at or above the confidence threshold render as settled; rows below it are visually distinct and editable with the model's guess pre-filled.
- [ ] Confidence appears only as settled / needs-review states; numeric scores are never displayed in the review UI.
- [ ] The needs-review threshold is server-side remote configuration: changed without an app release, never exposed to users.
- [ ] A totals banner shows whether line items reconcile with the printed total.
- [ ] I can edit any row, remove rows, mark rows "not a food item," and add missed items.
- [ ] Tapping an uncertain row shows the scanned receipt image (zoomed to the relevant region where extraction provides one) — verification never requires the paper receipt.
- [ ] I can confirm with uncertain rows unresolved: the model's guess stands, and the item remains correctable later via pantry correction. Uncertainty is visible, never blocking.
- [ ] One primary action confirms the whole receipt.

### Story 3: Offline shopper

**As a** household member in a store with no signal
**I want to** scan my receipt anyway
**So that** it processes when I'm back online

**Acceptance Criteria:**
- [ ] Capture works offline; the pending card shows "waiting for connection."
- [ ] Processing resumes without user action on reconnect.

### Story 4: It didn't work

**As a** household member whose receipt is crumpled or faded
**I want to** know quickly and have a fallback
**So that** one bad scan doesn't cost me the trip's data

**Acceptance Criteria:**
- [ ] Poor image quality is caught at capture time with a retake prompt where possible.
- [ ] Failed extraction produces a clear notification with retake and manual quick-entry options.
- [ ] Manual quick-entry creates the same ShoppingTrip confirmation flow (same events).

---

## BDD Scenarios

### Scenario: Happy path — confirmed receipt updates pantry and budget

```gherkin
Given a household with an empty pantry
And a legible receipt for 14 grocery items totalling $87.43
When the member scans the receipt
And the Document Understanding proposal reconciles with the printed total
And the member confirms the proposal without edits
Then a ShoppingTrip is confirmed
And 14 PantryItems are added via PantryItemsAddedFromReceipt
And BudgetSpendRecorded carries $87.43
And the Household Timeline shows one grouped entry for the trip
```

### Scenario: Uncertain row verified from the scanned image, not the paper

```gherkin
Given a review screen with an uncertain row "Organic spinach? 10 oz"
When the member taps the row
Then the scanned receipt image is shown, positioned at that line where available
And the member can correct or accept the guess without the physical receipt
```

### Scenario: Confirming with unresolved uncertainty is allowed

```gherkin
Given a review screen with 2 uncertain rows the member does not resolve
When the member confirms the receipt
Then all 14 items enter the pantry, including the 2 model guesses
And the 2 guesses remain correctable via PantryCorrection
And their learning_impact reflects unverified extraction
```

### Scenario: Low-confidence rows require attention

```gherkin
Given a scanned receipt where 2 of 14 items extract below the confidence threshold
When the member opens the review screen
Then exactly those 2 rows are highlighted as needing review
And each shows the model's guess pre-filled and editable
And the confirm action is available without forcing edits to settled rows
```

### Scenario: Totals mismatch flags the proposal

```gherkin
Given a scanned receipt whose extracted line items sum to $82.15
And the printed total reads $87.43
When the proposal is prepared
Then the proposal is marked low-confidence
And the review screen shows a totals-mismatch banner
And no pantry or budget change occurs until the member resolves and confirms
```

### Scenario: Nothing happens without confirmation (ADR-010)

```gherkin
Given a receipt proposal is ready for review
When the member never opens or confirms it
Then no pantry, budget, or shopping-list state changes
And the proposal remains visible in the Household Timeline as pending
```

### Scenario: Duplicate receipt is blocked

```gherkin
Given a receipt that was already confirmed for this household
When the same receipt is scanned again
And duplicate detection matches store, date, and extraction hash
Then ReceiptMarkedDuplicate is recorded
And the member is told this receipt was already processed
And no pantry additions occur
```

### Scenario: Correction emits a learning signal

```gherkin
Given a review screen where one item reads "Organic spinach 10 oz"
When the member corrects it to "Organic arugula 5 oz"
And confirms the receipt
Then the confirmed pantry item is arugula 5 oz
And the correction is recorded with correction-classed learning_impact
```

### Scenario: Photo retention is legible, never a surprise

```gherkin
Given a confirmed receipt whose photo auto-deletes in 90 days
When the member views it in the Receipts segment
Then the photo expiry date is shown on the receipt
And a "Keep" action exempts this photo from auto-delete
And line items and events remain complete after any photo deletion
```

### Scenario: Offline capture queues and recovers

```gherkin
Given the member's device is offline
When they scan a receipt
Then the image is queued locally by the Sync Engine
And the Timeline card shows a waiting-for-connection state
When connectivity returns
Then extraction proceeds without user action
```

---

## UX Notes

The interaction pattern (scan-and-forget → pending card → notify → review-highlighted-uncertainty → confirm) is proposed as **UXDR-001** — it is expected to become the standard shape for all async AI proposals.

### Screen Flow

The Shop tab is segmented `List | Receipts` per UXDR-002 (proposed): the scan action is prominent in both segments; the Receipts segment holds pending, needs-review, and confirmed receipts.

```text
[Shop tab / Home suggestion]
    │  "Scan receipt"
    ▼
[Camera capture + quality check]     ← retake prompt on blur/glare/cutoff
    │  done (≤15s)
    ▼
[Timeline pending card]              ← user leaves; extraction runs async
    │  push notification
    ▼
[Review & confirm screen]            ← uncertain rows highlighted; totals banner
    │  "Add N items to pantry"
    ▼
[Confirmation]                       ← Timeline grouped entry; pantry + budget updated
```

### Empty State

First-run Shop tab includes "Scan your first receipt" as the primary suggestion (Vision §21 empty-state rules; onboarding path in §50).

### Error State

The scanned image is the verification source throughout review — the paper receipt is never needed after capture (PDR-005: the system asks only about its own extraction failures, and answers are a glance away). Unreadable receipt → notification "We couldn't read this receipt" with retake and manual-entry actions. Totals mismatch → amber banner naming the discrepancy. Extraction service down → pending card explains the delay; retry is automatic; manual entry always offered.

### Loading State

Never a blocking spinner. The pending state lives in the Timeline card ("Reading your receipt…"); the user is free everywhere in the app.

---

## Technical Design

> Feature is non-trivial (new capability integration, async pipeline, confirmation flow): a full Solution Design is required at Stage 5 — planned as SD-001 in `Products/KitchenOS/45_Solution_Designs/`.

### Key Technical Decisions (already recorded)

- ADR-012 — Document Understanding via multimodal LLM behind the AI Provider Abstraction; model selection via AI Governance Model Evaluation; totals reconciliation as primary guard; no OCR fallback (fallback is manual entry).
- ADR-010 — confirmation-only pantry mutation; this PRD adds no exceptions.
- AI criticality classification: **Medium** (proposal shown with explanation and confidence; one primary confirm action; no autonomous effect). Extraction never touches safety constraints directly — items enter the pantry only after human confirmation, and Allergy Guard applies downstream at recommendation time, not at pantry entry.

### Sequence (brief)

```text
[Mobile capture] → [Cloud Storage image] → [Cloud Tasks job]
  → [Document Understanding via AI Provider Abstraction]
  → [proposal + per-field confidence + totals check]
  → [FCM notify] → [Review & confirm UI]
  → [ShoppingTripConfirmed → PantryItemsAddedFromReceipt, BudgetSpendRecorded]
```

### New API Endpoints (summary)

| Method | Path | Purpose |
|---|---|---|
| POST | /receipts | Upload capture, create processing job |
| GET | /receipts/{id}/proposal | Fetch extraction proposal for review |
| POST | /shopping-trips/{id}/confirm | Confirm reviewed items; produce domain events |

Full contract: Stage 5 Solution Design / `80_API_Reference/`.

---

## Domain Model Impact

- [ ] New entity: none — Receipt, ShoppingTrip, PantryItem all exist.
- [ ] New domain event: none — `ReceiptScanned`, `ReceiptOcrCompleted`, `ReceiptItemsConfirmed`, `PantryItemsAddedFromReceipt`, `BudgetSpendRecorded`, `ReceiptMarkedDuplicate` all exist.
- [ ] New business invariant: none — ADR-010 invariant already governs.
- [x] Clarification only: proposal schema (per-field confidence, totals status) is Document Understanding output, not domain state — it lives outside the domain until confirmation.

---

## Architecture Impact

- [x] New API endpoints (above).
- [x] Receipt module implementation within the modular monolith (boundary already defined in 40_TA).
- [ ] Database schema change: none beyond existing tables.
- [ ] New infrastructure component: none — Cloud Storage, Cloud Tasks, FCM, AI Provider Abstraction all stack-standard.

Architecture Review required at Stage 5 (AI-touching: apply the AI Architecture Review checklist in `Company/Governance/AI_Governance.md`).

---

## Security and Privacy

- [x] Touches user PII: yes — receipt images may contain loyalty numbers, partial card digits. Per ADR-012/GDR-002: provider under no-training/no-retention terms. Photo retention: a remote-configurable window after confirmation (default 90 days, aligned to typical return windows), expiry date visible on each receipt, per-receipt "Keep" pin exempts a photo from auto-delete — users treat scanned as saved, so deletion is legible, never silent (amends ADR-012's delete-on-confirmation mitigation). Line items and domain events persist regardless of photo deletion.
- [x] Touches household financial data: yes — spend amounts; household-scoped visibility (privacy open question on member spend visibility tracked in Vision §60).
- [ ] Requires new permissions or consent: camera permission only; no new data consent class.
- [x] Requires security review: yes, at Stage 5 (external AI processing path).

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | Confidence threshold for "needs review" | Product + Architect | **Resolved 2026-07-04** — server-side remote configuration: tunable by the team without an app release, never user-visible (Principle 1 — users are not asked to reason about confidence). Initial value calibrated from the evaluation set. SD-001 requirement. |
| 2 | Numeric confidence display? | Product | **Resolved 2026-07-04** — confidence renders as binary states only (settled / needs review); numeric scores never appear in the review UI. Uncertainty stays visibly distinguishable (Principle 7); numbers would be false precision, not guidance (Principles 1, 2). See the display-form clarification in `Company/Governance/AI_Governance.md`. |
| 3 | Receipt image retention | Product + Founders | **Resolved 2026-07-04** — photos kept for a remote-configurable window after confirmation (default 90 days, aligned to typical return windows); the expiry date is visible on each receipt; a per-receipt "Keep" pin exempts a photo from auto-delete. Retention must be legible — users treat "scanned" as "saved," so deletion is never a surprise. Line items and events persist regardless. Amends ADR-012's image-retention mitigation. |
| 4 | Voice input for manual quick-entry | Product | Deferred to MVP-1 |
| 5 | Multi-shot capture for long receipts | Product + Architect | Deferred to MVP-1 — MVP-0 detects likely truncation and warns at capture |
| 6 | Per-line image regions for tap-to-verify, or zoomable full-image viewer as the floor? | Architect (Stage 5) | Open |

---

## Definition of Done

- [ ] All acceptance criteria verified by QA.
- [ ] BDD scenarios pass, including the ADR-010 no-confirmation scenario.
- [ ] Extraction evaluated against the ≥50-receipt evaluation set (AI Governance Model Evaluation) before release.
- [ ] Totals reconciliation and duplicate detection covered by automated tests.
- [ ] Domain Model updated if changed (none expected).
- [ ] Architecture documentation updated if changed.
- [ ] Feature flagged for staged rollout.
- [ ] No critical bugs open.
