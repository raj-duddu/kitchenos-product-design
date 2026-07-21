---
id: SD-001
title: Receipt Scanning to Pantry Update — Solution Design
type: solution-design
status: draft
owner: architect
feature: PRD-001
depends_on: [PRD-001, DOC-071, ADR-010, ADR-012, DOC-020, DOC-040, GDR-002, GOV-001]
referenced_by: []
tags: [solution-design, receipt, document-understanding, pantry, budget, async, offline]
date: 2026-07-11
---

# SD-001: Receipt Scanning to Pantry Update — Solution Design

**Type:** Solution Design (Low-Level Design)
**Status:** Draft
**Date:** 2026-07-11
**Author:** Architect role (drafted; sponsored by @raj-duddu)
**Reviewer:** Tech Lead (approval required before Stage 6)
**Stage Gate:** Stage 5 — Technical Design

> **Scope:** This document covers the module-level design for receipt scanning. System-level architecture is in `Products/KitchenOS/40_Technical_Architecture.md`. This document describes *how* this feature is built, not *why* the architectural choices were made (ADR-010, ADR-012).

---

## Feature Summary

A household member photographs a grocery receipt; Document Understanding (multimodal LLM behind the AI Provider Abstraction, ADR-012) converts it asynchronously into a structured proposal with per-field confidence and food/non-food classification; the member reviews only uncertain rows and confirms; confirmation — and nothing before it (ADR-010) — adds items to the pantry and records budget spend, with a 30-second undo window.

Reference: `Products/KitchenOS/30_PRDs/PRD-001_Receipt_Scanning.md`; UX: `Products/KitchenOS/70_UX_Design_System/01_Receipt_Scanning_Wireframes.md`.

---

## Affected Building Blocks

| Building Block | Nature of change |
|---|---|
| Receipt module (modular monolith) | Full implementation: capture intake, proposal lifecycle, confirmation, undo, delete |
| AI Provider Abstraction | New Document Understanding call type (image → structured extraction contract) |
| Domain Event Bus | Emits existing Receipt-context events plus `ReceiptConfirmationUndone`, `ReceiptDeleted` |
| Pantry module | Consumes `ReceiptItemsConfirmed` → `PantryItemsAddedFromReceipt`; reversal on undo |
| Budget module | Consumes confirmation → `BudgetSpendRecorded`; reversal on undo |
| Sync Engine | Offline image queue; upload-on-reconnect |
| Household Timeline | Pending / ready / confirmed cards (UXDR-001) |

---

## Domain Events

No new event *types* beyond those already catalogued in `Products/KitchenOS/20_Domain_Model.md`. Events in this flow:

| Event | Trigger | Payload fields (key) | Criticality |
|---|---|---|---|
| `ReceiptScanned` | Capture accepted (client) | receipt_id, image_ref, captured_at, quality_flags | Low |
| `ReceiptOcrCompleted` | Extraction job finishes | receipt_id, proposal_id, totals_check, item_count, needs_review_count | Low |
| `ReceiptItemsConfirmed` | User confirms review | receipt_id, confirmed_items[], corrections[], excluded_items[] | Medium |
| `PantryItemsAddedFromReceipt` | Caused by confirmation | pantry_item_ids[], receipt_id | Medium |
| `BudgetSpendRecorded` | Caused by confirmation | amount, store, receipt_id | Medium |
| `ReceiptMarkedDuplicate` | Duplicate detected at confirmation | receipt_id, matched_receipt_id, match_basis | Low |
| `ReceiptConfirmationUndone` | Undo within window | receipt_id, undone_at | Medium |
| `PantryReceiptAdditionsReversed` / `BudgetSpendReversed` | Caused by undo | receipt_id, reversed refs | Medium |
| `ReceiptDeleted` | Delete from review | receipt_id, deleted_at | Low |

All events use the Standard Event Envelope; one scan shares a `correlation_id` end-to-end; `learning_impact`: unedited confirms → `learning`, edited rows → `correction_signal`, unresolved-uncertainty rows flagged unverified.

---

## Data Model Changes

### New tables or columns

```sql
-- Verify against existing Receipt-context schema; PRD expects no new tables.
-- If proposal storage does not fit the existing receipt tables, add:
-- receipt_proposals(id, receipt_id, extraction_json, totals_check_status,
--                   model_version, prompt_version, created_at)
-- Decision recorded here at Tech Lead review (Architecture Review condition 2).

-- Duplicate detection support:
CREATE INDEX idx_receipts_dedupe ON receipts (household_id, store_name, receipt_date, extraction_hash);
```

### Modified tables

```sql
-- receipts: photo_expires_at TIMESTAMPTZ NULL, photo_kept BOOLEAN DEFAULT FALSE
-- (photo retention policy, PRD-001 OQ-3)
```

### Four-layer impact check

| Layer | Affected? | Notes |
|---|---|---|
| Auth (identities) | No | |
| Person | No | |
| Domain (pantry, budget, receipt) | Yes | All state changes confirmation-gated (ADR-010) |
| Intelligence (beliefs, confidence) | Yes | Correction learning signals only; read-side |

> **Invariant check:** intelligence consumes domain events; domain never reads intelligence in this flow. Direction preserved.

---

## Module Responsibilities

### Receipt module (backend)

**Responsibility:** own the receipt lifecycle: intake → extraction job → proposal → confirmation/undo/delete.
**Inputs:** uploaded image, user confirmation payload, remote config (needs-review threshold, undo window, photo retention days).
**Outputs:** proposal (via API), Receipt-context events.
**Consumes:** none.
**Produces:** all events in the table above.

### AI Provider Abstraction

**Responsibility:** single Document Understanding entry point; provider selection per AI Governance Model Evaluation; enforces no-training/no-retention terms; returns the extraction contract below. No provider types leak into the Receipt module.

**Extraction output contract (per ADR-012 + PRD-001 OQ-7):**

```json
{
  "store": {"value": "Costco", "confidence": 0.98},
  "date": {"value": "2026-07-09", "confidence": 0.97},
  "printed_total": {"value": 87.43, "confidence": 0.99},
  "line_items": [{
    "name": {"value": "Organic spinach", "confidence": 0.61},
    "quantity": {"value": 10, "unit": "oz", "confidence": 0.55},
    "price": {"value": 3.49, "confidence": 0.93},
    "item_type": "food | tax | deposit | fee | other",
    "image_region": {"page": 1, "bbox": [x, y, w, h]}
  }],
  "totals_check": {"line_sum": 82.15, "reconciles": false, "gap": 5.28},
  "model_version": "…", "prompt_version": "…"
}
```

`image_region` is optional per line (PRD-001 OQ-6 — see Open Questions).

### Pantry / Budget modules

**Responsibility:** react to confirmation and undo events; no direct calls from the Receipt module (event-driven, per DOC-040 module isolation).

### Flutter (mobile)

| Layer | Responsibility |
|---|---|
| `receipt_capture_screen.dart` | Camera, client-side quality check (blur/glare/cutoff), offline queue handoff |
| `receipt_review_screen.dart` | Proposal rendering, settled/needs-review states, totals banner, edit sheet, confirm |
| `receipt_provider.dart` (Riverpod) | Proposal state, confirmation, undo countdown |
| Sync Engine | Offline image persistence + upload on reconnect |

---

## Architecture Fit

- **Bounded context:** Receipt (`receipt.*` events, DOC-020).
- **Backend module:** `receipt` module within the modular monolith (boundary pre-defined in DOC-040).
- **Flutter layer:** `features/receipt_scanning/` with Riverpod providers.
- **New infrastructure:** none — Cloud Storage (images + lifecycle rule for retention), Cloud Tasks (extraction jobs), FCM (ready notification) are stack-standard.

---

## Sequence Diagram

```text
[Flutter]            [Receipt module]        [Cloud Tasks]   [AI Provider Abstr.]   [Event Bus]

   │── POST /receipts ──────►│                     │                 │                  │
   │   (image)               │── enqueue job ─────►│                 │                  │
   │◄─ 202 + receipt_id ─────│                     │── run ─────────►│                  │
   │   (pending card)        │                     │                 │── extract ──►LLM │
   │                         │◄─ proposal + confidence + totals ─────│                  │
   │                         │── ReceiptOcrCompleted ───────────────────────────────────►│
   │◄─ FCM "ready to review" │                     │                 │                  │
   │── GET /receipts/{id}/proposal ►│              │                 │                  │
   │◄─ proposal ─────────────│                     │                 │                  │
   │── POST /receipts/{id}/confirm ►│  (duplicate check → 409 + ReceiptMarkedDuplicate) │
   │                         │── ReceiptItemsConfirmed ─────────────────────────────────►│
   │                         │      └─► PantryItemsAddedFromReceipt, BudgetSpendRecorded │
   │◄─ 200 (undo window) ────│                     │                 │                  │
   │── POST /receipts/{id}/undo (≤30s) ►│── ReceiptConfirmationUndone + reversals ──────►│
```

---

## AI Decision Criticality

- **Criticality level:** **Medium** (GOV-001) — proposal with explanation and confidence; one primary confirm action; no autonomous effect.
- **Allergy Guard required:** No at pantry entry — applies downstream at recommendation time (PRD-001).
- **Explanation field required:** Yes — totals-check result, needs-review reasons, `item_type` classification.
- **Explicit user confirmation required:** Yes — sole state-changing trigger (ADR-010).
- **Safeguard implementation:** confirmation-gated event emission; totals reconciliation marks proposals low-confidence on mismatch; needs-review threshold from server-side remote config (never client-hardcoded, never displayed); undo window remote-configurable (default 30s).

---

## Error Cases and Edge Cases

| Case | Expected behaviour |
|---|---|
| Poor capture quality | Client-side retake prompt with reason; "Use anyway" always offered |
| Extraction fails | Notification with retake + manual quick-entry (same confirmation flow/events) |
| Extraction slow / provider down | Pending card explains delay; automatic retry with backoff; manual entry offered |
| Totals mismatch | Proposal marked low-confidence; amber banner; user marks tax/deposit or corrects rows |
| Duplicate at confirmation | 409; `ReceiptMarkedDuplicate`; no pantry additions |
| Undo after window expiry | 410; UI hides Undo at expiry; PantryCorrection path remains |
| Confirm with unresolved uncertain rows | Allowed; extracted values stand; rows flagged unverified for learning |
| Offline capture | Image queued locally; "waiting for connection"; resumes without user action |
| App killed during pending | State recoverable from server on next open (proposal is server-side) |
| Likely truncated long receipt | Warn at capture (multi-shot deferred to MVP-1, PRD-001 OQ-5) |

---

## Security Considerations

- Authorization: all endpoints household-scoped; membership check on every receipt access; undo/delete restricted to household members.
- PII: receipt images may contain loyalty numbers / partial card digits — images in Cloud Storage with household-scoped ACLs; provider under no-training/no-retention terms (GDR-002/ADR-012).
- No new consent class; camera permission only.
- **Security review required before Stage 7** (Architecture Review ARC-001, condition 1): upload validation (type/size), signed URLs, provider data-handling verification.

---

## Privacy Impact

- New data: receipt images — justified as the extraction source; auto-deleted after remote-configurable window (default 90 days) with visible expiry and per-receipt Keep pin (PRD-001 OQ-3). Line items and events persist independently.
- AI layer data flow: image only; no household profile or member PII in the extraction context.
- ConsentGrant: no new or modified grant.

---

## API Contract

| Method | Path | Purpose | Error cases |
|---|---|---|---|
| POST | /receipts | Upload capture; create extraction job | 400 invalid image, 401/403, 413 too large |
| GET | /receipts/{id}/proposal | Fetch proposal for review | 401/403, 404, 425 not ready |
| POST | /receipts/{id}/confirm | Confirm reviewed items | 401/403, 404, 409 duplicate, 422 invalid edits |
| POST | /receipts/{id}/undo | Undo within window | 401/403, 404, 410 window expired |
| DELETE | /receipts/{id} | Delete receipt + image + proposal | 401/403, 404, 409 already confirmed (must undo first) |

Full request/response schemas to `80_API_Reference/` when that section is created.

---

## Offline Behaviour

- **Capture:** fully offline — image persisted locally, queued by the Sync Engine, uploaded on reconnect without user action.
- **Review/confirm:** requires connectivity (proposal is server-side); pending card communicates state.
- **Conflict resolution:** none needed — a receipt has a single linear lifecycle per household; duplicate detection handles double-submission.

---

## Testing Strategy

| Test Type | What to Test | Tool |
|---|---|---|
| Unit | Totals reconciliation, duplicate hash, threshold classification, undo-window logic | Jest |
| Integration | All five endpoints incl. 409/410/425 paths; event emission + causation chain | Supertest + Testcontainers |
| BDD | All 10 PRD-001 scenarios, incl. the ADR-010 no-confirmation scenario | As defined in PRD |
| Widget | Review screen states: settled/needs-review, totals banner, edit sheet, undo countdown | flutter_test |
| Golden | Review rows, pending/confirmed cards | golden_toolkit |
| Model evaluation | ≥50-receipt evaluation set before release; re-run on prompt/model change | GOV-001 Model Evaluation |
| Offline/sync | Queue, reconnect, kill-and-restore | Stage 8 |

---

## Acceptance Criteria (Technical)

```gherkin
Given a proposal whose line items sum differs from printed_total beyond tax logic
When the proposal is prepared
Then totals_check.reconciles is false and the proposal is marked low-confidence

Given a confirmed receipt
When POST /receipts/{id}/undo arrives within the configured window
Then ReceiptConfirmationUndone, PantryReceiptAdditionsReversed and BudgetSpendReversed
  are emitted with the original correlation_id

Given an extraction job and a provider outage
When retries are exhausted
Then the receipt enters failed state, the user is notified with retake and
  manual-entry options, and no pantry or budget event exists for the receipt
```

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | PRD-001 OQ-6: per-line `image_region` from extraction, or zoomable full-image viewer as the floor? Contract above makes regions optional; viewer is the guaranteed floor. Proposed: accept optional-region contract. | Architect + Tech Lead | Open — resolve at SD review |
| 2 | Does proposal storage fit existing receipt tables, or is `receipt_proposals` needed? | Tech Lead | Open — resolve at SD review |
| 3 | Initial needs-review threshold value (calibrated from evaluation set) | Product + Architect | Open — blocked on evaluation set |

---

## Related

- PRD: `Products/KitchenOS/30_PRDs/PRD-001_Receipt_Scanning.md`
- UX: `Products/KitchenOS/70_UX_Design_System/01_Receipt_Scanning_Wireframes.md`
- Architecture Review: `Products/KitchenOS/45_Solution_Designs/ARC-001_PRD-001_Architecture_Review.md`
- ADRs: ADR-010 (confirmation-only mutation), ADR-012 (Document Understanding)
- GDR-002 (Privacy by Design); GOV-001 (AI Governance — criticality, model evaluation)
